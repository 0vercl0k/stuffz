# sm.js

`sm.js` is a [JavaScript](https://docs.microsoft.com/en-us/windows-hardware/drivers/debugger/javascript-debugger-scripting) debugger extension for WinDbg that allows to dump both `js::Value` and `JSObject` [Spidermonkey](https://github.com/mozilla/gecko-dev/tree/master/js) objects. It works on crash-dumps, live debugging, and TTD traces.

The extension detects automatically if it is running from the [Javascript shell](https://github.com/mozilla/gecko-dev/tree/master/js/src/shell) (in which case `js.exe` is the module hosting the JavaScript engine code) or from Firefox directly (in which case `xul.dll` is the module hosting the JavaScript engine code). Private symbol information for the module hosting the JavaScript engine code is required. It only supports x64 version of spidermonkey.

It has been used and tested against spidermonkey during end of 2018 - but should work fine on newer versions assuming core data-structures haven't changed a whole lot (and if they do, it should be fairly easy to adapt anyway).

## Usage

Run `.scriptload sm.js` to load the script. You can dump `js::Value` with `!smdump_jsvalue` and `JSObject` with `!smdump_jsobject`.

## Examples

* Dumping the `js::Value` associated to the following JavaScript object `['short', 13.37, new Map([[ 1, 'one' ],[ 2, 'two' ]]), ['loooooooooooooooooooooooooooooong', [0x1337, {doare:'in d4 place'}]], false, null, undefined, true, Math.atan2, Math]`:

```text
0:000> !smdump_jsvalue vp[2].asBits_
1e5f10024c0: js!js::ArrayObject:   Length: 10
1e5f10024c0: js!js::ArrayObject: Capacity: 10
1e5f10024c0: js!js::ArrayObject:  Content: ['short', 13.37, new Map(...), ['loooooooooooooooooooooooooooooong', [0x1337, {'doare' : 'in d4 place'}]], false, null, undefined, true, atan2(), Math]
@$smdump_jsvalue(vp[2].asBits_)
```

