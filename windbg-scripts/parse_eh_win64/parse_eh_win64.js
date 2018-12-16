// Axel '0vercl0k' Souchet - Dec 2017

"use strict";

let log = host.diagnostics.debugLog;
let logln = function (e) {
    host.diagnostics.debugLog(e + '\n');
};

function read_u32(addr) {
    return host.memory.readMemoryValues(addr, 1, 4)[0];
}

function read_u8(addr) {
    return host.memory.readMemoryValues(addr, 1, 1)[0];
}

class ScopeRecord {
    // 0:000> dt SCOPE_RECORD
    //   +0x000 BeginAddress     : Uint4B
    //   +0x004 EndAddress       : Uint4B
    //   +0x008 HandlerAddress   : Uint4B
    //   +0x00c JumpTarget       : Uint4B
    constructor(ScopeRecordAddress) {
        this.Begin = read_u32(ScopeRecordAddress);
        this.End = read_u32(ScopeRecordAddress.add(0x4));
        this.HandlerAddress = read_u32(ScopeRecordAddress.add(0x8));
        this.JumpTarget = read_u32(ScopeRecordAddress.add(0xc));
    }

    get IsTryFinally() {
        return this.JumpTarget.compareTo(0) == 0;
    }

    get HasFilter() {
        return this.IsTryFinally == false &&
            this.HandlerAddress.compareTo(1) != 0;
    }

    InBound(Begin, End) {
        return this.Begin.compareTo(Begin) >= 0 &&
            this.End.compareTo(End) < 0;
    }

    toString() {
        let S = '  __try {'
        S += this.Begin.toString(16) + ' -> ' + this.End.toString(16);
        S += '}';
        if (this.IsTryFinally == true) {
            S += ' __finally {';
            S += this.HandlerAddress.toString(16);
        } else {
            S += ' __except(';
            if (this.HasFilter == false) {
                S += 'EXCEPTION_EXECUTE_HANDLER';
            } else {
                S += this.HandlerAddress.toString(16) + '()';
            }
            S += ') {';
            S += this.JumpTarget.toString(16);
        }
        S += '}';
        return S;
    }
}

class Function {
    constructor(BaseAddress, EHHandler, Begin, End) {
        this.__BaseAddress = BaseAddress;
        this.EHHandlerRVA = EHHandler;
        this.EHHandler = BaseAddress.add(EHHandler);
        this.BeginRVA = Begin;
        this.EndRVA = End;
        this.Begin = BaseAddress.add(Begin);
        this.End = BaseAddress.add(End);
        this.ExceptionHandlers = [];
    }

    SetRecords(Records, KeepRVA = false) {
        this.ExceptionHandlers = Records;
        if (KeepRVA) {
            return;
        }

        for (let ExceptionHandler of this.ExceptionHandlers) {
            ExceptionHandler.Begin = ExceptionHandler.Begin.add(this.__BaseAddress);
            ExceptionHandler.End = ExceptionHandler.End.add(this.__BaseAddress);
            if (ExceptionHandler.JumpTarget.compareTo(0) != 0) {
                ExceptionHandler.JumpTarget = ExceptionHandler.JumpTarget.add(this.__BaseAddress);
            }
            if (ExceptionHandler.HandlerAddress.compareTo(1) != 0) {
                ExceptionHandler.HandlerAddress = ExceptionHandler.HandlerAddress.add(this.__BaseAddress);
            }
        }
    }

    toString() {
        let S = 'RVA:' + this.Begin.toString(16) + ' -> RVA:' + this.End.toString(16);
        S += ', ' + this.ExceptionHandlers.length + ' exception handlers';
        return S;
    }
}

function ParseCSpecificHandlerDatas(
    ScopeCount,
    ScopeRecords,
    Function
) {
    // 0:000> ?? sizeof(SCOPE_RECORD)
    // unsigned int64 0x10
    let Records = [];
    let ScopeSize = ScopeCount.multiply(0x10);
    for (let i = 0; i < ScopeSize; i += 0x10) {
        let CurrentScope = ScopeRecords.add(i);
        let Record = new ScopeRecord(CurrentScope);
        if (Record.InBound(Function.BeginRVA, Function.EndRVA) == false) {
            return [];
        }
        Records.push(Record);
    }
    return Records;
}

function ExtractExceptionHandlersForModule(
    BaseAddress,
    KeepRVA = false
) {
    let EHANDLER = 1;
    let IMAGE_DIRECTORY_ENTRY_EXCEPTION = 3;

    // 0:000> dt _IMAGE_DOS_HEADER e_lfanew
    //   +0x03c e_lfanew : Int4B
    let NtHeaders = BaseAddress.add(read_u32(BaseAddress.add(0x3c)));

    // 0:000> dt _IMAGE_NT_HEADERS64 OptionalHeader
    //   +0x018 OptionalHeader : _IMAGE_OPTIONAL_HEADER64
    // 0:000> dt _IMAGE_OPTIONAL_HEADER64 DataDirectory
    //   +0x070 DataDirectory : [16] _IMAGE_DATA_DIRECTORY
    // 0:000> dt _IMAGE_DATA_DIRECTORY
    //   +0x000 VirtualAddress   : Uint4B
    //   +0x004 Size             : Uint4B
    let EntryExceptionDirectory = NtHeaders.add(0x18 + 0x70 + (IMAGE_DIRECTORY_ENTRY_EXCEPTION * 8));
    let RuntimeFunctionEntry = BaseAddress.add(read_u32(EntryExceptionDirectory));
    let SizeOfDirectory = read_u32(EntryExceptionDirectory.add(4));
    let Functions = [];

    for (let i = 0; i < SizeOfDirectory; i += 0xC) {
        // 0:000> dt _IMAGE_RUNTIME_FUNCTION_ENTRY
        //   +0x000 BeginAddress     : Uint4B
        //   +0x004 EndAddress       : Uint4B
        //   +0x008 UnwindInfoAddress : Uint4B
        //   +0x008 UnwindData       : Uint4B
        // 0:000> ?? sizeof(_IMAGE_RUNTIME_FUNCTION_ENTRY)
        // unsigned int64 0xc
        let CurrentEntry = RuntimeFunctionEntry.add(i);
        let BeginAddress = read_u32(CurrentEntry);
        let EndAddress = read_u32(CurrentEntry.add(4));

        if (BeginAddress.compareTo(0) == 0 || EndAddress.compareTo(0) == 0) {
            continue;
        }

        // 0:000> dt UNWIND_INFO
        //   +0x000 Version          : Pos 0, 3 Bits
        //   +0x000 Flags            : Pos 3, 5 Bits
        //   +0x001 SizeOfProlog     : UChar
        //   +0x002 CountOfCodes     : UChar
        //   +0x003 FrameRegister    : Pos 0, 4 Bits
        //   +0x003 FrameOffset      : Pos 4, 4 Bits
        //   +0x004 UnwindCode       : [1] UNWIND_CODE
        let UnwindInfo = BaseAddress.add(read_u32(CurrentEntry.add(8)));
        let UnwindInfoFlags = read_u8(UnwindInfo).bitwiseShiftRight(3);
        if (UnwindInfoFlags.bitwiseAnd(EHANDLER).compareTo(0) == 0) {
            continue;
        }

        // 0:000> ?? sizeof(UNWIND_CODE)
        // unsigned int64 2
        let CountOfCodes = read_u8(UnwindInfo.add(2));
        // For alignment purposes, this array will always have an even number of entries,
        // with the final entry potentially unused (in which case the array will be one
        // longer than indicated by the count of unwind codes field).
        let AlignedCountOfCodes = (CountOfCodes + 1) & ~1;

        // 0:000> dt UNWIND_INFO_END
        //   +0x000 ExceptionHandler : Uint4B
        //   +0x004 ExceptionData    : Uint4B
        let UnwindInfoEnd = UnwindInfo.add(4 + (AlignedCountOfCodes * 2));
        let ExceptionHandler = read_u32(UnwindInfoEnd);

        // 0:000> dt SEH_SCOPE_TABLE
        //   +0x000 Count            : Uint4B
        //   +0x004 ScopeRecord      : [1] SCOPE_RECORD
        let ScopeTable = UnwindInfoEnd.add(4);
        let ScopeCount = read_u32(ScopeTable);
        if (ScopeCount == 0) {
            continue;
        }

        let Records = ScopeTable.add(4);
        let CurrentFunction = new Function(
            BaseAddress, ExceptionHandler,
            BeginAddress, EndAddress
        );
        Records = ParseCSpecificHandlerDatas(ScopeCount, Records, CurrentFunction);
        if (Records.length == 0) {
            continue;
        }

        CurrentFunction.SetRecords(Records, KeepRVA);
        Functions.push(CurrentFunction);
    }

    return Functions;
}

class ModelExceptionHandlers {
    constructor(Type, Inst) {
        this.__module = null;
        this.__process = null;
        if (Type == 'Module') {
            this.__module = Inst;
        } else {
            this.__process = Inst;
        }
        this.__handlers = null;
        // We do not parse the exception handlers information here
        // as this constructor is called everytime you do:
        //  dx @$curprocess
        // so we will only parse the information when the user asked for it.
    }

    __ExceptionHandlers(Modules) {
        let Handlers = [];
        for (let Module of Modules) {
            let Functions = ExtractExceptionHandlersForModule(Module.BaseAddress);
            for (let Function of Functions) {
                Handlers = Handlers.concat(Function.ExceptionHandlers);
            }
        }
        return Handlers;
    }

    *[Symbol.iterator]() {
        if (this.__handlers == null) {
            // Only parse the infornmation once everytine we query it.
            let Modules = [this.__module];
            if (this.__process != null) {
                Modules = this.__process.Modules;
            }
            this.__handlers = this.__ExceptionHandlers(Modules);
        }

        for (let Handler of this.__handlers) {
            yield Handler;
        }
    }

    toString() {
        return 'Exception handlers';
    }
}

class ModelFunctions {
    constructor(Type, Inst) {
        this.__module = null;
        this.__process = null;
        if (Type == 'Module') {
            this.__module = Inst;
        } else {
            this.__process = Inst;
        }
        this.__functions = null;
    }

    __Functions(Modules) {
        let Functions = [];
        for (let Module of Modules) {
            let CurrentFunctions = ExtractExceptionHandlersForModule(Module.BaseAddress);
            Functions = Functions.concat(CurrentFunctions);
        }
        return Functions;
    }

    *[Symbol.iterator]() {
        if (this.__functions == null) {
            this.__functions = [];
            let Modules = [this.__module];
            if (this.__process != null) {
                Modules = this.__process.Modules;
            }

            this.__functions = this.__Functions(Modules);
        }

        for (let Function of this.__functions) {
            yield Function;
        }
    }

    toString() {
        return 'Functions';
    }
}

class __ProcessModelExtension {
    get ExceptionHandlers() {
        return new ModelExceptionHandlers('Process', this);
    }

    get Functions() {
        return new ModelFunctions('Process', this);
    }
}

class __ModuleModelExtension {
    get ExceptionHandlers() {
        return new ModelExceptionHandlers('Module', this);
    }

    get Functions() {
        return new ModelFunctions('Module', this);
    }
}

function BangEHHandlers() {
    let Control = host.namespace.Debugger.Utility.Control;
    let CurrentThread = host.currentThread;
    let CurrentProcess = host.currentProcess;
    let Registers = CurrentThread.Registers.User;

    let ReturnAddresses = [Registers.rip];
    let Frames = CurrentThread.Stack.Frames;
    for (let Frame of Frames) {
        ReturnAddresses.push(Frame.Attributes.ReturnOffset);
    }

    logln(ReturnAddresses.length + ' stack frames, scanning for handlers...');
    let Functions = Array.from(CurrentProcess.Functions);
    for (let Entry of ReturnAddresses.entries()) {
        let FrameNumber = host.Int64(Entry[0]);
        let ReturnAddress = Entry[1];
        let Func = Functions.find(
            c => ReturnAddress.compareTo(c.Begin) >= 0 &&
                ReturnAddress.compareTo(c.End) < 0
        );

        if (Func == undefined) {
            continue;
        }

        let ExceptionHandlers = Array.from(Func.ExceptionHandlers);
        let ExceptionHandler = ExceptionHandlers.find(
            c => ReturnAddress.compareTo(c.Begin) >= 0 &&
                ReturnAddress.compareTo(c.End) < 0
        )

        if (ExceptionHandler == undefined) {
            continue;
        }

        let Filter = undefined;
        let EHHandler = Func.EHHandler;
        let Handler = ExceptionHandler.HandlerAddress;
        let Name = 'Finally';
        if (ExceptionHandler.IsTryFinally == false) {
            if (ExceptionHandler.HasFilter) {
                Filter = ExceptionHandler.HandlerAddress;
            }
            Handler = ExceptionHandler.JumpTarget;
            Name = ' Except';
        }

        let FormatAddress = function (Handler) {
            let S = Handler.toString(16) + ': ';
            S += Control.ExecuteCommand(
                'u ' + Handler.toString(16) + ' l1'
            ).First();
            return S;
        }

        logln('Frame ' + FrameNumber.toString(16) + ': EHHandler: ' + FormatAddress(EHHandler));
        logln('             ' + Name + ': ' + FormatAddress(Handler));
        if (Filter != undefined) {
            logln('              Filter: ' + FormatAddress(Filter));
        }
    }
}

function initializeScript() {
    return [
        new host.namedModelParent(
            __ProcessModelExtension,
            'Debugger.Models.Process'
        ),
        new host.namedModelParent(
            __ModuleModelExtension,
            'Debugger.Models.Module'
        ),
        new host.functionAlias(
            BangEHHandlers,
            'ehhandlers'
        )
    ];
}
