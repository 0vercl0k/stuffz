#include <wdm.h>
#include <ntddkbd.h>

typedef struct _EXTENSION_DEVICE
{
    PDEVICE_OBJECT pDeviceAttache;
}EXTENSION_DEVICE,*PEXTENSION_DEVICE;

int compteur = 0;


VOID unloadDriver(PDRIVER_OBJECT pDriverObject);
NTSTATUS RelayerIRPsOsef(PDEVICE_OBJECT pDeviceObject,PIRP pIrp);
NTSTATUS RelayerIRPs(PDEVICE_OBJECT pDeviceObject,PIRP pIrp);
NTSTATUS CompletionRoutine(PDEVICE_OBJECT pFdo, PIRP pIrp, PVOID context);

NTSTATUS DriverEntry(PDRIVER_OBJECT pDriverObject,PUNICODE_STRING pRegistryPath)
{
    NTSTATUS retour = 0;
    PDEVICE_OBJECT pNotreDevice,pDeviceAttache;
    UNICODE_STRING keyboardClass0;
    PEXTENSION_DEVICE pExtensionDevice;
    int i;

    RtlInitUnicodeString(&keyboardClass0,L"\\Device\\KeyboardClass0");
    retour = IoCreateDevice(pDriverObject,sizeof(EXTENSION_DEVICE),NULL,FILE_DEVICE_KEYBOARD,0,TRUE,&pNotreDevice);


    RtlZeroMemory(pNotreDevice->DeviceExtension,sizeof(EXTENSION_DEVICE));
    pExtensionDevice =  pNotreDevice->DeviceExtension;

    pNotreDevice->Flags = pNotreDevice->Flags | DO_BUFFERED_IO | DO_POWER_PAGABLE ;
    pNotreDevice->Flags = pNotreDevice->Flags &~ DO_DEVICE_INITIALIZING ; //A device function or filter driver clears the flag in its AddDevice routine, after attaching the device object to the device stack
    //&~ = NON on vire le bit DO_DEVICE_INITIALIZING.

    for(i = 0 ; i < IRP_MJ_MAXIMUM_FUNCTION ; i++)pDriverObject->MajorFunction[i] = RelayerIRPsOsef;

    pDriverObject->MajorFunction[IRP_MJ_READ] = RelayerIRPs;

    retour = IoAttachDevice(pNotreDevice,&keyboardClass0,&pExtensionDevice->pDeviceAttache);

    pDriverObject->DriverUnload = unloadDriver;

    return STATUS_SUCCESS;
}

VOID unloadDriver(PDRIVER_OBJECT pDriverObject)
{
    PEXTENSION_DEVICE pDeviceExt;

    pDeviceExt = (PEXTENSION_DEVICE)pDriverObject->DeviceObject->DeviceExtension;
    IoDetachDevice(pDeviceExt->pDeviceAttache);
    DbgPrint("Dettaché.");
}

NTSTATUS RelayerIRPsOsef(PDEVICE_OBJECT pDeviceObject,PIRP pIrp)
{
    //DbgPrint("Relais d'une IRP.");
    IoSkipCurrentIrpStackLocation(pIrp);//On passe l'irp au device suivant, soit KeyboardClass0 la cible.
    return IoCallDriver(((PEXTENSION_DEVICE)pDeviceObject->DeviceExtension)->pDeviceAttache , pIrp);
}

NTSTATUS RelayerIRPs(PDEVICE_OBJECT pDeviceObject,PIRP pIrp)
{
    //You often need to know the results of I/O requests that you pass down to lower levels of the driver hierarchy or that you originate.
    //To find out what happened to a request, you install a completion routine by calling IoSetCompletionRoutine:


    //If you intend to provide an IoCompletion routine for the IRP, your driver should call IoCopyCurrentIrpStackLocationToNext instead of IoSkipCurrentIrpStackLocation
    //After calling this routine, a driver typically sets an I/O completion routine with IoSetCompletionRoutine before passing the IRP to the next-lower driver with IoCallDriver. Drivers that pass on their IRP parameters but do not set an I/O completion routine should call IoSkipCurrentIrpStackLocation instead of this routine.

    PIO_STACK_LOCATION IrpStackCourante = IoGetCurrentIrpStackLocation(pIrp);
    PIO_STACK_LOCATION IrpStackSuivante = IoGetNextIrpStackLocation(pIrp);

    *IrpStackSuivante = *IrpStackCourante;

    IoSetCompletionRoutine(pIrp,CompletionRoutine,pDeviceObject,TRUE,TRUE,TRUE);

    return IoCallDriver(((PEXTENSION_DEVICE)pDeviceObject->DeviceExtension)->pDeviceAttache , pIrp);
}

NTSTATUS CompletionRoutine(PDEVICE_OBJECT pDeviceObject, PIRP pIrp, PVOID context)
{
    PEXTENSION_DEVICE pDeviceExtension = pDeviceObject->DeviceExtension;
    PKEYBOARD_INPUT_DATA ptrStructKeyboard;
    int nbrStruct,i;
    const unsigned short mot[] = {24,47,18,19,46,38,24,37,57}; //'o' ,'v' ,'e' ,'r' ,'c' ,'l' ,'o' ,'k' ,' '


    if(pIrp->IoStatus.Status == STATUS_SUCCESS)
    {
        nbrStruct = ((pIrp->IoStatus.Information)/(sizeof(KEYBOARD_INPUT_DATA)));

        for(i = 0 ; i < nbrStruct ; i++)
        {
            if( (sizeof(mot)/sizeof(unsigned short)) < compteur)compteur = 0;

            ptrStructKeyboard = pIrp->AssociatedIrp.SystemBuffer;

            if(ptrStructKeyboard[i].Flags == KEY_MAKE)
            {
                ptrStructKeyboard[i].MakeCode = mot[compteur];
                compteur++;
            }
        }

    }

    if(pIrp->PendingReturned)
    {
        IoMarkIrpPending(pIrp);
    }
    return pIrp->IoStatus.Status;
}
