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
}

function invokeScript() {
    let Control = host.namespace.Debugger.Utility.Control;
    let Regs = host.currentThread.Registers.User;
    let CurrentProcess = host.currentProcess;
    let BreakpointAlreadySet = CurrentProcess.Debug.Breakpoints.Any(
        c => c.OffsetExpression == 'ntdll!RtlAllocateHeap+0x0'
    );

    if(BreakpointAlreadySet == false) {
        let Bp = Control.SetBreakpointAtOffset('RtlAllocateHeap', 0, 'ntdll');
        Bp.Command = '.echo doare; dx @$scriptContents.handle_bp(); gc';
    } else {
        logln('Breakpoint already set.');
    }
    logln('Press "g" to run the target.');
    // let Lines = Control.ExecuteCommand('gc');
    // for(let Line of Lines) {
    //     logln('Line: ' + Line);
    // }
}
