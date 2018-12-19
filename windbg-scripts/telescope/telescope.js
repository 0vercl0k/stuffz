// Axel '0vercl0k' Souchet - 7th December 2018

'use strict';

const log = host.diagnostics.debugLog;
const logln = p => host.diagnostics.debugLog(p + '\n');

//
// Config variables.
//

// This is the number of lines the !telescope command displays.
const DefaultNumberOfLines = 10;

// This is the number of instructions to disassemble when a code pointer is encountered.
const DefaultNumberOfInstructions = 3;

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

function ReadU16(Addr) {
    let Value = null;
    try {
        Value = host.memory.readMemoryValues(
            Addr, 1, 2
        )[0];
    } catch(e) {
    }

    return Value;
}

function ReadString(Addr, MaxLength) {
    let Value = null;
    try {
        Value = host.memory.readString(Addr);
    } catch(e) {
        return null;
    }

    if(Value.length > MaxLength) {
        return Value.substr(0, MaxLength);
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
    const Code = host.namespace.Debugger.Utility.Code;
    const Disassembler = Code.CreateDisassembler();
    const Instrs = Array.from(Disassembler.DisassembleInstructions(Addr).Take(
        DefaultNumberOfInstructions
    ));

    return Instrs.map(

        //
        // Clean up the assembly.
        // Turn the below:
        //   'mov     rbx,qword ptr [00007FF8D3525660h] ; test    rbx,rbx ; je     00007FF8D34FC2EB'
        // Into:
        //   'mov rbx,qword ptr [00007FF8D3525660h] ; test rbx,rbx ; je 00007FF8D34FC2EB'
        //

        p => p.toString().replace(/[ ]+/g, ' ')
    ).join(' ; ');
}

function FormatU64(Addr) {
    return '0x' + Addr.toString(16).padStart(16, '0');
}

function FormatU32(Addr) {
    return '0x' + Addr.toString(16).padStart(8, '0');
}

function BitSet(Value, Bit) {
    return Value.bitwiseAnd(Bit).compareTo(0) != 0;
}

//
// Initialization / global stuff.
//

let Initialized = false;
let ReadPtr = null;
let FormatPtr = null;
let IsTTD = false;
let IsUser = false;
let IsKernel = false;
let VaSpace = [];

function *SectionHeaders(BaseAddress) {
    if(IsKernel && ReadU32(BaseAddress) == null) {

        //
        // If we can't read the module, then..bail :(.
        // XXX: Fix this? Session space? Paged out?
        //

        logln('Cannot read ' + BaseAddress.toString(16) + ', skipping.');
        return;
    }

    // 0:000> dt _IMAGE_DOS_HEADER e_lfanew
    //   +0x03c e_lfanew : Int4B
    const NtHeaders = BaseAddress.add(ReadU32(BaseAddress.add(0x3c)));
    // 0:000> dt _IMAGE_NT_HEADERS64 FileHeader
    //    +0x004 FileHeader : _IMAGE_FILE_HEADER
    // 0:000> dt _IMAGE_FILE_HEADER NumberOfSections SizeOfOptionalHeader
    //    +0x002 NumberOfSections : Uint2B
    //    +0x010 SizeOfOptionalHeader : Uint2B
    const NumberOfSections = ReadU16(NtHeaders.add(0x4 + 0x2));
    const SizeOfOptionalHeader = ReadU16(NtHeaders.add(0x4 + 0x10));
    // 0:000> dt _IMAGE_NT_HEADERS64 OptionalHeader
    //   +0x018 OptionalHeader : _IMAGE_OPTIONAL_HEADER64
    const OptionalHeader = NtHeaders.add(0x18);
    const SectionHeaders = OptionalHeader.add(SizeOfOptionalHeader);
    // 0:000> ?? sizeof(_IMAGE_SECTION_HEADER)
    // unsigned int64 0x28
    const SizeofSectionHeader = 0x28;
    for(let Idx = 0; Idx < NumberOfSections; Idx++) {
        const SectionHeader = SectionHeaders.add(
            Idx.multiply(SizeofSectionHeader)
        );
        // 0:000> dt _IMAGE_SECTION_HEADER Name
        //    +0x000 Name             : [8] UChar
        const Name = ReadString(SectionHeader, 8);
        // 0:000> dt _IMAGE_SECTION_HEADER VirtualAddress
        //    +0x00c VirtualAddress : Uint4B
        const Address = BaseAddress.add(
            ReadU32(SectionHeader.add(0xc))
        );
        // 0:000> dt _IMAGE_SECTION_HEADER SizeOfRawData
        //    +0x08 Misc : Uint4B
        // XXX: Take care of alignment?
        const VirtualSize = ReadU32(SectionHeader.add(0x08));
        // 0:000> dt _IMAGE_SECTION_HEADER Characteristics
        //    +0x024 Characteristics : Uint4B
        const Characteristics = ReadU32(SectionHeader.add(0x24));
        const Properties = [
            '-',
            '-',
            '-'
        ];

        // The section can be read.
        const IMAGE_SCN_MEM_READ = host.Int64(0x40000000);
        if(BitSet(Characteristics, IMAGE_SCN_MEM_READ)) {
            Properties[0] = 'r';
        }

        if(IsKernel) {
            const IMAGE_SCN_MEM_DISCARDABLE = host.Int64(0x2000000);
            if(BitSet(Characteristics, IMAGE_SCN_MEM_DISCARDABLE)) {
                Properties[0] = '-';
            }
        }

        // The section can be written to.
        const IMAGE_SCN_MEM_WRITE = host.Int64(0x80000000);
        if(Characteristics.bitwiseAnd(IMAGE_SCN_MEM_WRITE).compareTo(0) != 0) {
            Properties[1] = 'w';
        }

        // The section can be executed as code.
        const IMAGE_SCN_MEM_EXECUTE = host.Int64(0x20000000);
        if(Characteristics.bitwiseAnd(IMAGE_SCN_MEM_EXECUTE).compareTo(0) != 0) {
            Properties[2] = 'x';
        }

        yield new _Region(
            Address,
            VirtualSize,
            Name,
            Properties.join('')
        );
    }
}

function HandleTTD() {
    const CurrentSession = host.currentSession;

    //
    // Grab addressable chunks.
    //

    logln('Populating the VA space with TTD.Data.Heap..');
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
    // Grab virtual allocated memory regions.
    //

    logln('Populating the VA space with VirtualAllocated regions..');
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
            // XXX: parse access
            'rw-'
        ));
    }

    //
    // Grab mapped view regions.
    //

    logln('Populating the VA space with MappedViewOfFile regions..');
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
            // XXX: parse access
            'rw-'
        ));
    }
}

function HandleUser() {

    //
    // Enumerate the modules.
    //

    logln('Populating the VA space with modules..');
    const CurrentProcess = host.currentProcess;
    for(const Module of CurrentProcess.Modules) {

        //
        // Iterate over the section headers of the module.
        //

        for(const Section of SectionHeaders(Module.BaseAddress)) {
            VaSpace.push(new _Region(
                Section.BaseAddress,
                Section.Size,
                'Image ' + Module.Name + ' (' + Section.Name + ')',
                Section.Properties
            ));
        }

        //
        // Add a catch all in case a pointer points inside the PE but not
        // inside any sections (example of this is the PE header).
        //

        VaSpace.push(new _Region(
            Module.BaseAddress,
            Module.Size,
            'Image ' + Module.Name,
            'r--'
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
}

function HandleKernel() {

    //
    // Enumerate the kernel modules.
    //

    logln('Populating the VA space with kernel modules..');
    const CurrentSession = host.currentSession;
    const SystemProcess = CurrentSession.Processes.First(
        p => p.Name == 'System'
    );

    const MmUserProbeAddress = ReadPtr(
        host.getModuleSymbolAddress('nt', 'MmUserProbeAddress')
    );

    const KernelModules = SystemProcess.Modules.Where(
        p => p.BaseAddress.compareTo(MmUserProbeAddress) > 0
    );

    for(const Module of KernelModules) {

        //
        // Iterate over the section headers of the module.
        //

        for(const Section of SectionHeaders(Module.BaseAddress)) {
            VaSpace.push(new _Region(
                Section.BaseAddress,
                Section.Size,
                'Driver ' + Module.Name + ' (' + Section.Name + ')',
                Section.Properties
            ));
        }

        //
        // Add a catch all in case a pointer points inside the PE but not
        // inside any sections (example of this is the PE header).
        //

        VaSpace.push(new _Region(
            Module.BaseAddress,
            Module.Size,
            'Driver ' + Module.Name,
            'r--'
        ));
    }
}

function InitializeVASpace() {
    if(IsUser) {
        HandleUser();
    }

    if(IsTTD) {

        //
        // If we have a TTD target, let's do some more work.
        //

        HandleTTD();
    }

    if(IsKernel) {
        HandleKernel();
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
            const TargetAttributes = CurrentSession.Attributes.Target;
            IsTTD = TargetAttributes.IsTTDTarget;
            IsUser = TargetAttributes.IsUserTarget;
            IsKernel = TargetAttributes.IsKernelTarget;

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
        this.Properties = Properties;
        this.Executable = false;
        this.Readable = false;
        this.Writeable = false;
        if(Properties.indexOf('r') != -1) {
            this.Readable = true;
        }

        if(Properties.indexOf('w') != -1) {
            this.Writeable = true;
        }

        if(Properties.indexOf('x') != -1) {
            this.Executable = true;
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
            this.Writeable ? 'w' : '-',
            this.Executable ? 'x' : '-'
        ];

        return this.Name + ' ' + Prop.join('');
    }
}

function AddressToRegion(Addr) {

    //
    // Map the address space with VA regions.
    //

    const Hits = VaSpace.filter(
        p => p.In(Addr)
    );

    //
    // Now, let's get the most precise region information by ordering
    // the hits by size.
    //

    const OrderedHits = Hits.sort(
        p => p.Size
    );

    //
    // Return the most precise information we have!
    //

    return OrderedHits[0];
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
        const DoesEntryExist = this.__Entries.find(
            p => p.Equals(Entry)
        );

        if(DoesEntryExist) {

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

    //
    // Initialize the VA space.
    //

    InitializeVASpace();

    const Chain = new _Chain(Addr);
    VaSpace = [];
    return Chain;
}

function Telescope(Addr) {
    if(Addr == undefined) {
        logln('!telescope <addr>');
        return;
    }

    //
    // Initialize the VA space.
    //

    InitializeVASpace();

    const CurrentSession = host.currentSession;
    const Lines = DefaultNumberOfLines;
    const PointerSize = CurrentSession.Attributes.Machine.PointerSize;
    const FormatOffset = p => '0x' + p.toString(16).padStart(4, '0');

    for(let Idx = 0; Idx < Lines; Idx++) {
        const Offset = PointerSize.multiply(Idx);
        const CurAddr = Addr.add(Offset);
        const Chain = new _Chain(CurAddr);
        const Header = FormatPtr(CurAddr) + '|+' + FormatOffset(Offset);
        logln(Header + ': ' + Chain.toString());
    }

    VaSpace = [];
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
