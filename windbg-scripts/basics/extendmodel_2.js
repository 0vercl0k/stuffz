// Axel '0vercl0k' Souchet - Dec 2017

"use strict";

class DiaryOfAReverseEngineer {
    constructor(Process) {
        this.process = Process;
    }

    get Foo() {
        return 'Foo from ' + this.process.Name;
    }

    get Bar() {
        return 'Bar from ' + this.process.Name;
    }

    Add(a, b) {
        return a + b;
    }
}

class ProcessModelParent {
    get DiaryOfAReverseEngineer() {
        return new DiaryOfAReverseEngineer(this);
    }
}

function initializeScript() {
    return [new host.namedModelParent(
        ProcessModelParent,
        'Debugger.Models.Process'
    )];
}