// Axel '0vercl0k' Souchet - Dec 2017

"use strict";

class ProcessModelParent {
    get DiaryOfAReverseEngineer() {
        return 'hello from ' + this.Name;
    }
}

function initializeScript() {
    return [new host.namedModelParent(
        ProcessModelParent,
        'Debugger.Models.Process'
    )];
}