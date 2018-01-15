// Axel '0vercl0k' Souchet - Dec 2017

"use strict";

class DiaryOfAReverseEngineer {
    constructor(Process) {
        this.__process = process;
    }

    get Foo() {
        return 'Foo from ' + this.__process.Name;
    }

    get Bar() {
        return 'Bar from ' + this.__process.Name;
    }

    Add(a, b) {
        return a + b;
    }

    toString() {
        return 'Diary of a reverse-engineer';
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