// Axel '0vercl0k' Souchet - Dec 2017

"use strict";

class Attribute {
    constructor(Process, Name, Value) {
        this.__process = Process;
        this.Name = Name;
        this.Value = Value;
    }

    toString() {
        let S = 'Process: ' + this.__process.Name + ', ';
        S += 'Name: ' + this.Name + ', ';
        S += 'Value: ' + this.Value;
        return S;
    }
}

class Attributes {
    constructor() {
        this.__attrs = [];
    }

    push(Attr) {
        this.__attrs.push(Attr);
    }

    *[Symbol.iterator]() {
        for (let Attr of this.__attrs) {
            yield Attr;
        }
    }

    toString() {
        return 'Attributes';
    }
}

class Sub {
    constructor(Process) {
        this.__process = Process;
    }

    get SubFoo() {
        return 'SubFoo from ' + this.__process.Name;
    }

    get SubBar() {
        return 'SubBar from ' + this.__process.Name;
    }

    get Attributes() {
        let Attrs = new Attributes();
        Attrs.push(new Attribute(this.__process, 'attr0', 'value0'));
        Attrs.push(new Attribute(this.__process, 'attr1', 'value0'));
        return Attrs;
    }

    toString() {
        return 'Sub module';
    }
}

class DiaryOfAReverseEngineer {
    constructor(Process) {
        this.__process = Process;
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

    get Sub() {
        return new Sub(this.__process);
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
