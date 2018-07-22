// Axel '0vercl0k' Souchet - 24-June-2018
'use strict';

const logln = p => host.diagnostics.debugLog(p + '\n');
const JSVAL_TAG_SHIFT = host.Int64(47);
const JSVAL_PAYLOAD_MASK = host.Int64(1).bitwiseShiftLeft(JSVAL_TAG_SHIFT.add(1)).subtract(1);
const CLASS_NON_NATIVE = host.Int64(0x40000);
const FLAG_DELEGATE = host.Int64(8);

const JSVAL_TYPE_DOUBLE = host.Int64(0x1fff0);
const JSVAL_TYPE_INT32 = host.Int64(0x1fff1);
const JSVAL_TYPE_BOOLEAN = host.Int64(0x1fff2);
const JSVAL_TYPE_UNDEFINED = host.Int64(0x1fff3);
const JSVAL_TYPE_NULL = host.Int64(0x1fff4);
const JSVAL_TYPE_MAGIC = host.Int64(0x1fff5);
const JSVAL_TYPE_STRING = host.Int64(0x1fff6);
const JSVAL_TYPE_SYMBOL = host.Int64(0x1fff7);
const JSVAL_TYPE_PRIVATE_GCTHING = host.Int64(0x1fff8);
const JSVAL_TYPE_BIGINT = host.Int64(0x1fff9);
const JSVAL_TYPE_OBJECT = host.Int64(0x1fffc);

const INLINE_CHARS_BIT = host.Int64(1 << 3);
const LATIN1_CHARS_BIT = host.Int64(1 << 6);

const JSID_TYPE_MASK = host.Int64(0x7);
const JSID_TYPE_STRING = host.Int64(0x0);
const JSID_TYPE_INT = host.Int64(0x1);
const JSID_TYPE_VOID = host.Int64(0x2);
const JSID_TYPE_SYMBOL = host.Int64(0x4);

function read_u64(addr) {
    return host.memory.readMemoryValues(addr, 1, 8)[0];
}

function heapslot_to_objectelements(Addr) {
    // static ObjectElements* fromElements(HeapSlot* elems) {
    //  return reinterpret_cast<ObjectElements*>(uintptr_t(elems) - sizeof(ObjectElements));
    // }
    const ObjectElementsSize = host.getModuleType('js.exe', 'js::ObjectElements').size;
    const ObjectElements = host.createPointerObject(
        Addr.subtract(ObjectElementsSize),
        'js.exe',
        'js::ObjectElements*'
    );

    return ObjectElements;
}

function printable(Byte) {
    return Byte >= 0x20 && Byte <= 0x7e;
}

function byte_to_str(Byte) {
    if(printable(Byte)) {
        return String.fromCharCode(Byte);
    }

    return '\\x' + Byte.toString(16).padStart(2, '0');
}

function jsid_is_int(Propid) {
    const Bits = Propid.value.asBits;
    return Bits.bitwiseAnd(JSID_TYPE_MASK).compareTo(JSID_TYPE_INT) == 0;
}

function jsid_is_string(Propid) {
    const Bits = Propid.value.asBits;
    return Bits.bitwiseAnd(JSID_TYPE_MASK).compareTo(JSID_TYPE_STRING) == 0;
}

function get_property_from_shape(Shape) {
    const Propid = Shape.propid_;
    if(jsid_is_int(Propid)) {
        return Propid.value.asBits.bitwiseShiftRight(1);
    }

    if(jsid_is_string(Propid)) {
        return new __JSString(Propid.value.asBits);
    }

    // XXX: todo
}

function jsvalue_to_instance(Addr) {
    const JSValue = new __JSValue(Addr);
    const Types = {
        [JSVAL_TYPE_INT32] : __JSInt32,
        [JSVAL_TYPE_STRING] : __JSString,
        [JSVAL_TYPE_UNDEFINED] : __JSUndefined,
        [JSVAL_TYPE_BOOLEAN] : __JSBoolean,
        [JSVAL_TYPE_NULL] : __JSNull,
        [JSVAL_TYPE_OBJECT] : __JSObject
    };

    if(!Types.hasOwnProperty(JSValue.Tag)) {
        return 'Dunno';
    }

    const Type = Types[JSValue.Tag];
    return new Type(JSValue.Payload);
}

class __JSNull {
    constructor(Addr) {
    }

    toString() {
        return 'null';
    }
}

class __JSUndefined {
    constructor(Addr) {
    }

    toString() {
        return 'undefined';
    }
}

class __JSBoolean {
    constructor(Addr) {
        this._Value = Addr.compareTo(1) == 0 ? true : false;
    }

    toString() {
        return this._Value.toString();
    }
}

class __JSInt32 {
    constructor(Addr) {
        this._Value = Addr.bitwiseAnd(0xffffffff);
    }

    toString() {
        return '0x' + this._Value.toString(16);
    }
}

class __JSString {
    constructor(Addr) {
        this._Obj = host.createPointerObject(
            Addr,
            'js.exe',
            'JSString*'
        );
        /*
         * The Flags Word
         *
         * The flags word stores both the string's type and its character encoding.
         *
         * If LATIN1_CHARS_BIT is set, the string's characters are stored as Latin1
         * instead of TwoByte. This flag can also be set for ropes, if both the
         * left and right nodes are Latin1. Flattening will result in a Latin1
         * string in this case.
         */
        const Flags = this._Obj.d.u1.flags;
        const IsLatin1 = Flags.bitwiseAnd(LATIN1_CHARS_BIT).compareTo(0) != 0;
        const IsInline = Flags.bitwiseAnd(INLINE_CHARS_BIT).compareTo(0) != 0;
        let Address = null;
        if(IsInline) {

            //
            // inlineStorageLatin1 and inlineStorageTwoByte are in a union and
            // as a result are at the same address
            //

            Address = this._Obj.d.inlineStorageLatin1.address;
        } else {

            //
            // Same as above with nonInlineStorageLatin1 and nonInlineStorageTwoByte.
            //

            Address = this._Obj.d.s.u2.nonInlineCharsLatin1.address;
        }

        let Length = this._Obj.d.u1.length;
        if(!IsLatin1) {
            Length *= 2;
        }

        this._String = Array.from(host.memory.readMemoryValues(
            Address,
            Length,
            1
        )).map(
            p => byte_to_str(p)
        ).join('');
    }

    toString() {
        return "'" + this._String + "'";
    }
}

class __JSValue {
    constructor(Addr) {
        this._Addr = Addr;
        const Value = read_u64(this._Addr);
        this._Tag = Value.bitwiseShiftRight(JSVAL_TAG_SHIFT);
        this._Payload = Value.bitwiseAnd(JSVAL_PAYLOAD_MASK);
    }

    get Payload() {
        return this._Payload;
    }

    get Tag() {
        return this._Tag;
    }
}

class __JSArray {
    constructor(Addr) {
        this._Obj = host.createPointerObject(
            Addr,
            'js.exe',
            'js::ArrayObject*'
        );
        // XXX: why doesn't it work?
        // this.Obj.elements_.value.address
        this._Content = this._Obj.elements_.address;
        this._Header = heapslot_to_objectelements(this._Content);
        this._Length = this._Header.length;
        this._Capacity = this._Header.capacity;
    }

    get Length() {
        return this._Length;
    }

    get Capacity() {
        return this._Capacity;
    }

    toString() {
        const Max = 5;
        const Content = [];
        for(let Idx = 0; Idx < Math.min(Max, this.Length); ++Idx) {
            const Addr = this._Content.add(Idx * 8);
            Content.push(jsvalue_to_instance(Addr).toString());
        }
        return '[' + Content.join(', ') + (this.Length > Max ? ', ...' : '') + ']';
    }
}

class __JSFunction {
    constructor(Addr) {
        this._Obj = host.createPointerObject(
            Addr,
            'js.exe',
            'JSFunction*'
        );

        this._Atom = this._Obj.atom_.value.address;
        this._Name = '<anonymous>';
        if(this._Atom.compareTo(0) != 0) {
            this._Name = new __JSString(this._Atom).toString();
        }

        this._Name += '()';
    }

    toString() {
        return this._Name;
    }
}

class __JSObject {
    constructor(Addr) {
        this._Addr = Addr;
        this._Obj = host.createPointerObject(
            this._Addr,
            'js.exe',
            'JSObject*'
        );

        const Group = this._Obj.group_.value;
        this._ClassName = host.memory.readString(Group.clasp_.name);
    }

    toString() {
        if(this._ClassName == 'Object') {
            return '[Object]';
        }

        if(this._ClassName == 'Array') {
            return new __JSArray(this._Addr).toString();
        }

        return 'Dunno';
    }
}

function smdump_jsint32(Addr) {
    const Logger = function (Content) {
        logln(Addr.toString(16) + ': JSVAL_TYPE_INT32: ' + Content);
    };

    const JSInt32 = new __JSInt32(Addr);
    Logger(JSInt32);
}

function smdump_jsfunction(Addr) {
    const Logger = function (Content) {
        logln(Addr.toString(16) + ': js!JSFunction: ' + Content);
    };

    const JSFunction = new __JSFunction(Addr);
    Logger(JSFunction);
}

function smdump_jsarray(Addr) {
    const Logger = function (Content) {
        logln(Addr.toString(16) + ': js!js::ArrayObject: ' + Content);
    };

    const JSArray = new __JSArray(Addr);
    Logger('  Length: ' + JSArray.Length);
    Logger('Capacity: ' + JSArray.Capacity);
    Logger(' Content: ' + JSArray);
}

function smdump_jsstring(Addr) {
    const Logger = function (Content) {
        logln(Addr.toString(16) + ': js!JSString: ' + Content);
    };

    const JSString = new __JSString(Addr);
    Logger(JSString);
}

function smdump_jsobject(Addr) {
    /* JSObject.h
     * A JavaScript object.
     *
     * This is the base class for all objects exposed to JS script (as well as some
     * objects that are only accessed indirectly). Subclasses add additional fields
     * and execution semantics. The runtime class of an arbitrary JSObject is
     * identified by JSObject::getClass().
     *
     * The members common to all objects are as follows:
     *
     * - The |group_| member stores the group of the object, which contains its
     *   prototype object, its class and the possible types of its properties.
     *
     * - The |shapeOrExpando_| member points to (an optional) guard object that JIT
     *   may use to optimize. The pointed-to object dictates the constraints
     *   imposed on the JSObject:
     *      nullptr
     *          - Safe value if this field is not needed.
     *      js::Shape
     *          - All objects that might point |shapeOrExpando_| to a js::Shape
     *            must follow the rules specified on js::ShapedObject.
     *      JSObject
     *          - Implies nothing about the current object or target object. Either
     *            of which may mutate in place. Store a JSObject* only to save
     *            space, not to guard on.
     */
    const Logger = function (Content) {
        logln(Addr.toString(16) + ': js!JSObject: ' + Content);
    };

    const JSObject = host.createPointerObject(Addr, 'js.exe', 'JSObject*');
    const Group = JSObject.group_.value;
    const ClassName = host.memory.readString(Group.clasp_.name);
    const NonNative = Group.clasp_.flags.bitwiseAnd(CLASS_NON_NATIVE).compareTo(0) != 0;
    if(!NonNative) {
        const Shape = host.createPointerObject(
            JSObject.shapeOrExpando_.address,
            'js.exe',
            'js::Shape*'
        );
        const BaseShape = Shape.base_.value;
        const Delegate = BaseShape.flags.bitwiseAnd(FLAG_DELEGATE).compareTo(0) != 0;
        Logger('[Object ' + ClassName + ']');
        Logger('  Shape: ' + Shape.address.toString(16));

        let CurrentShape = Shape;
        while(CurrentShape.parent.value.address.compareTo(0) != 0) {
            Logger('    Property: ' + get_property_from_shape(CurrentShape));
            CurrentShape = CurrentShape.parent.value;
        }
    }

    if(ClassName == 'Function') {
        smdump_jsfunction(Addr);
    } else if(ClassName == 'Array') {
        smdump_jsarray(Addr);
    }
}

function smdump_jsundefined(Addr) {
    const Logger = function (Content) {
        logln(Addr.toString(16) + ': JSVAL_TYPE_UNDEFINED: ' + Content);
    };

    const Undefined = new __JSUndefined(Addr);
    Logger(Undefined);
}

function smdump_jsboolean(Addr) {
    const Logger = function (Content) {
        logln(Addr.toString(16) + ': JSVAL_TYPE_BOOLEAN: ' + Content);
    };

    const JSBoolean = new __JSBoolean(Addr);
    Logger(JSBoolean);
}

function smdump_jssymbol(Addr) {
    const Logger = function (Content) {
        logln(Addr.toString(16) + ': JSVAL_TYPE_SYMBOL: ' + Content);
    };

    // XXX: TODO!
    Logger(':(');
}

function smdump_jsdouble(Addr) {
    const Logger = function (Content) {
        logln(Addr.toString(16) + ': JSVAL_TYPE_DOUBLE: ' + Content);
    };

    // XXX: TODO!
    Logger(':(');
}

function smdump_jsnull(Addr) {
    const Logger = function (Content) {
        logln(Addr.toString(16) + ': JSVAL_TYPE_NULL: ' + Content);
    };

    Logger('null');
}

function smdump_jsvalue(Addr) {
    if(Addr == undefined) {
        logln('!smdump_jsvalue <jsvalue object addr>');
        return;
    }

    const dumps = {
        [JSVAL_TYPE_INT32] : smdump_jsint32,
        [JSVAL_TYPE_OBJECT] : smdump_jsobject,
        [JSVAL_TYPE_STRING] : smdump_jsstring,
        [JSVAL_TYPE_UNDEFINED] : smdump_jsundefined,
        [JSVAL_TYPE_BOOLEAN] : smdump_jsboolean,
        [JSVAL_TYPE_SYMBOL] : smdump_jssymbol,
        [JSVAL_TYPE_DOUBLE] : smdump_jsdouble,
        [JSVAL_TYPE_NULL] : smdump_jsnull
    };

    const JSValue = new __JSValue(Addr);
    dumps[JSValue.Tag](JSValue.Payload);
}

function initializeScript() {
    return [
        new host.apiVersionSupport(1, 2),
        new host.functionAlias(
            smdump_jsvalue,
            'smdump_jsvalue'
        ), new host.functionAlias(
            smdump_jsobject,
            'smdump_jsobject'
        )
    ];
}
