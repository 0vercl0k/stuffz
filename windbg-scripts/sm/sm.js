// Axel '0vercl0k' Souchet - 24-June-2018
//
// Example:
//   * from the interpreter:
//       Math.atan2(['short', 13.37, new Map([[ 1, 'one' ],[ 2, 'two' ]]), ['loooooooooooooooooooooooooooooong', [0x1337, {doare:'in d4 place'}]], false, null, undefined, true, Math.atan2, Math])
//
//   * from the debugger:
//       js!js::math_atan2:
//       00007ff6`0227e140 56              push    rsi
//       0:000> !smdump_jsvalue vp[2].asBits_
//       1e5f10024c0: js!js::ArrayObject:   Length: 10
//       1e5f10024c0: js!js::ArrayObject: Capacity: 10
//       1e5f10024c0: js!js::ArrayObject:  Content: ['short', 13.37, new Map(...), ['loooooooooooooooooooooooooooooong', [0x1337, {'doare' : 'in d4 place'}]], false, null, undefined, true, atan2(), Math]
//       @$smdump_jsvalue(vp[2].asBits_)
//

'use strict';

let Module = null;

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
const JSVAL_TYPE_OBJECT = host.Int64(0x1fffc);

const INLINE_CHARS_BIT = host.Int64(1 << 6);
const LATIN1_CHARS_BIT = host.Int64(1 << 9);

const JSID_TYPE_MASK = host.Int64(0x7);
const JSID_TYPE_STRING = host.Int64(0x0);
const JSID_TYPE_INT = host.Int64(0x1);
const JSID_TYPE_VOID = host.Int64(0x2);
const JSID_TYPE_SYMBOL = host.Int64(0x4);

const SLOT_MASK = host.Int64(0xffffff);
const FIXED_SLOTS_SHIFT = host.Int64(24);

const FunctionConstants = {
    0x0001 : 'INTERPRETED',
    0x0004 : 'EXTENDED',
    0x0008 : 'BOUND_FUN',
    0x0010 : 'WASM_OPTIMIZED',
    0x0020 : 'HAS_GUESSED_ATOM/HAS_BOUND_FUNCTION_NAME_PREFIX',
    0x0040 : 'LAMBDA',
    0x0080 : 'SELF_HOSTED',
    0x0100 : 'HAS_INFERRED_NAME',
    0x0200 : 'INTERPRETED_LAZY',
    0x0400 : 'RESOLVED_LENGTH',
    0x0800 : 'RESOLVED_NAME',
};

const FunctionKindConstants = {
    0 : 'NORMAL_KIND',
    1 : 'ARROW_KIND',
    2 : 'METHOD_KIND',
    3 : 'CLASSCONSTRUCTOR_KIND',
    4 : 'GETTER_KIND',
    5 : 'SETTER_KIND',
    6 : 'ASMJS_KIND'
};

const Tag2Names = {
    [JSVAL_TYPE_DOUBLE] : 'Double',
    [JSVAL_TYPE_INT32] : 'Int32',
    [JSVAL_TYPE_STRING] : 'String',
    [JSVAL_TYPE_UNDEFINED] : 'Undefined',
    [JSVAL_TYPE_BOOLEAN] : 'Boolean',
    [JSVAL_TYPE_NULL] : 'Null',
    [JSVAL_TYPE_OBJECT] : 'Object',
    [JSVAL_TYPE_SYMBOL] : 'Symbol',
    [JSVAL_TYPE_MAGIC] : 'Magic',
};

//
// Read a uint64_t integer from Addr.
//

function read_u64(Addr) {
    return host.memory.readMemoryValues(Addr, 1, 8)[0];
}

//
// Mirror the functionality of ::fromElements.
//

function heapslot_to_objectelements(Addr) {
    // static ObjectElements* fromElements(HeapSlot* elems) {
    //  return reinterpret_cast<ObjectElements*>(uintptr_t(elems) - sizeof(ObjectElements));
    // }
    const ObjectElementsSize = host.getModuleType(Module, 'js::ObjectElements').size;
    const ObjectElements = host.createPointerObject(
        Addr.subtract(ObjectElementsSize),
        Module,
        'js::ObjectElements*'
    );

    return ObjectElements;
}

//
// Is Byte printable?
//

function printable(Byte) {
    return Byte >= 0x20 && Byte <= 0x7e;
}

//
// Return a string describing Byte; either a \x41 or its ascii representation
//

function byte_to_str(Byte) {
    if(printable(Byte)) {
        return String.fromCharCode(Byte);
    }

    return '\\x' + Byte.toString(16).padStart(2, '0');
}

//
// Is this jsid an integer?
//

function jsid_is_int(Propid) {
    const Bits = Propid.value.asBits;
    return Bits.bitwiseAnd(JSID_TYPE_MASK).compareTo(JSID_TYPE_INT) == 0;
}

//
// Is this jsid a string?
//

function jsid_is_string(Propid) {
    const Bits = Propid.value.asBits;
    return Bits.bitwiseAnd(JSID_TYPE_MASK).compareTo(JSID_TYPE_STRING) == 0;
}

//
// Retrieve a property from a Shape; returns an actual integer/string based
// on the propid_.
//

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
    if(!Tag2Names.hasOwnProperty(JSValue.Tag)) {
        return 'Dunno';
    }

    const Name = Tag2Names[JSValue.Tag];
    const Type = Names2Types[Name];
    return new Type(JSValue.Payload);
}

class __JSMagic {
    constructor(Addr) {
        this._Addr = Addr;
    }

    toString() {
        return 'magic';
    }

    Logger(Content) {
        logln(this._Addr.toString(16) + ': JSVAL_TYPE_MAGIC: ' + Content);
    }

    Display() {
        this.Logger(this);
    }
}

class __JSNull {
    constructor(Addr) {
        this._Addr = Addr;
    }

    toString() {
        return 'null';
    }

    Logger(Content) {
        logln(this._Addr.toString(16) + ': JSVAL_TYPE_NULL: ' + Content);
    }

    Display() {
        this.Logger(this);
    }
}

class __JSUndefined {
    constructor(Addr) {
        this._Addr = Addr;
    }

    toString() {
        return 'undefined';
    }

    Logger(Content) {
        logln(this.Addr.toString(16) + ': JSVAL_TYPE_UNDEFINED: ' + Content);
    }

    Display() {
        this.Logger(this);
    }
}

class __JSBoolean {
    constructor(Addr) {
        this._Addr = Addr;
        this._Value = Addr.compareTo(1) == 0 ? true : false;
    }

    toString() {
        return this._Value.toString();
    }

    Logger(Content) {
        logln(this._Addr.toString(16) + ': JSVAL_TYPE_BOOLEAN: ' + Content);
    }

    Display() {
        this.Logger(this);
    }
}

class __JSInt32 {
    constructor(Addr) {
        this._Addr = Addr;
        this._Value = Addr.bitwiseAnd(0xffffffff);
    }

    toString() {
        return '0x' + this._Value.toString(16);
    }

    Logger(Content) {
        logln(this._Addr.toString(16) + ': JSVAL_TYPE_INT32: ' + Content);
    }

    Display() {
        this.Logger(this);
    }
}

class __JSString {
    constructor(Addr) {
        this._Obj = host.createPointerObject(
            Addr,
            Module,
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
        const Flags = this._Obj.d.flags_;
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

        let Length = Flags.bitwiseShiftRight(32);
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

    Logger(Content) {
        logln(this._Obj.address.toString(16) + ': js!JSString: ' + Content);
    }

    Display() {
        this.Logger(this);
    }
}

class __JSValue {
    constructor(Addr) {
        this._Addr = Addr;
        this._Tag = this._Addr.bitwiseShiftRight(JSVAL_TAG_SHIFT);
        this._IsDouble = this._Tag.compareTo(JSVAL_TYPE_DOUBLE) < 0;
        this._Payload = this._Addr.bitwiseAnd(JSVAL_PAYLOAD_MASK);
    }

    get Payload() {
        if(this._IsDouble) {
            return this._Addr;
        }

        return this._Payload;
    }

    get Tag() {
        if(this._IsDouble) {
            return JSVAL_TYPE_DOUBLE;
        }

        return this._Tag;
    }
}

class __JSArray {
    constructor(Addr) {
        this._Obj = host.createPointerObject(
            Addr,
            Module,
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
        const Max = 10;
        const Content = [];
        for(let Idx = 0; Idx < Math.min(Max, this.Length); ++Idx) {
            const Addr = this._Content.add(Idx * 8);
            const JSValue = read_u64(Addr);
            const Inst = jsvalue_to_instance(JSValue);
            Content.push(Inst.toString());
        }

        return '[' + Content.join(', ') + (this.Length > Max ? ', ...' : '') + ']';
    }

    Logger(Content) {
        logln(this._Obj.address.toString(16) + ': js!js::ArrayObject: ' + Content);
    }

    Display() {
        this.Logger('  Length: ' + this.Length);
        this.Logger('Capacity: ' + this.Capacity);
        this.Logger(' Content: ' + this);
    }
}

class __JSFunction {
    constructor(Addr) {
        this._Obj = host.createPointerObject(
            Addr,
            Module,
            'JSFunction*'
        );

        this._Atom = this._Obj.atom_.value.address;
        this._Name = '<anonymous>';
        if(this._Atom.compareTo(0) != 0) {
            this._Name = new __JSString(this._Atom).toString().slice(1, -1);
        }

        this._Name += '()';
        this._Flags = this._Obj.flags_;
    }

    toString() {
        return this._Name;
    }

    get Flags() {
        const S = [];
        for(const Key in FunctionConstants) {
            if(this._Flags.bitwiseAnd(host.parseInt64(Key)).compareTo(0) != 0) {
                S.push(FunctionConstants[Key]);
            }
        }

        const Kind = (this._Flags >> 13) & 7;
        S.push(FunctionKindConstants[Kind]);
        return S.join(' | ');
    }

    Logger(Content) {
        logln(this._Obj.address.toString(16) + ': js!JSFunction: ' + Content);
    }

    Display() {
        this.Logger(this);
        this.Logger('Flags: ' + this.Flags);
    }
}

class __JSSymbol {
    constructor(Addr) {
        this._Obj = host.createPointerObject(
            Addr,
            Module,
            'js::Symbol*'
        );
    }

    toString() {
        const Desc = new __JSString(this._Obj.description_.address);
        return 'Symbol(' + Desc + ')';
    }

    Logger(Content) {
        logln(this.Obj_.address.toString(16) + ': js!js::Symbol: ' + Content);
    }

    Display() {
        this.Logger(this);
    }
}

class __JSArrayBuffer {
    constructor(Addr) {
        this._Obj = host.createPointerObject(
            Addr,
            Module,
            'js::ArrayBufferObject*'
        );

        const ArrayBufferObjectSize = host.getModuleType(Module, 'js::ArrayBufferObject').size;
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

        const ArrayBufferFlagsConstants = {
            [0x04] : 'DETACHED',
            [0x08] : 'OWNS_DATA',
            [0x10] : 'FOR_INLINE_TYPED_OBJECT',
            [0x20] : 'TYPED_OBJECT_VIEWS',
            [0x40] : 'FOR_ASMJS'
        };

        for(const Key in ArrayBufferFlagsConstants) {
            if(this._Flags.bitwiseAnd(host.parseInt64(Key)).compareTo(0) != 0) {
                ArrayBufferFlags.push(ArrayBufferFlagsConstants[Key]);
            }
        }

        return ArrayBufferFlags.join(' | ');
    }

    get ByteLength() {
        return this._ByteLength;
    }

    toString() {
        return 'ArrayBuffer({ByteLength:' + this._ByteLength + ', ...})';
    }

    Logger(Content) {
        logln(this._Obj.address.toString(16) + ': js!js::ArrayBufferObject: ' + Content);
    }

    Display() {
        this.Logger('ByteLength: ' + this.ByteLength);
        this.Logger('     Flags: ' + this.Flags);
        this.Logger('   Content: ' + this);
    }
}

class __JSTypedArray {
    constructor(Addr) {
        this._Obj = host.createPointerObject(
            Addr,
            Module,
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

        const TypedArrayObjectSize = host.getModuleType(Module, 'js::TypedArrayObject').size;
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

    Logger(Content) {
        logln(this._Obj.address.toString(16) + ': js!js::TypedArrayObject: ' + Content);
    }

    Display() {
        this.Logger('      Type: ' + this.Type);
        this.Logger('    Length: ' + this.Length);
        this.Logger('ByteLength: ' + this.ByteLength);
        this.Logger('ByteOffset: ' + this.ByteOffset);
        this.Logger('   Content: ' + this);
    }
}

class __JSMap {
    constructor(Addr) {
        this._Addr = Addr;
    }

    // XXX: TODO
    toString() {
        return 'new Map(...)';
    }

    Logger(Content) {
        logln(this._Addr.toString(16) + ': js!js::MapObject: ' + Content);
    }

    Display() {
        this.Logger('Content: ' + this);
    }
}

class __JSDouble {
    constructor(Addr) {
        this._Addr = Addr;
    }

    toString() {
        const U32 = new Uint32Array([
            this._Addr.getLowPart(),
            this._Addr.getHighPart()
        ]);
        const F64 = new Float64Array(U32.buffer);
        return F64[0];
    }

    Logger(Content) {
        logln(this._Addr.toString(16) + ': JSVAL_TYPE_DOUBLE: ' + Content);
    }

    Display() {
        this.Logger(this);
    }
}

const Names2Types = {
    'Function' : __JSFunction,
    'Array' : __JSArray,
    'ArrayBuffer' : __JSArrayBuffer,
    'Map' : __JSMap,
    'Int32' : __JSInt32,
    'String' : __JSString,
    'Boolean' : __JSBoolean,
    'Null' : __JSNull,
    'Undefined' : __JSUndefined,
    'Symbol' : __JSSymbol,
    'Double' : __JSDouble,

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
            Module,
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
            Module,
            'js::Shape*'
        );

        const NativeObject = host.createPointerObject(Addr, Module, 'js::NativeObject*');

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
            const SlotIdx = CurrentShape.immutableFlags.bitwiseAnd(SLOT_MASK).asNumber();
            Properties[SlotIdx] = get_property_from_shape(CurrentShape);
            CurrentShape = CurrentShape.parent.value;
        }

        //
        // Walk the slots to get the values now (check NativeGetPropertyInline/GetExistingProperty)
        //

        const NativeObjectTypeSize = host.getModuleType(Module, 'js::NativeObject').size;
        const NativeObjectElements = NativeObject.address.add(NativeObjectTypeSize);
        const NativeObjectSlots = NativeObject.slots_.address;
        const Max = Shape.immutableFlags.bitwiseShiftRight(FIXED_SLOTS_SHIFT).asNumber();
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
        if(this._ClassName != 'Object' && Names2Types.hasOwnProperty(this._ClassName)) {
            const Type = Names2Types[this._ClassName];
            return new Type(this._Addr).toString();
        }

        if(this._ClassName != 'Object') {
            return this._ClassName;
        }

        if(this._Properties != undefined && this._Properties.length > 0) {
            return '{' + this._Properties.join(', ') + '}';
        }

        if(this._ClassName == 'Object') {
            return '[Object]';
        }

        return 'Dunno';
    }

    Logger(Content) {
        logln(this._Addr.toString(16) + ': js!JSObject: ' + Content);
    }

    Display() {
        this.Logger('Content: ' + this);

        //
        // If the class name is not Object then it means the toString() method
        // might already have displayed the properties.
        // {foo:'bar'} VS Math.
        //

        if(this._ClassName != 'Object') {
            this.Logger('Properties: {' + this._Properties.join(', ') + '}');
        }
    }
}

Names2Types['Object'] = __JSObject;

function smdump_jsobject(Addr, Type = null) {
    Init();

    if(Addr.hasOwnProperty('address')) {
        Addr = Addr.address;
    }

    let ClassName;
    if(Type == 'Object' || Type == null) {
        const JSObject = new __JSObject(Addr);
        ClassName = JSObject.ClassName;
        if(!Names2Types.hasOwnProperty(ClassName)) {
            JSObject.Display();
        }
    } else {
        ClassName = Type;
    }

    if(Names2Types.hasOwnProperty(ClassName)) {
        const Inst = new Names2Types[ClassName](Addr);
        Inst.Display();
    }
}

function smdump_jsvalue(Addr) {
    Init();

    if(Addr == undefined) {
        logln('!smdump_jsvalue <jsvalue object addr>');
        return;
    }

    //
    // Ensure Addr is an unsigned value. If we don't do this
    // the shift operations don't behave the way we want them to.
    //

    Addr = Addr.bitwiseAnd(host.parseInt64('0xffffffffffffffff'));
    const JSValue = new __JSValue(Addr);
    if(!Tag2Names.hasOwnProperty(JSValue.Tag)) {
        logln('Tag ' +  JSValue.Tag.toString(16) + ' not recognized');
        return;
    }

    const Name = Tag2Names[JSValue.Tag];
    return smdump_jsobject(JSValue.Payload, Name);
}

function Init() {
    if(Module != null) {
        return;
    }

    const Xul = host.currentProcess.Modules.Any(
        p => p.Name.toLowerCase().endsWith('xul.dll')
    );

    if(Xul) {
        Module = 'xul.dll';
        logln('Detected xul.dll, using it as js module.');
        return;
    }

    Module = 'js.exe';
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
