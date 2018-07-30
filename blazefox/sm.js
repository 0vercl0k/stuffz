// Axel '0vercl0k' Souchet - 24-June-2018
'use strict';

const logln = p => host.diagnostics.debugLog(p + '\n');
const JSVAL_TAG_SHIFT = host.Int64(47);
const JSVAL_PAYLOAD_MASK = host.Int64(1).bitwiseShiftLeft(JSVAL_TAG_SHIFT).subtract(1);
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

const SLOT_MASK = host.Int64(0xffffff);
const FIXED_SLOTS_SHIFT = host.Int64(27);

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
    // XXX: expose a smdump_jsid
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
        [JSVAL_TYPE_OBJECT] : __JSObject,
        [JSVAL_TYPE_SYMBOL] : __JSSymbol
    };

    if(!Types.hasOwnProperty(JSValue.Tag)) {
        return 'Dunno';
    }

    const Type = Types[JSValue.Tag];
    return new Type(JSValue.Payload);
}

class __JSNull {
    toString() {
        return 'null';
    }
}

class __JSUndefined {
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
        this._Tag = this._Addr.bitwiseShiftRight(JSVAL_TAG_SHIFT);
        this._Payload = this._Addr.bitwiseAnd(JSVAL_PAYLOAD_MASK);
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
            const JSValue = read_u64(Addr);
            Content.push(jsvalue_to_instance(JSValue).toString());
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

class __JSSymbol {
    constructor(Addr) {
        this._Obj = host.createPointerObject(
            Addr,
            'js.exe',
            'js::Symbol*'
        );
    }

    toString() {
        const Desc = new __JSString(this._Obj.description_.address);
        return 'Symbol(' + Desc + ')';
    }
}

class __JSArrayBuffer {
    constructor(Addr) {
        this._Obj = host.createPointerObject(
            Addr,
            'js.exe',
            'js::ArrayBufferObject*'
        );

        const ArrayBufferObjectSize = host.getModuleType('js.exe', 'js::ArrayBufferObject').size;
        // static const uint8_t DATA_SLOT = 0;
        // static const uint8_t BYTE_LENGTH_SLOT = 1;
        const ByteLengthSlotAddr = Addr.add(ArrayBufferObjectSize).add(1 * 8);
        const ByteLengthSlot = read_u64(ByteLengthSlotAddr);
        this._ByteLength = new __JSInt32(ByteLengthSlot)._Value;
        // static const uint8_t FIRST_VIEW_SLOT = 2;
        // static const uint8_t FLAGS_SLOT = 3;
        const FlagsAddr = Addr.add(ArrayBufferObjectSize).add(3 * 8);
        const FlagsSlot = read_u64(FlagsAddr);
        this._Flags = new __JSInt32(FlagsSlot)._Value;
    }

    get Flags() {
        //  enum BufferKind {
        //      PLAIN               = 0, // malloced or inline data
        //      WASM                = 1,
        //      MAPPED              = 2,
        //      EXTERNAL            = 3,
        //      KIND_MASK           = 0x3
        //  };
        // enum ArrayBufferFlags {
        //     // The flags also store the BufferKind
        //     BUFFER_KIND_MASK    = BufferKind::KIND_MASK,
        //     DETACHED            = 0x4,
        //     // The dataPointer() is owned by this buffer and should be released
        //     // when no longer in use. Releasing the pointer may be done by freeing,
        //     // invoking a dereference callback function, or unmapping, as
        //     // determined by the buffer's other flags.
        //     //
        //     // Array buffers which do not own their data include buffers that
        //     // allocate their data inline, and buffers that are created lazily for
        //     // typed objects with inline storage, in which case the buffer points
        //     // directly to the typed object's storage.
        //     OWNS_DATA           = 0x8,
        //     // This array buffer was created lazily for a typed object with inline
        //     // data. This implies both that the typed object owns the buffer's data
        //     // and that the list of views sharing this buffer's data might be
        //     // incomplete. Any missing views will be typed objects.
        //     FOR_INLINE_TYPED_OBJECT = 0x10,
        //     // Views of this buffer might include typed objects.
        //     TYPED_OBJECT_VIEWS  = 0x20,
        //     // This PLAIN or WASM buffer has been prepared for asm.js and cannot
        //     // henceforth be transferred/detached.
        //     FOR_ASMJS           = 0x40
        // };
        const BufferKinds = {
            0 : 'PLAIN',
            1 : 'WASM',
            2 : 'MAPPED',
            3 : 'EXTERNAL'
        };

        const BufferKind = BufferKinds[this._Flags.bitwiseAnd(3).asNumber()];
        const ArrayBufferFlags = [
            'BufferKind(' + BufferKind + ')'
        ];

        if(this._Flags.bitwiseAnd(4).compareTo(0) != 0) {
            ArrayBufferFlags.push('DETACHED');
        }

        if(this._Flags.bitwiseAnd(8).compareTo(0) != 0) {
            ArrayBufferFlags.push('OWNS_DATA');
        }

        if(this._Flags.bitwiseAnd(0x10).compareTo(0) != 0) {
            ArrayBufferFlags.push('FOR_INLINE_TYPED_OBJECT');
        }

        if(this._Flags.bitwiseAnd(0x20).compareTo(0) != 0) {
            ArrayBufferFlags.push('TYPED_OBJECT_VIEWS');
        }

        if(this._Flags.bitwiseAnd(0x40).compareTo(0) != 0) {
            ArrayBufferFlags.push('FOR_ASMJS');
        }

        return ArrayBufferFlags.join(' | ');
    }

    get ByteLength() {
        return this._ByteLength;
    }

    toString() {
        return 'ArrayBuffer({ByteLength:' + this._ByteLength + ', ...})';
    }
}

class __JSTypedArray {
    constructor(Addr) {
        this._Obj = host.createPointerObject(
            Addr,
            'js.exe',
            'js::TypedArrayObject*'
        );

        const Group = this._Obj.group_.value;
        this._TypeName = host.memory.readString(Group.clasp_.name)
        const Sizes = {
            'Float64Array' : 8,
            'Float32Array' : 4,
            'Uint32Array' : 4,
            'Int32Aray' : 4,
            'Uint16Array' : 2,
            'Int16Array' : 2,
            'Uint8Array' : 1,
            'Uint8ClampedArray' : 1,
            'Int8Array' : 1
        };
        this._ElementSize = Sizes[this._TypeName];

        const TypedArrayObjectSize = host.getModuleType('js.exe', 'js::TypedArrayObject').size;
        // static const size_t BUFFER_SLOT = 0;
        // static const size_t LENGTH_SLOT = 1;
        const LengthSlotAddr = Addr.add(TypedArrayObjectSize).add(1 * 8);
        const LengthSlot = read_u64(LengthSlotAddr);
        this._Length = new __JSInt32(LengthSlot)._Value;
        this._ByteLength = this._Length * this._ElementSize;
        // static const size_t BYTEOFFSET_SLOT = 2;
        const ByteOffsetSlotAddr = Addr.add(TypedArrayObjectSize).add(2 * 8);
        const ByteOffsetSlot = read_u64(ByteOffsetSlotAddr);
        this._ByteOffset = new __JSInt32(ByteOffsetSlot)._Value;
        // static const size_t RESERVED_SLOTS = 3;
    }

    get Type() {
        return this._TypeName;
    }

    get ByteOffset() {
        return this._ByteOffset;
    }

    get ByteLength() {
        return this._ByteLength;
    }

    get Length() {
        return this._Length;
    }

    toString() {
        return this._TypeName + '({Length:' + this._Length + ', ...})';
    }
}

class __JSMap {
    // XXX: TODO
    toString() {
        return 'new Map(...)';
    }
}

class __JSObject {
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
    constructor(Addr) {
        this._Addr = Addr;
        this._Obj = host.createPointerObject(
            this._Addr,
            'js.exe',
            'JSObject*'
        );

        this._Properties = [];
        const Group = this._Obj.group_.value;
        this._ClassName = host.memory.readString(Group.clasp_.name);
        const NonNative = Group.clasp_.flags.bitwiseAnd(CLASS_NON_NATIVE).compareTo(0) != 0;
        if(NonNative) {
            return;
        }

        const Shape = host.createPointerObject(
            this._Obj.shapeOrExpando_.address,
            'js.exe',
            'js::Shape*'
        );

        const NativeObject = host.createPointerObject(Addr, 'js.exe', 'js::NativeObject*');

        if(this._ClassName == 'Array') {

            //
            // Optimization for 'length' property if 'Array' cf
            // js::ArrayObject::length / js::GetLengthProperty
            //

            const ObjectElements = heapslot_to_objectelements(NativeObject.elements_.address);
            this._Properties.push('length : ' + ObjectElements.length);
            return;
        }

        //
        // Walk the list of Shapes and get the property names
        //

        const Properties = {};
        let CurrentShape = Shape;
        while(CurrentShape.parent.value.address.compareTo(0) != 0) {
            const SlotIdx = CurrentShape.slotInfo.bitwiseAnd(SLOT_MASK).asNumber();
            Properties[SlotIdx] = get_property_from_shape(CurrentShape);
            CurrentShape = CurrentShape.parent.value;
        }


        //
        // Walk the slots to get the values now (check NativeGetPropertyInline/GetExistingProperty)
        //

        const NativeObjectTypeSize = host.getModuleType('js.exe', 'js::NativeObject').size;
        const NativeObjectElements = NativeObject.address.add(NativeObjectTypeSize);
        const NativeObjectSlots = NativeObject.slots_.address;
        const Max = Shape.slotInfo.bitwiseShiftRight(FIXED_SLOTS_SHIFT).asNumber();
        for(let Idx = 0; Idx < Object.keys(Properties).length; Idx++) {

            //
            // Check out NativeObject::getSlot()
            //

            const PropertyName = Properties[Idx];
            let PropertyValue = undefined;
            let ElementAddr = undefined;
            if(Idx < Max) {
                ElementAddr = NativeObjectElements.add(Idx * 8);
            } else {
                ElementAddr = NativeObjectSlots.add((Idx - Max) * 8);
            }

            const JSValue = read_u64(ElementAddr);
            PropertyValue = jsvalue_to_instance(JSValue);
            this._Properties.push(PropertyName + ' : ' + PropertyValue);
        }
    }

    get Properties() {
        return this._Properties;
    }

    get ClassName() {
        return this._ClassName;
    }

    toString() {
        const Builders = {
            'Array' : __JSArray,
            'Map' : __JSMap,
            'ArrayBuffer' : __JSArrayBuffer,
            'Float64Array' : __JSTypedArray,
            'Float32Array' : __JSTypedArray,
            'Uint32Array' : __JSTypedArray,
            'Int32Array' : __JSTypedArray,
            'Uint16Array' : __JSTypedArray,
            'Int16Array' : __JSTypedArray,
            'Uint8Array' : __JSTypedArray,
            'Uint8ClampedArray' : __JSTypedArray,
            'Int8Array' : __JSTypedArray
        };

        if(Builders.hasOwnProperty(this._ClassName)) {
            return new Builders[this._ClassName](this._Addr).toString();
        }

        if(this._Properties != undefined && this._Properties.length > 0) {
            return '{' + this._Properties.join(', ') + '}';
        }

        if(this._ClassName == 'Object') {
            return '[Object]';
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
        logln(Addr.toString(16) + ': js!js::Symbol: ' + Content);
    };

    const JSSymbol = new __JSSymbol(Addr);
    Logger(JSSymbol);
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

function smdump_jsmap(Addr) {
    const Logger = function (Content) {
        logln(Addr.toString(16) + ': js!js::MapObject: ' + Content);
    };

    const JSMap = new __JSMap(Addr);
    Logger('Content: ' + JSMap);
}

function smdump_jsarraybuffer(Addr) {
    const Logger = function (Content) {
        logln(Addr.toString(16) + ': js!js::ArrayBufferObject: ' + Content);
    };

    const JSArrayBuffer = new __JSArrayBuffer(Addr);
    Logger('ByteLength: ' + JSArrayBuffer.ByteLength);
    Logger('     Flags: ' + JSArrayBuffer.Flags);
    Logger('   Content: ' + JSArrayBuffer);
}

function smdump_jstypedarray(Addr) {
    const Logger = function (Content) {
        logln(Addr.toString(16) + ': js!js::TypedArrayObject: ' + Content);
    };

    const JSTypedArray = new __JSTypedArray(Addr);
    Logger('      Type: ' + JSTypedArray.Type);
    Logger('    Length: ' + JSTypedArray.Length);
    Logger('ByteLength: ' + JSTypedArray.ByteLength);
    Logger('ByteOffset: ' + JSTypedArray.ByteOffset);
    Logger('   Content: ' + JSTypedArray);
}

function smdump_jsobject(Addr) {
    const Logger = function (Content) {
        logln(Addr.toString(16) + ': js!JSObject: ' + Content);
    };

    if(Addr.hasOwnProperty('address')) {
        Addr = Addr.address;
    }

    const JSObject = new __JSObject(Addr);
    const ClassName = JSObject.ClassName;

    const Dumpers = {
        'Function' : smdump_jsfunction,
        'Array' : smdump_jsarray,
        'ArrayBuffer' : smdump_jsarraybuffer,
        'Map' : smdump_jsmap,

        'Float64Array' : smdump_jstypedarray,
        'Float32Array' : smdump_jstypedarray,
        'Uint32Array' : smdump_jstypedarray,
        'Int32Array' : smdump_jstypedarray,
        'Uint16Array' : smdump_jstypedarray,
        'Int16Array' : smdump_jstypedarray,
        'Uint8Array' : smdump_jstypedarray,
        'Uint8ClampedArray' : smdump_jstypedarray,
        'Int8Array' : smdump_jstypedarray
    };

    if(Dumpers.hasOwnProperty(ClassName)) {
        Dumpers[ClassName](Addr);
    } else {
        Logger(' { ' + JSObject.Properties.join(', ') + ' }');
    }
}

function smdump_jsvalue(Addr) {
    // XXX: There's an issue when passing a Int64 via the command;
    // It thinks it's signed for some reason and the bitwiseShiftRight doesn't
    // do a proper right shift.
    if(Addr == undefined) {
        logln('!smdump_jsvalue <jsvalue object addr>');
        return;
    }

    if(Addr.hasOwnProperty('address')) {
        Addr = Addr.address;
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
