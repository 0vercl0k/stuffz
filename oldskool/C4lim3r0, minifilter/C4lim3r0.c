#include <fltKernel.h>
#include <string.h>

NTSTATUS cfsd_Unload(FLT_FILTER_UNLOAD_FLAGS theFlags);
FLT_PREOP_CALLBACK_STATUS AvantDirectoryControl(PFLT_CALLBACK_DATA Data,PCFLT_RELATED_OBJECTS FltObjects,PVOID *CompletionContext );
FLT_POSTOP_CALLBACK_STATUS ApresDirectoryControl(PFLT_CALLBACK_DATA Data,PCFLT_RELATED_OBJECTS FltObjects,PVOID CompletionContext,FLT_POST_OPERATION_FLAGS Flags );
NTSTATUS unloadCalimero( FLT_FILTER_UNLOAD_FLAGS theFlags );


CONST FLT_OPERATION_REGISTRATION callbacksCalimero[] =
{
    {
        IRP_MJ_DIRECTORY_CONTROL,
        0,
        AvantDirectoryControl,
        ApresDirectoryControl
    },

    {
        IRP_MJ_OPERATION_END
    }
};

CONST FLT_REGISTRATION  structRegistration =
{
    sizeof(FLT_REGISTRATION),
    FLT_REGISTRATION_VERSION,
    0,
    NULL,
    callbacksCalimero,
    unloadCalimero,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL
};

PFLT_FILTER retFilter;


NTSTATUS DriverEntry (PDRIVER_OBJECT pDriverObject,PUNICODE_STRING pRegistryPath)
{
    NTSTATUS retour = 0;
    OBJECT_ATTRIBUTES objAttrib;

    retour = FltRegisterFilter(pDriverObject,&structRegistration,&retFilter);
    if(NT_SUCCESS(retour))
    {
        DbgPrint("STATUS_SUCCESS.");
        retour = FltStartFiltering(retFilter);
        DbgPrint("Retour : %x.",retour);
    }

    return retour;
}

FLT_PREOP_CALLBACK_STATUS AvantDirectoryControl(PFLT_CALLBACK_DATA Data,PCFLT_RELATED_OBJECTS FltObjects,PVOID *CompletionContext )
{
   //The minifilter driver is returning the I/O operation to the filter manager for further processing.
   //In this case, the filter manager calls the minifilter driver's postoperation callback during I/O completion.
    return FLT_PREOP_SUCCESS_WITH_CALLBACK;
}

FLT_POSTOP_CALLBACK_STATUS ApresDirectoryControl(PFLT_CALLBACK_DATA Data,PCFLT_RELATED_OBJECTS FltObjects,PVOID CompletionContext,FLT_POST_OPERATION_FLAGS Flags )
{
    //DbgPrint("ApresDirectoryCallback called o/.");
    NTSTATUS retour;
    PFLT_FILE_NAME_INFORMATION ptrStructFileName;
    UNICODE_STRING dossierAHide;

    RtlInitUnicodeString(&dossierAHide,L"\\Device\\HarddiskVolume1\\C4lim3r0__");
    retour = FltGetFileNameInformation(Data,FLT_FILE_NAME_NORMALIZED,&ptrStructFileName);

    if(wcsstr(ptrStructFileName->Name.Buffer,dossierAHide.Buffer) != NULL)
    {
        DbgPrint("FileName : '%wZ.'",&ptrStructFileName->Name); //http://alter.org.ua/ru/docs/nt_kernel/kdprint_ustr/
        Data->IoStatus.Status = STATUS_LOCK_NOT_GRANTED;
        Data->IoStatus.Information = 0;
    }
    return FLT_POSTOP_FINISHED_PROCESSING;
}

NTSTATUS unloadCalimero( FLT_FILTER_UNLOAD_FLAGS theFlags )
{
    // DDK : "...Unregister itself so that the Filter Manager no longer calls it to
   //        process I/O operations. "
    DbgPrint("UNLOAD.");
    FltUnregisterFilter(retFilter);
    return STATUS_SUCCESS;
}
