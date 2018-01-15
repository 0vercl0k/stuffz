// Axel '0vercl0k' Souchet - Dec 2017

"use strict";

let logln = function (e) {
    host.diagnostics.debugLog(e + '\n');
}

function handle_bp() {
    let Regs = host.currentThread.Registers.User;
    let Args = [Regs.rcx, Regs.rdx, Regs.r8];
    let ArgsS = Args.map(c => c.toString(16));
    let HeapHandle = ArgsS[0];
    let Flags = ArgsS[1];
    let Size = ArgsS[2];
    logln('RtlAllocateHeap: HeapHandle: ' + HeapHandle + ', Flags: ' + Flags + ', Size: ' + Size);
    if(Args[2].compareTo(0x100) > 0) {
        // stop execution if the allocation size is bigger than 0x100
        return true;
    }
    // keep the execution going if it's a small size
    return false;
}

function invokeScript() {
    let Control = host.namespace.Debugger.Utility.Control;
    let Regs = host.currentThread.Registers.User;
    let CurrentProcess = host.currentProcess;
    let HeapAlloc = host.getModuleSymbolAddress('ntdll', 'RtlAllocateHeap');
    let BreakpointAlreadySet = CurrentProcess.Debug.Breakpoints.Any(
        c => c.Address == HeapAlloc
    );
    if(BreakpointAlreadySet == false) {
        logln('RltAllocateHeap @ ' + HeapAlloc.toString(16));
        Control.ExecuteCommand('bp /w "@$scriptContents.handle_bp()" ' + HeapAlloc.toString(16));
    } else {
        logln('Breakpoint already set.');
    }
    logln('Press "g" to run the target.');
}
