/*
    Anti-Dbg based on the j00ru's paper (http://j00ru.vexillium.org/?p=866) -- Evil Segmentation >:]
*/

#include <stdio.h>
#include <windows.h>

#define MERROR(x) { fprintf(stderr, "[!] An error occured in %s()|line-%d:\n\t-> '%s', GetLastError() = %.3d.\n", __FUNCTION__, __LINE__, (x), GetLastError()); }
#define MDISPLAY(...) { fprintf(stdout, "[+] "); fprintf(stdout, __VA_ARGS__); fprintf(stdout, ".\n"); }

#if !defined(NT_SUCCESS)
#define NT_SUCCESS(Status) (((NTSTATUS)(Status)) >= 0)
#endif

typedef struct
{
    ULONG Start;
    ULONG Length;
    LDT_ENTRY LdtEntries[1];
} PROCESS_LDT_INFORMATION, *PPROCESS_LDT_INFORMATION;

typedef enum
{
    ProcessLdtInformation = 10
} PROCESS_INFORMATION_CLASS;

NTSTATUS NTAPI NtSetInformationProcess(
    IN HANDLE ProcessHandle,
    IN PROCESS_INFORMATION_CLASS ProcessInformationClass,
    IN PVOID ProcessInformation,
    IN ULONG ProcessInformationLength
);

VOID ItIsDone()
{
    MDISPLAY("Hmm, It appears you're not currently debugged bro!");
    ExitProcess(0);
}

VOID AntiDbg()
{
    __asm
    {
        mov ax, 0x1B
        push ax
        push ItIsDone
        retf
    }
}

BOOL PlayWithMyCodeSegment()
{
    PROCESS_LDT_INFORMATION ldtInfo = {0};
    LDT_ENTRY cs = {0};
    DWORD base = (DWORD)GetModuleHandle(NULL), dst = (DWORD)AntiDbg;
    NTSTATUS status = 0;
    BOOL ret = TRUE;

    MDISPLAY("Process loaded at: %#.8x", base);

    cs.LimitLow                  = 0xFFFF;
	cs.BaseLow                   = base & 0xFFFF;
	cs.HighWord.Bits.BaseMid     = base >> 16;
	cs.HighWord.Bits.Type        = 0x1A;
	cs.HighWord.Bits.Dpl         = 3;
	cs.HighWord.Bits.Pres        = 1;
	cs.HighWord.Bits.LimitHi     = 0xF;
	cs.HighWord.Bits.Sys         = 0;
	cs.HighWord.Bits.Default_Big = 1;
	cs.HighWord.Bits.Granularity = 0;
	cs.HighWord.Bits.BaseHi      = base >> 24;

    MDISPLAY("Crafting a code-segment: %#.8x -> %#.8x",
        (cs.BaseLow + (cs.HighWord.Bits.BaseMid << 16) + (cs.HighWord.Bits.BaseHi << 24)),
        (((cs.LimitLow + (cs.HighWord.Bits.LimitHi << 16)) * 0x1000) + 0xffff)
    );

    ldtInfo.Start = 0;
    ldtInfo.Length = sizeof(LDT_ENTRY);
    memcpy(&ldtInfo.LdtEntries[0], &cs, sizeof(LDT_ENTRY));

    MDISPLAY("Setting up our LDT..");

    ret = NtSetInformationProcess(
        GetCurrentProcess(),
        ProcessLdtInformation,
        &ldtInfo,
        sizeof(PROCESS_LDT_INFORMATION)
    );

    if(!NT_SUCCESS(ret))
    {
        ret = FALSE;
        MERROR("NtSetInformationProcess failed");
        goto clean;
    }

    dst -= base;

    __asm
    {
        mov ax, 0x7
        push ax
        push dst
        retf
    }

    clean:
    return ret;
}

int main(int argc, char* argv[])
{
    PlayWithMyCodeSegment();
    return EXIT_SUCCESS;
}
