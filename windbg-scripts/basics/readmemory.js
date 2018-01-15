// Axel '0vercl0k' Souchet - Dec 2017

"use strict";

let logln = function (e) {
    host.diagnostics.debugLog(e + '\n');
}

function read_u64(addr) {
    return host.memory.readMemoryValues(addr, 1, 8)[0];
}

function invokeScript() {
    let Regs = host.currentThread.Registers.User;
    let a = read_u64(Regs.rsp);
    logln(a.toString(16));
    try {
        read_u64(0xdeadbeef);
    } catch(e) {
        logln(e);
    }
    let WideStr = host.currentProcess.Environment.EnvironmentBlock.ProcessParameters.ImagePathName.Buffer;
    logln(host.memory.readWideString(WideStr));
    let WideStrAddress = WideStr.address;
    logln(host.memory.readWideString(WideStrAddress));
}
