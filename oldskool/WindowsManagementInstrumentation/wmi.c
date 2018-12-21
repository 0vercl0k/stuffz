#include <Ntifs.h>
#include <wdf.h>
#include "wmi.h"

/*
To support WMI data blocks, a framework-based driver must:

    * Register the managed object format (MOF) resource names of any customized WMI data providers that are not defined in Wmicore.mof.
    * Define event callback functions that support a WMI client's requests to access the driver's WMI data blocks.
    * Create a WMI provider object for each WMI data block that the driver supports for a device.
    * Create a WMI instance object for each instance of each data block that the driver supports for a device.
    * Register each WMI instance object to make it available to WMI clients.
*/



/*
A framework-based driver's DriverEntry routine must:

    * Activate WPP software tracing.
      DriverEntry should include a WPP_INIT_TRACING macro to activate software tracing.

    * Call WdfDriverCreate.
      The call to WdfDriverCreate enables the driver to use Windows Driver Framework interfaces. (The driver cannot call other framework routines before calling WdfDriverCreate.)

    * Allocate any non-device-specific system resources and global variables that it might need.
      Typically, drivers associate system resources with individual devices. Therefore, framework-based drivers allocate most resources in an EvtDriverDeviceAdd callback, which is called when individual devices are detected.

    [* Obtain driver-specific parameters from the registry.
      Some drivers obtain parameters from the registry. These drivers can call WdfDriverOpenParametersRegistryKey to open the registry key that contains these parameters.]

    * Provide a DriverEntry return value.
*/
NTSTATUS
  DriverEntry(
    PDRIVER_OBJECT pDriverObj,
    PUNICODE_STRING pRegistryPath
    )
{
    NTSTATUS ret = STATUS_SUCCESS;
    WDF_DRIVER_CONFIG config = {0};

    pDriverObj->DriverUnload = Unload;
    DbgPrint("[ Wmi::DriverEntry ]\n");

    WDF_DRIVER_CONFIG_INIT(&config, WmiEvtDriverDeviceAdd);

    DBGING("-> Création du framework..\n");
    ret = WdfDriverCreate(pDriverObj, pRegistryPath, WDF_NO_OBJECT_ATTRIBUTES, &config, WDF_NO_HANDLE);

    return ret;
}

VOID
  Unload(PDRIVER_OBJECT pDrivObj)
{
    DbgPrint("[ Wmi::Unload ]\n");
    return;
}

//A driver's EvtDriverDeviceAdd event callback function performs device initialization operations when the Plug and Play (PnP) manager
//reports the existence of a device.
NTSTATUS
  WmiEvtDriverDeviceAdd(
    WDFDRIVER DriverObject,
    PWDFDEVICE_INIT DeviceInit
    )
{
    NTSTATUS ret = STATUS_SUCCESS;
    WDF_OBJECT_ATTRIBUTES objAttr = {0};
    WDFDEVICE deviceObject = {0};
    WDF_WMI_INSTANCE_CONFIG wmiInstConfig = {0};
    WDF_WMI_PROVIDER_CONFIG wmiProvConfig = {0};
    POBJECT_CONTEXT pContext = NULL;
    DECLARE_CONST_UNICODE_STRING(nameMof_u, L"MofResourceName");

    WDF_OBJECT_ATTRIBUTES_INIT(&objAttr);
    WDF_OBJECT_ATTRIBUTES_SET_CONTEXT_TYPE(&objAttr, OBJECT_CONTEXT);
    objAttr.EvtDestroyCallback = WmiDestroyCallback;

    WDF_WMI_INSTANCE_CONFIG_INIT_PROVIDER_CONFIG(&wmiInstConfig, &wmiProvConfig);
    WDF_WMI_PROVIDER_CONFIG_INIT(&wmiProvConfig, &WmiT4pz_GUID);
    wmiProvConfig.MinInstanceBufferSize = sizeof(WmiT4pz);

    /*
        typedef struct _WDF_WMI_INSTANCE_CONFIG
        {
            ULONG  Size;
            WDFWMIPROVIDER  Provider;
            PWDF_WMI_PROVIDER_CONFIG  ProviderConfig;
            BOOLEAN  UseContextForQuery;
            BOOLEAN  Register;
            PFN_WDF_WMI_INSTANCE_QUERY_INSTANCE  EvtWmiInstanceQueryInstance;
            PFN_WDF_WMI_INSTANCE_SET_INSTANCE  EvtWmiInstanceSetInstance;
            PFN_WDF_WMI_INSTANCE_SET_ITEM  EvtWmiInstanceSetItem;
            PFN_WDF_WMI_INSTANCE_EXECUTE_METHOD  EvtWmiInstanceExecuteMethod;
        } WDF_WMI_INSTANCE_CONFIG, *PWDF_WMI_INSTANCE_CONFIG;
    */

    //A Boolean value that, if TRUE, indicates that the framework will register the provider instance with the system's WMI service after it creates a WMI instance object.
    // If this member is FALSE, the driver must call WdfWmiInstanceRegister to register the provider instance.
    wmiInstConfig.Register                    = TRUE;
    wmiInstConfig.EvtWmiInstanceQueryInstance = WmiQueryDataOfInstance;
    wmiInstConfig.EvtWmiInstanceExecuteMethod = WmiExecuteMethodOfInstance;
    DBGING("[ Wmi::WmiEvtDriverDeviceAdd ]\n-> Création du device framework..\n");

    ret = WdfDeviceCreate(&DeviceInit, &objAttr, &deviceObject);
    if(!NT_SUCCESS(ret))
    {
        DBGING("--> WdfDeviceCreate fail : 0x%x\n", ret);
        return ret;
    }

    DBGING("-> Initialisation des données..\n");
    pContext = GetWmiDeviceData(deviceObject);
    pContext->a = (PWmiT4pz)ExAllocatePoolWithTag(NonPagedPool, sizeof(WmiT4pz), 't4pz');
    pContext->a->nbMagic = 0;

    DBGING("-> Enregistrement des ressources MOFs..\n");
    ret = WdfDeviceAssignMofResourceName(deviceObject, &nameMof_u);
    if(!NT_SUCCESS(ret))
    {
        DBGING("--> WdfDeviceAssignMofRessourceName fail : 0x%x\n", ret);
        return ret;
    }

    DBGING("-> Création de l'instance..\n");
    ret = WdfWmiInstanceCreate(deviceObject, &wmiInstConfig, WDF_NO_OBJECT_ATTRIBUTES, WDF_NO_HANDLE);
    if(!NT_SUCCESS(ret))
    {
        DBGING("--> WdfWmiInstanceCreate fail : 0x%x\n", ret);
        return ret;
    }
    return ret;
}

//A driver's EvtWmiInstanceQueryInstance callback function copies a WMI provider's instance data into a buffer for delivery to a WMI client.
NTSTATUS
  WmiQueryDataOfInstance(
    WDFWMIINSTANCE WmiInstance,
    ULONG OutBufferSize,
    PVOID OutBuffer,
    PULONG BufferUsed
    )
{
    NTSTATUS ret = STATUS_SUCCESS;
    POBJECT_CONTEXT pCtx = GetWmiDeviceData(WdfWmiInstanceGetDevice(WmiInstance));
    DBGING("[ Wmi::WmiQueryDataOfInstance ]\n");

    memset(OutBuffer, 0, OutBufferSize);
    if(sizeof(WmiT4pz) <= OutBufferSize)
    {
        *BufferUsed = sizeof(WmiT4pz);
        RtlCopyMemory(OutBuffer, pCtx->a, sizeof(WmiT4pz));
    }
    else
    {
        DBGING("--> Fail in WmiQueryDataOfInstance : STATUS_BUFFER_TOO_SMALL\n");
        *BufferUsed = 0;
        ret = STATUS_BUFFER_TOO_SMALL;
    }
    return ret;
}

NTSTATUS
  WmiExecuteMethodOfInstance(
    WDFWMIINSTANCE WmiInstance,
    ULONG MethodId,
    ULONG InBufferSize,
    ULONG OutBufferSize,
    PVOID Buffer,
    PULONG BufferUsed
    )
{
    NTSTATUS ret = STATUS_SUCCESS;
    PWmiT4pz pT4pz = NULL;
    POBJECT_CONTEXT pCtx = GetWmiDeviceData(WdfWmiInstanceGetDevice(WmiInstance));
    DBGING("[ Wmi::WmiExecuteMethodOfInstance ]\n");

    switch(MethodId)
    {
        case Setter:
        {
            pCtx->a->nbMagic = 10;
            DBGING("-> Happy Halloween <-");
            //EVIL C0D3 :]>
            break;
        }

        default:
        {
            ret = STATUS_WMI_ITEMID_NOT_FOUND;
            DBGING("--> This MethodId isn't handle by this provider.\n");
            break;
        }
    }
    *BufferUsed = 0;
    return ret;
}

VOID
  WmiDestroyCallback(
    WDFDEVICE DeviceObject
    )
{
    POBJECT_CONTEXT pCtx = GetWmiDeviceData(DeviceObject);
    DBGING("[ Wmi::WmiSampDeviceEvtDestroyCallback ]\n");
    ExFreePoolWithTag(pCtx->a, 't4pz');
    pCtx->a = NULL;
    return;
}
