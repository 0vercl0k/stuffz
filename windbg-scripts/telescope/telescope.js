// Axel '0vercl0k' Souchet - 7th December 2018

'use strict';

const log = host.diagnostics.debugLog;
const logln = p => host.diagnostics.debugLog(p + '\n');

//
// Config variables.
//

// This is the number of lines the !telescope command displays.
const DefaultNumberOfLines = 10;

//
// Utility functions.
//

function ReadU64(Addr) {
    let Value = null;
    try {
        Value = host.memory.readMemoryValues(
           Addr, 1, 8
        )[0];
    } catch(e) {
    }

    return Value;
}

function ReadU32(Addr) {
    let Value = null;
    try {
        Value = host.memory.readMemoryValues(
            Addr, 1, 4
        )[0];
    } catch(e) {
    }

    return Value;
}

function ReadString(Addr) {
    let Value = null;
    try {
        Value = host.memory.readString(Addr);
    } catch(e) {
    }

    return Value;
}

function ReadWideString(Addr) {
    let Value = null;
    try {
        Value = host.memory.readWideString(Addr);
    } catch(e) {
    }

    return Value;
}

function Disassemble(Addr) {
    const Control = host.namespace.Debugger.Utility.Control;
    const Lines = Array.from(Control.ExecuteCommand(
        'u ' + Addr.toString(16) + ' l2')
    );

    const Disass = [];
    for(const Line of Lines) {

        //
        // Skip everything that doesn't start by an address.
        //

        if(Line.match(/^[0-9a-f`]+ /i) == null) {
            continue;
        }

        //
        // Extracts what follows the address.
        //

        const Match = Line.match(/^[0-9a-f`]+ [0-9a-f]+ [ ]+(.+)$/i);
        Disass.push(Match[1]);
    }

    return Disass.join(' ; ');
}

function FormatU64(Addr) {
    return '0x' + Addr.toString(16).padStart(16, '0');
}

function FormatU32(Addr) {
    return '0x' + Addr.toString(16).padStart(8, '0');
}

//
// Initializion / global stuff.
//

let Initialized = false;
let ReadPtr = null;
let FormatPtr = null;
const VaSpace = [];

function HandleTTD() {
    const CurrentSession = host.currentSession;

    //
    // Grabs addressable chunks.
    //

    const CurrentThread = host.currentThread;
    const Position = CurrentThread.TTD.Position;
    const Chunks = CurrentSession.TTD.Data.Heap().Where(
        p => p.TimeStart.compareTo(Position) < 0 &&
            p.Action == 'Alloc'
    );

    for(const Chunk of Chunks) {
        VaSpace.push(new _Region(
            Chunk.Address,
            Chunk.Size,
            'Heap',
            'rw-'
        ));
    }

    //
    // Grabs virtual allocated memory regions.
    //

    const VirtualAllocs = CurrentSession.TTD.Calls(
        'kernelbase!VirtualAlloc'
    ).Where(
        p => p.TimeStart.compareTo(Position) < 0
    );

    for(const VirtualAlloc of VirtualAllocs) {
        VaSpace.push(new _Region(
            VirtualAlloc.ReturnValue,
            VirtualAlloc.Parameters[1],
            'VirtualAlloced',
            // XXX: figure out access
            'rw-'
        ));
    }

    //
    // Grabs mapped view regions.
    //

    const MapViewOfFiles = CurrentSession.TTD.Calls(
        'kernelbase!MapViewOfFile'
    ).Where(
        p => p.TimeStart.compareTo(Position) < 0
    );

    for(const MapViewOfFile of MapViewOfFiles) {
        VaSpace.push(new _Region(
            MapViewOfFile.ReturnValue,
            0x1000,
            'MappedView',
            // XXX: figure out access
            'rw-'
        ));
    }
}

function InitializeVASpace() {

    //
    // Enumerates the modules.
    //

    logln('Populating the VA space with modules..');
    const CurrentProcess = host.currentProcess;
    for(const Module of CurrentProcess.Modules) {
        VaSpace.push(new _Region(
            Module.BaseAddress,
            Module.Size,
            'Image ' + Module.Name,
            'r-x'
        ));
    }

    //
    // Enumerates the TEBs and the stacks.
    //

    logln('Populating the VA space with TEBs & thread stacks..');
    for(const Thread of CurrentProcess.Threads) {
        const Teb = Thread.Environment.EnvironmentBlock;

        //
        // TEB!
        //

        VaSpace.push(new _Region(
            Teb.address,
            Teb.targetType.size,
            'Teb of ' + Thread.Id.toString(16),
            'rw-'
        ));

        //
        // Stacks!
        //

        const StackBase = Teb.NtTib.StackBase.address;
        const StackLimit = Teb.NtTib.StackLimit.address;
        VaSpace.push(new _Region(
            StackLimit,
            StackBase.subtract(StackLimit),
            'Stack',
            'rw-'
        ));
    }

    //
    // Get the PEB.
    //

    logln('Populating the VA space with the PEB..');
    const Peb = CurrentProcess.Environment.EnvironmentBlock;
    VaSpace.push(new _Region(
        Peb.address,
        Peb.targetType.size,
        'Peb',
        'rw-'
    ));

    //
    // If we have a TTD target, let's do some more work.
    //

    const CurrentSession = host.currentSession;
    const IsTTD = CurrentSession.Attributes.Target.IsTTDTarget
    if(IsTTD) {
        HandleTTD();
    }
}

function InitializeWrapper(Funct) {
    return Arg => {
        if(!Initialized) {
            const CurrentSession = host.currentSession;

            //
            // Initialize the ReadPtr function according to the PointerSize.
            //

            const PointerSize = CurrentSession.Attributes.Machine.PointerSize;
            ReadPtr = PointerSize.compareTo(8) == 0 ? ReadU64 : ReadU32;
            FormatPtr = PointerSize.compareTo(8) == 0 ? FormatU64 : FormatU32;

            //
            // Initialize the VA map.
            //

            InitializeVASpace();

            //
            // One time initialization!
            //

            Initialized = true;
        }

        //
        // Once initialization is done, call into the function.
        //

        return Funct(Arg);
    };
}


//
// The meat!
//

class _Region {
    constructor(BaseAddress, Size, Name, Properties) {
        this.Name = Name;
        this.BaseAddress = BaseAddress;
        this.EndAddress = this.BaseAddress.add(Size);
        this.Size = Size;
        this.Executable = false;
        this.Readable = false;
        if(Properties.indexOf('x') != -1) {
            this.Executable = true;
        }

        if(Properties.indexOf('r') != -1) {
            this.Readable = true;
        }
    }

    In(Addr) {
        const InBounds = Addr.compareTo(this.BaseAddress) >= 0 &&
            Addr.compareTo(this.EndAddress) < 0;
        return InBounds;
    }

    toString() {
        const Prop = [
            this.Readable ? 'r' : '-',
            '-',
            this.Executable ? 'e' : '-'
        ];

        return this.Name + ' ' + Prop.join('');
    }
}

function AddressToRegion(Addr) {

    //
    // Maps the address space with VA regions.
    //

    return VaSpace.find(
        p => p.In(Addr)
    );
}

class _ChainEntry {
    constructor(Addr, Value) {
        this.Addr = Addr;
        this.Value = Value;
        this.AddrRegion = AddressToRegion(this.Addr);
        this.ValueRegion = AddressToRegion(this.Value);
        if(this.ValueRegion == undefined) {
            this.Name = 'Unknown';
        } else {

            //
            // Just keep the file name and strips off the path.
            //

            this.Name = this.ValueRegion.Name;
            this.Name = this.Name.substring(this.Name.lastIndexOf('\\') + 1);
        }
        this.Last = false;
    }

    toStringLast() {
    }

    Equals(Entry) {
        return this.Addr.compareTo(Entry.Addr) == 0;
    }

    toString() {
        const S = FormatPtr(this.Value) + ' (' + this.Name + ')';
        if(!this.Last || this.AddrRegion == undefined) {
            return S;
        }

        if(this.AddrRegion.Executable) {
            return Disassemble(this.Addr);
        }

        if(this.AddrRegion.Readable) {

            //
            // Maybe it points on a unicode / ascii string?
            //

            const Ansi = ReadString(this.Addr);
            const IsPrintable = p => {
                return p != null &&
                    // XXX: ugly AF.
                    p.match(/^[a-z0-9!"#$%&'()*+,/\\.:;<=>?@\[\] ^_`{|}~-]+$/i) != null &&
                    p.length > 5
            };

            if(IsPrintable(Ansi)) {
                return Ansi;
            }

            const Wide = ReadWideString(this.Addr);
            if(IsPrintable(Wide)) {
                return Wide;
            }
        }

        //
        // If we didn't find something better, fallback to the regular
        // output.
        //

        return S;
    }
}

class _Chain {
    constructor(Addr) {
        this.__Entries = [];
        this.__HasCycle = false;
        this.__Addr = Addr;
        while(this.FollowPtr()) { };
        this.__Length = this.__Entries.length;

        //
        // Tag the last entry as 'last'.
        //

        if(this.__Length >= 1) {
            this.__Entries[this.__Length - 1].Last = true;
        }
    }

    FollowPtr() {

        //
        // Attempt to follow the pointer.
        //

        const Value = ReadPtr(this.__Addr);
        if(Value == null) {

            //
            // We are done following pointers now!
            //

            return false;
        }

        //
        // Let's build an entry and evaluate what we want to do with it.
        //

        const Entry = new _ChainEntry(this.__Addr, Value);
        if(this.__Entries.find(p => p.Equals(Entry))) {

            //
            // If we have seen this Entry before, it means there's a cycle
            // and we will stop there.
            //

            this.__HasCycle = true;
            return false;
        }

        //
        // This Entry is of interest, so let's add it in our list.
        //

        this.__Entries.push(Entry);
        this.__Addr = Value;
        return true;
    }

    toString() {
        if(this.__Entries.length == 0) {
            return '';
        }

        //
        // Iterate over the chain.
        //

        let S = this.__Entries.join(' -> ');

        //
        // Add a little something if we have a cycle so that the user knows.
        //

        if(this.__HasCycle) {
            S += ' [...]';
        }

        return S;
    }

    *[Symbol.iterator]() {
        for(const Entry of this.__Entries) {
            yield Entry;
        }
    }
}

function CreateChain(Addr) {
    return new _Chain(Addr);
}

function Telescope(Addr) {
    if(Addr == undefined) {
        logln('!telescope <addr>');
        return;
    }

    const CurrentSession = host.currentSession;
    const Lines = DefaultNumberOfLines;
    const PointerSize = CurrentSession.Attributes.Machine.PointerSize;
    const FormatOffset = p => '0x' + p.toString(16).padStart(4, '0');

    for(let Idx = 0; Idx < Lines; Idx++) {
        const Offset = PointerSize.multiply(Idx);
        const CurAddr = Addr.add(Offset);
        const Chain = CreateChain(CurAddr);
        const Header = FormatPtr(CurAddr) + '|+' + FormatOffset(Offset);
        logln(Header + ': ' + Chain.toString());
    }
}

function initializeScript() {
    return [
        new host.apiVersionSupport(1, 3),
        new host.functionAlias(
            InitializeWrapper(Telescope),
            'telescope'
        ),
        new host.functionAlias(
            InitializeWrapper(CreateChain),
            'createchain'
        )
    ];
}
