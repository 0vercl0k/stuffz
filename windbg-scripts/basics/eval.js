// Axel '0vercl0k' Souchet - Dec 2017

"use strict";

let logln = function (e) {
    host.diagnostics.debugLog(e + '\n');
}

function invokeScript() {
    let Control = host.namespace.Debugger.Utility.Control;
    for(let Line of Control.ExecuteCommand('kp')) {
        logln('Line: ' + Line);
    }
}
