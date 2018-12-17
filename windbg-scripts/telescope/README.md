# telescope.js

`telescope.js` is a [JavaScript](https://docs.microsoft.com/en-us/windows-hardware/drivers/debugger/javascript-debugger-scripting) debugger extension  for WinDbg that mirrors the `dereference`/`telescope` command from [GEF](https://github.com/hugsy/gef). It works on crash-dumps, live debugging, and TTD traces. Both for user and kernel-mode.

## Usage

Run `.scriptload telescope.js` to load the script. You can invoke the telescope feature with `!telescope <addr>` or programatically via `dx @$createchain(<addr>)`.

## Examples

* From an x64 TTD execution trace:

```text
0:000> !telescope @rsp
0x0000005be1ffcec0|+0x0000: 0xe1000205e1ffdd48 (Unknown)
0x0000005be1ffcec8|+0x0008: 0x00007ff700000006 (Unknown)
0x0000005be1ffced0|+0x0010: 0x000001fce5928840 (VirtualAlloced) -> 0x0000005be1ffd0b8 (Stack) -> 0x000001fce5928840 (VirtualAlloced) [...]
0x0000005be1ffced8|+0x0018: 0x0000005be1ffdb68 (Stack) -> 0x000001fce5928840 (VirtualAlloced) -> 0x0000005be1ffd0b8 (Stack) -> 0x000001fce5928840 (VirtualAlloced) [...]
0x0000005be1ffcee0|+0x0020: 0x000001fce634afa0 (VirtualAlloced) -> 0x0000000800000b50 (Unknown)
0x0000005be1ffcee8|+0x0028: 0x00004a54b4bb11e0 (Unknown)
0x0000005be1ffcef0|+0x0030: 0x0000000000000008 (Unknown)
0x0000005be1ffcef8|+0x0038: 0x0000000000000000 (Unknown)
0x0000005be1ffcf00|+0x0040: 0x0000005be1ffdbc8 (Stack) -> 0x000001fce6cb3eb8 (VirtualAlloced) -> 0x00007ff77704e920 (js.exe (.rdata)) -> 0x00007ff776755aa0 (js.exe (.text)) -> mov     rax,qword ptr [rcx-18h] ; test    byte ptr [rax+23h],2
0x0000005be1ffcf08|+0x0048: 0x00007ff7766b4546 (js.exe (.text)) -> test    rax,rax ; je      js!mozilla::Vector<char *,0,js::TempAllocPolicy>::growStorageBy+0x395 (00007ff7`766b4805)
@$telescope(@rsp)
```

* Accessing the chain programatically via `createchain`:

```text
0:000> dx @$createchain(0x0000005be1ffcf08)
@$createchain(0x0000005be1ffcf08)                 : 0x00007ff7766b4546 (js.exe (.text)) -> test    rax,rax ; je      js!mozilla::Vector<char *,0,js::TempAllocPolicy>::growStorageBy+0x395 (00007ff7`766b4805)
    [0x0]            : 0x00007ff7766b4546 (js.exe (.text))
    [0x1]            : test    rax,rax ; je      js!mozilla::Vector<char *,0,js::TempAllocPolicy>::growStorageBy+0x395 (00007ff7`766b4805)

0:000> dx -r1 @$createchain(0x0000005be1ffcf08)[0]
@$createchain(0x0000005be1ffcf08)[0]                 : 0x00007ff7766b4546 (js.exe (.text))
    Addr             : 0x5be1ffcf08
    Value            : 0x7ff7766b4546
    AddrRegion       : Stack rw-
    ValueRegion      : Image C:\work\codes\blazefox\js-release\js.exe (.text) r-x
    Name             : js.exe (.text)
    Last             : false

0:000> dx -r1 @$createchain(0x0000005be1ffcf08)[1]
@$createchain(0x0000005be1ffcf08)[1]                 : test    rax,rax ; je      js!mozilla::Vector<char *,0,js::TempAllocPolicy>::growStorageBy+0x395 (00007ff7`766b4805)
    Addr             : 0x7ff7766b4546
    Value            : 0x2b6840fc08548
    AddrRegion       : Image C:\work\codes\blazefox\js-release\js.exe (.text) r-x
    Name             : Unknown
    Last             : true
```

* From an x86 live-session:

```text
0:001> !telescope @esp
0x00d7ff44|+0x0000: 0x77dcb3a9 (ntdll.dll (.text)) -> jmp     ntdll!DbgUiRemoteBreakin+0x42 (77dcb3b2) ; xor     eax,eax
0x00d7ff48|+0x0004: 0x1911c0a3 (Unknown)
0x00d7ff4c|+0x0008: 0x77dcb370 (ntdll.dll (.text)) -> push    8 ; push    offset ntdll!QueryRegistryValue+0x13d2 (77e29538)
0x00d7ff50|+0x000c: 0x77dcb370 (ntdll.dll (.text)) -> push    8 ; push    offset ntdll!QueryRegistryValue+0x13d2 (77e29538)
0x00d7ff54|+0x0010: 0x00000000 (Unknown)
0x00d7ff58|+0x0014: 0x00d7ff48 (Stack) -> 0x1911c0a3 (Unknown)
0x00d7ff5c|+0x0018: 0x00000000 (Unknown)
0x00d7ff60|+0x001c: 0x00d7ffcc (Stack) -> 0x00d7ffe4 (Stack) -> 0xffffffff (Unknown)
0x00d7ff64|+0x0020: 0x77d986d0 (ntdll.dll (.text)) -> mov     edi,edi ; push    ebp
0x00d7ff68|+0x0024: 0x6e24aaeb (Unknown)
@$telescope(@esp)
```

* From an x64 kernel live-session

```
kd> !telescope 0xfffff8000d2dca78
0xfffff8000d2dca78|+0x0000: 0x0000000000000000 (Unknown)
0xfffff8000d2dca80|+0x0008: 0x0000000000000000 (Unknown)
0xfffff8000d2dca88|+0x0010: 0x0000000000000000 (Unknown)
0xfffff8000d2dca90|+0x0018: 0xfffff8000d03e030 (Image ntkrnlmp.exe (.text)) -> sub     rsp,28h ; and     qword ptr [rsp+28h],0
0xfffff8000d2dca98|+0x0020: 0x0000000000000000 (Unknown)
0xfffff8000d2dcaa0|+0x0028: 0x0000000000000000 (Unknown)
0xfffff8000d2dcaa8|+0x0030: 0xfffff8000d2d9e48 (Image ntkrnlmp.exe (CACHEALI)) -> 0xfffff8000d2dcaa8 (Image ntkrnlmp.exe (CACHEALI)) [...]
0xfffff8000d2dcab0|+0x0038: 0xfffff8000d2d9e48 (Image ntkrnlmp.exe (CACHEALI)) -> 0xfffff8000d2dcaa8 (Image ntkrnlmp.exe (CACHEALI)) -> 0xfffff8000d2d9e48 (Image ntkrnlmp.exe (CACHEALI)) [...]
0xfffff8000d2dcab8|+0x0040: 0x0000000000000000 (Unknown)
0xfffff8000d2dcac0|+0x0048: 0x0000000000000000 (Unknown)
@$telescope(0xfffff8000d2dca78)
```
