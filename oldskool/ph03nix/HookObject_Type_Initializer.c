#include <Ntifs.h>
#include <string.h>

PULONG ptrDeleteProcedure;
ULONG ancienneValeur;
VOID (*PspProcessDelete)(PVOID);


typedef enum _SYSTEM_INFORMATION_CLASS {
	SystemInformationClassMin = 0,
	SystemBasicInformation = 0,
	SystemProcessorInformation = 1,
	SystemPerformanceInformation = 2,
	SystemTimeOfDayInformation = 3,
	SystemPathInformation = 4,
	SystemNotImplemented1 = 4,
	SystemProcessInformation = 5,
	SystemProcessesAndThreadsInformation = 5,
	SystemCallCountInfoInformation = 6,
	SystemCallCounts = 6,
	SystemDeviceInformation = 7,
	SystemConfigurationInformation = 7,
	SystemProcessorPerformanceInformation = 8,
	SystemProcessorTimes = 8,
	SystemFlagsInformation = 9,
	SystemGlobalFlag = 9,
	SystemCallTimeInformation = 10,
	SystemNotImplemented2 = 10,
	SystemModuleInformation = 11,
	SystemLocksInformation = 12,
	SystemLockInformation = 12,
	SystemStackTraceInformation = 13,
	SystemNotImplemented3 = 13,
	SystemPagedPoolInformation = 14,
	SystemNotImplemented4 = 14,
	SystemNonPagedPoolInformation = 15,
	SystemNotImplemented5 = 15,
	SystemHandleInformation = 16,
	SystemObjectInformation = 17,
	SystemPageFileInformation = 18,
	SystemPagefileInformation = 18,
	SystemVdmInstemulInformation = 19,
	SystemInstructionEmulationCounts = 19,
	SystemVdmBopInformation = 20,
	SystemInvalidInfoClass1 = 20,
	SystemFileCacheInformation = 21,
	SystemCacheInformation = 21,
	SystemPoolTagInformation = 22,
	SystemInterruptInformation = 23,
	SystemProcessorStatistics = 23,
	SystemDpcBehaviourInformation = 24,
	SystemDpcInformation = 24,
	SystemFullMemoryInformation = 25,
	SystemNotImplemented6 = 25,
	SystemLoadImage = 26,
	SystemUnloadImage = 27,
	SystemTimeAdjustmentInformation = 28,
	SystemTimeAdjustment = 28,
	SystemSummaryMemoryInformation = 29,
	SystemNotImplemented7 = 29,
	SystemNextEventIdInformation = 30,
	SystemNotImplemented8 = 30,
	SystemEventIdsInformation = 31,
	SystemNotImplemented9 = 31,
	SystemCrashDumpInformation = 32,
	SystemExceptionInformation = 33,
	SystemCrashDumpStateInformation = 34,
	SystemKernelDebuggerInformation = 35,
	SystemContextSwitchInformation = 36,
	SystemRegistryQuotaInformation = 37,
	SystemLoadAndCallImage = 38,
	SystemPrioritySeparation = 39,
	SystemPlugPlayBusInformation = 40,
	SystemNotImplemented10 = 40,
	SystemDockInformation = 41,
	SystemNotImplemented11 = 41,
	/* SystemPowerInformation = 42, Conflicts with POWER_INFORMATION_LEVEL 1 */
	SystemInvalidInfoClass2 = 42,
	SystemProcessorSpeedInformation = 43,
	SystemInvalidInfoClass3 = 43,
	SystemCurrentTimeZoneInformation = 44,
	SystemTimeZoneInformation = 44,
	SystemLookasideInformation = 45,
	SystemSetTimeSlipEvent = 46,
	SystemCreateSession = 47,
	SystemDeleteSession = 48,
	SystemInvalidInfoClass4 = 49,
	SystemRangeStartInformation = 50,
	SystemVerifierInformation = 51,
	SystemAddVerifier = 52,
	SystemSessionProcessesInformation	= 53,
	SystemInformationClassMax
} SYSTEM_INFORMATION_CLASS;

// types
typedef struct _SYSTEM_THREAD_INFORMATION {
	LARGE_INTEGER KernelTime;
	LARGE_INTEGER UserTime;
	LARGE_INTEGER CreateTime;
	ULONG WaitTime;
	PVOID StartAddress;
	CLIENT_ID ClientId;
	KPRIORITY Priority;
	KPRIORITY BasePriority;
	ULONG ContextSwitchCount;
	LONG State;
	LONG WaitReason;
} SYSTEM_THREAD_INFORMATION, *PSYSTEM_THREAD_INFORMATION;

typedef struct _SYSTEM_PROCESS_INFORMATION {
	ULONG NextEntryOffset;
	ULONG NumberOfThreads;
	LARGE_INTEGER SpareLi1;
	LARGE_INTEGER SpareLi2;
	LARGE_INTEGER SpareLi3;
	LARGE_INTEGER CreateTime;
	LARGE_INTEGER UserTime;
	LARGE_INTEGER KernelTime;
	UNICODE_STRING ImageName;
	KPRIORITY BasePriority;
	HANDLE UniqueProcessId;
	HANDLE InheritedFromUniqueProcessId;
	ULONG HandleCount;
	ULONG SessionId;
	ULONG_PTR PageDirectoryBase;
	SIZE_T PeakVirtualSize;
	SIZE_T VirtualSize;
	ULONG PageFaultCount;
	SIZE_T PeakWorkingSetSize;
	SIZE_T WorkingSetSize;
	SIZE_T QuotaPeakPagedPoolUsage;
	SIZE_T QuotaPagedPoolUsage;
	SIZE_T QuotaPeakNonPagedPoolUsage;
	SIZE_T QuotaNonPagedPoolUsage;
	SIZE_T PagefileUsage;
	SIZE_T PeakPagefileUsage;
	SIZE_T PrivatePageCount;
	LARGE_INTEGER ReadOperationCount;
	LARGE_INTEGER WriteOperationCount;
	LARGE_INTEGER OtherOperationCount;
	LARGE_INTEGER ReadTransferCount;
	LARGE_INTEGER WriteTransferCount;
	LARGE_INTEGER OtherTransferCount;
	SYSTEM_THREAD_INFORMATION Threads[1];
} SYSTEM_PROCESS_INFORMATION, *PSYSTEM_PROCESS_INFORMATION;

NTSTATUS ZwQuerySystemInformation(
    SYSTEM_INFORMATION_CLASS SystemInformationClass,
    PVOID SystemInformation,
    ULONG SystemInformationLength,
    PULONG ReturnLength
  );
VOID PspProcessDeleteHooked(
    PVOID Object
  );
VOID unloadDriver(PDRIVER_OBJECT pDriverObject);
HANDLE NameToPid(PUNICODE_STRING name);



NTSTATUS DriverEntry(PDRIVER_OBJECT pDriverObject,PUNICODE_STRING pRegistryPath)
{
    NTSTATUS retour;
    HANDLE handleProc,pID,handleObject;
    OBJECT_ATTRIBUTES objectAttrib;
    CLIENT_ID clientID;
    UNICODE_STRING name;
    PUCHAR ptrObject,ptrObjectHeader,ptrObjectType,ptrObjectTypeInit;

    RtlInitUnicodeString(&name,L"explorer.exe");
    pDriverObject->DriverUnload = unloadDriver;


    pID = NameToPid(&name);
    if(pID == NULL) return STATUS_SUCCESS;
    DbgPrint("PID : %d.",pID);

    clientID.UniqueProcess = pID;
    clientID.UniqueThread = NULL;

    InitializeObjectAttributes(&objectAttrib,NULL,0,NULL,NULL);

    retour = ZwOpenProcess(&handleProc,PROCESS_DUP_HANDLE,&objectAttrib,&clientID);

    retour = ObReferenceObjectByHandle(handleProc,GENERIC_READ,*PsProcessType,KernelMode,&ptrObject,NULL);

    ptrObjectHeader = ptrObject - 0x18;
    ptrObjectType = (PUCHAR)(*(PULONG)(ptrObjectHeader + 0x8));
    ptrObjectTypeInit = ptrObjectType + 0x60;
    ptrDeleteProcedure = (PULONG)(ptrObjectTypeInit + 0x38);

    ancienneValeur = *ptrDeleteProcedure;
    PspProcessDelete = (VOID*)ancienneValeur;   //   +0x038 DeleteProcedure  : 0x8058a87d     void  nt!PspProcessDelete+0

    *ptrDeleteProcedure = (ULONG)PspProcessDeleteHooked;

    DbgPrint("ObjectInit : %x",ptrObjectTypeInit);


/*kd> dt nt!_OBJECT_HEADER 8152a448
   +0x000 PointerCount     : 166
   +0x004 HandleCount      : 8
   +0x004 NextToFree       : 0x00000008
   +0x008 Type             : 0x817cce70 _OBJECT_TYPE
   +0x00c NameInfoOffset   : 0 ''
   +0x00d HandleInfoOffset : 0 ''
   +0x00e QuotaInfoOffset  : 0 ''
   +0x00f Flags            : 0x20 ' '
   +0x010 ObjectCreateInfo : 0x81533350 _OBJECT_CREATE_INFORMATION
   +0x010 QuotaBlockCharged : 0x81533350
   +0x014 SecurityDescriptor : 0xe1ab0bdf
   +0x018 Body             : _QUAD
kd> dt nt!_OBJECT_TYPE 817cce70
   +0x000 Mutex            : _ERESOURCE
   +0x038 TypeList         : _LIST_ENTRY [ 0x817ccea8 - 0x817ccea8 ]
   +0x040 Name             : _UNICODE_STRING "Process"
   +0x048 DefaultObject    : (null)
   +0x04c Index            : 5
   +0x050 TotalNumberOfObjects : 0x13
   +0x054 TotalNumberOfHandles : 0x49
   +0x058 HighWaterNumberOfObjects : 0x13
   +0x05c HighWaterNumberOfHandles : 0x49
   +0x060 TypeInfo         : _OBJECT_TYPE_INITIALIZER
   +0x0ac Key              : 0x636f7250
   +0x0b0 ObjectLocks      : [4] _ERESOURCE
   kd> dt nt!_OBJECT_TYPE_INITIALIZER 817cced0
   +0x000 Length           : 0x4c
   +0x002 UseDefaultObject : 0 ''
   +0x003 CaseInsensitive  : 0 ''
   +0x004 InvalidAttributes : 0xb0
   +0x008 GenericMapping   : _GENERIC_MAPPING
   +0x018 ValidAccessMask  : 0x1f0fff
   +0x01c SecurityRequired : 0x1 ''
   +0x01d MaintainHandleCount : 0 ''
   +0x01e MaintainTypeList : 0 ''
   +0x020 PoolType         : 0 ( NonPagedPool )
   +0x024 DefaultPagedPoolCharge : 0x1000
   +0x028 DefaultNonPagedPoolCharge : 0x290
   +0x02c DumpProcedure    : (null)
   +0x030 OpenProcedure    : (null)
   +0x034 CloseProcedure   : (null)
   +0x038 DeleteProcedure  : 0x8058a87d     void  nt!PspProcessDelete+0
   +0x03c ParseProcedure   : (null)
   +0x040 SecurityProcedure : 0x8056a71e     long  nt!SeDefaultObjectMethod+0
   +0x044 QueryNameProcedure : (null)
   +0x048 OkayToCloseProcedure : (null)


*/
    __asm{int 3}
    ZwClose(handleProc);

    //ObOpenObjectByPointer();
    return STATUS_SUCCESS;
}


VOID unloadDriver(PDRIVER_OBJECT pDriverObject)
{
    *ptrDeleteProcedure = ancienneValeur;
    DbgPrint("Unload.");
}


HANDLE NameToPid(PUNICODE_STRING name)
{
    ULONG taille;
    PSYSTEM_PROCESS_INFORMATION structProcessInfo;
    NTSTATUS ret;

    ZwQuerySystemInformation(SystemProcessInformation,NULL,0,&taille);
    structProcessInfo = ExAllocatePoolWithTag(PagedPool,taille,'zgaT');

    ret = ZwQuerySystemInformation(SystemProcessInformation,structProcessInfo,taille,&taille);
    while(structProcessInfo->NextEntryOffset != 0)
    {
        if(structProcessInfo->ImageName.Buffer != NULL)
        {
            if(wcsstr(structProcessInfo->ImageName.Buffer,name->Buffer) != NULL)
            {
                return structProcessInfo->UniqueProcessId;
            }
        }
        structProcessInfo = (PSYSTEM_PROCESS_INFORMATION)((PUCHAR)structProcessInfo + structProcessInfo->NextEntryOffset);
    }
    ExFreePoolWithTag(structProcessInfo,'zgaT');

    return NULL;
}

VOID PspProcessDeleteHooked(PVOID Object)
{
    PEPROCESS ptrStructProc;
    NTSTATUS retour;
    char* processInkillable = "calc.exe";

    ptrStructProc = Object;
    if(strcmp(((PUCHAR)ptrStructProc + 0x174),processInkillable))
    {
        PspProcessDelete(Object);
    }
    DbgPrint("Process a proteger (%s).",(PUCHAR)ptrStructProc + 0x174); //+0x174 ImageFileName    : [16] UChar
}