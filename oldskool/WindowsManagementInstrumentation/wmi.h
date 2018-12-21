#ifndef _WMI_
#define _WMI_

#include <initguid.h> // pour DEFINE_GUID

#define _DBG_ TRUE
#define DBGING if(_DBG_)DbgPrint

DEFINE_GUID(WmiT4pz_GUID, \
            0x15d851f1,0x6539,0x1337,0xa5,0x29,0x00,0xa0,0xc9,0x06,0x29,0x10);

//
// Method id definitions for WmiT4pz
#define Setter     1


//
DRIVER_UNLOAD Unload;
DRIVER_INITIALIZE DriverEntry;
EVT_WDF_DRIVER_DEVICE_ADD WmiEvtDriverDeviceAdd;
EVT_WDF_WMI_INSTANCE_QUERY_INSTANCE WmiQueryDataOfInstance;
EVT_WDF_WMI_INSTANCE_EXECUTE_METHOD WmiExecuteMethodOfInstance;
EVT_WDF_OBJECT_CONTEXT_DESTROY WmiDestroyCallback;
//

//
// Warning: Header for class WmiT4pz cannot be created
typedef struct _WmiT4pz
{
    //
    CHAR nbMagic;
    #define WmiT4pz_nbMagic_SIZE sizeof(CHAR)
    #define WmiT4pz_nbMagic_ID 1

} WmiT4pz, *PWmiT4pz;

typedef struct
{
    PWmiT4pz a;
} OBJECT_CONTEXT, *POBJECT_CONTEXT;

//Specifions notre accesseur pour accéder au context
WDF_DECLARE_CONTEXT_TYPE_WITH_NAME(OBJECT_CONTEXT, GetWmiDeviceData)


#endif
