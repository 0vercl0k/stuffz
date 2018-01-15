// Axel '0vercl0k' Souchet - Dec 2017

"use strict";

let logln = function (e) {
    host.diagnostics.debugLog(e + '\n');
}

function invokeScript() {
    let a = host.Int64(1337);
    let aplusone = a + 1;
    logln(aplusone.toString(16));
    let b = host.parseInt64('0xdeadbeefbaadc0de', 16);
    let bplusone = b.add(1);
    logln(bplusone.toString(16));
    let bplusonenothrow = b.convertToNumber() + 1;
    logln(bplusonenothrow);
    try {
        let bplusonethrow = b + 1;
    } catch(e) {
        logln(e);
    }
    logln(a.compareTo(1));
    logln(a.compareTo(1337));
    logln(a.compareTo(1338));
}
