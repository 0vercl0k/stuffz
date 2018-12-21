#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include "main.h"

#define TESTFILE "/tapz.txt"

HANDLE hEvent = NULL;
PAM_DEVICE pDevice = NULL;
PAFCCONNECTION pAfcCo = NULL;

int main()
{
    int size = SIZE_BUF;
    HINSTANCE imgBaseDll = NULL;
    char fullPathItuneDll[SIZE_BUF] = {0};

    if(getItuneDllPath(fullPathItuneDll, &size) == NULL)
    {
        printf("--> getItuneDllPath() fail ;s. <--\n");
        return 0;
    }

    imgBaseDll = LoadLibrary(fullPathItuneDll);

    printf("-> Itunes' dll path found : %s\n", fullPathItuneDll);

    if(connectToPhone(imgBaseDll) == FALSE)
    {
        _DBG_("connectToPhone", 0);
        FreeLibrary(imgBaseDll);
        return 0;
    }


    FreeLibrary(imgBaseDll);
    return 1;
}

char* getItuneDllPath(char* buff, int* size)
{
    int ret = 0;
    HKEY hKey = 0;

    ret = RegOpenKeyEx(HKEY_LOCAL_MACHINE, "SOFTWARE\\Apple Inc.\\Apple Mobile Device Support\\Shared\\", 0, KEY_READ, &hKey);
    if(ret != ERROR_SUCCESS)
    {
        _DBG_("RegOpenKeyEx", ret);
        return NULL;
    }

    ret = RegQueryValueEx(hKey, "ItunesMobileDeviceDLL", NULL, NULL, (LPBYTE)buff, (LPDWORD)size);
    if(ret != ERROR_SUCCESS)
    {
        _DBG_("RegQueryValueEx", ret);
        return NULL;
    }

    ret = RegCloseKey(hKey);
    if(ret != ERROR_SUCCESS)
    {
        _DBG_("RegCloseKey", ret);
        return NULL;
    }

    return buff;
}

BOOL connectToPhone(HINSTANCE imgBase)
{
    int status = 0, size = 5;
    char* buf = NULL;
    PAM_DEVICE_NOTIFICATION pDeviceNotif = NULL;
    HINSTANCE imgBaseCoreF = GetModuleHandle("CoreFoundation.dll");

    AMDEVICECONNECT AMDeviceConnect         = (AMDEVICECONNECT)GetProcAddress(imgBase, "AMDeviceConnect"),
                    AMDeviceIsPaired        = (AMDEVICECONNECT)GetProcAddress(imgBase, "AMDeviceIsPaired"),
                    AMDevicePair            = (AMDEVICECONNECT)GetProcAddress(imgBase, "AMDevicePair"),
                    AMDeviceValidatePairing = (AMDEVICECONNECT)GetProcAddress(imgBase, "AMDeviceValidatePairing"),
                    AMDeviceStartSession    = (AMDEVICECONNECT)GetProcAddress(imgBase, "AMDeviceStartSession"),
                    AMDeviceDisconnect      = (AMDEVICECONNECT)GetProcAddress(imgBase, "AMDeviceDisconnect"),
                    AMDeviceStopSession     = (AMDEVICECONNECT)GetProcAddress(imgBase, "AMDeviceStopSession");

    AMDEVICENOTIFSUSC AMDeviceNotificationSubscribe = (AMDEVICENOTIFSUSC)GetProcAddress(imgBase, "AMDeviceNotificationSubscribe");
    AMDEVICESTART     AMDeviceStartService = (AMDEVICESTART)GetProcAddress(imgBase, "AMDeviceStartService");
    CFSTRINGMAKE      CFSringMakeConstantString = NULL;
    AFCCONNOPEN       AFCConnectionOpen = (AFCCONNOPEN)GetProcAddress(imgBase, "AFCConnectionOpen");
    PAFCCONNECTION    phAfc = NULL;

    if(imgBaseCoreF == 0)
    {
        _DBG_("connectToPhone::Unable to retrieve CoreFoundation address", (int)imgBaseCoreF);
        return FALSE;
    }

    CFSringMakeConstantString = (CFSTRINGMAKE)GetProcAddress(imgBaseCoreF, "__CFStringMakeConstantString");

    if(!AMDeviceConnect || !AMDeviceIsPaired || !AMDevicePair || !AMDeviceValidatePairing || !AMDeviceStartSession ||
       !AMDeviceDisconnect || !AMDeviceStopSession || !AMDeviceNotificationSubscribe || !AMDeviceStartService || !CFSringMakeConstantString || !AFCConnectionOpen)
       {
           _DBG_("connectToPhone::GetProcAddress", 0);
           return FALSE;
       }

    hEvent = CreateEvent(NULL, TRUE, FALSE, NULL);

    if(hEvent == NULL)
    {
        _DBG_("connectToPhone::CreateEvent", (int)hEvent);
        return FALSE;
    }


	/*  Registers a notification with the current run loop. The callback gets
	 *  copied into the notification struct, as well as being registered with the
	 *  current run loop. Cookie gets copied into cookie in the same.
	 *  (Cookie is a user info parameter that gets passed as an arg to
	 *  the callback) unused0 and unused1 are both 0 when iTunes calls this.
	 *
	 *  Never try to acces directly or copy contents of dev and subscription fields
	 *  in am_device_notification_callback_info. Treat them as abstract handles.
	 *  When done with connection use AMDeviceRelease to free resources allocated for am_device.
	 *
	 *  Returns:
	 *      MDERR_OK            if successful
	 *      MDERR_SYSCALL       if CFRunLoopAddSource() failed
	 *      MDERR_OUT_OF_MEMORY if we ran out of memory
	 */
    if( (status = AMDeviceNotificationSubscribe(notificationCallBack, 0, 0, 0, &pDeviceNotif)) != ERR_SUCCESS )
    {
        _DBG_("connectToPhone::AMDeviceNotificationSubscribe", status);
        return FALSE;
    }

    WaitForSingleObject(hEvent, INFINITE);

    printf("-> Iphone plugged in            ");
    printColor("[OK]", greenl);

    /*
      #define MDERR_OK                 ERR_SUCCESS -> 0
      #define MDERR_SYSCALL           (ERR_MOBILE_DEVICE | 0x01)
      #define MDERR_OUT_OF_MEMORY     (ERR_MOBILE_DEVICE | 0x03)
      #define MDERR_QUERY_FAILED      (ERR_MOBILE_DEVICE | 0x04)
      #define MDERR_INVALID_ARGUMENT  (ERR_MOBILE_DEVICE | 0x0b)
	  Connects to the iPhone. Pass in the am_device structure that the
	 *  notification callback will give to you.
	 *
	 *  Returns:
	 *      MDERR_OK                if successfully connected
	 *      MDERR_SYSCALL           if setsockopt() failed
	 *      MDERR_QUERY_FAILED      if the daemon query failed
	 *      MDERR_INVALID_ARGUMENT  if USBMuxConnectByPort returned 0xffffffff
	 */

    if( (status = AMDeviceConnect(pDevice)) != ERR_SUCCESS )
    {
        _DBG_(".\nconnectToPhone::AMDeviceConnect", status);
        return FALSE;
    }

    printf(".\n-> AMDeviceConnect              ");
    printColor("[OK]", greenl);

    if( ((status = AMDeviceIsPaired(pDevice))!= ERR_SUCCESS) )
    {
        printf(".\n-> AMDeviceIsPaired             ");
        printColor("[FAIL]", redl);
        printf(".\n-> Pairing..                    ");
        if( (status = AMDevicePair(pDevice)) != ERR_SUCCESS )
        {
            _DBG_("\nconnectToPhone::AMDevicePair", status);
            return FALSE;
        }

        printColor("[OK]", greenl);
    }

    if( (status = AMDeviceValidatePairing(pDevice)) != ERR_SUCCESS )
    {
        _DBG_(".\nconnectToPhone::AMDeviceValidatePairing", status);
        return FALSE;
    }

    printf(".\n-> Pairing validate             ");
    printColor("[OK]", greenl);

    if( (status = AMDeviceStartSession(pDevice)) != ERR_SUCCESS )
    {
        _DBG_(".\nconnectToPhone::AMDeviceStartSession", status);
        return FALSE;
    }

    printf(".\n-> Session started              ");
    printColor("[OK]", greenl);

    if(readValue(pDevice, "SerialNumber", &buf, imgBase))
        printf(".\n\n\t-> Serial Number dumped : '%s'.\n\n", buf);
    else
    {
        _DBG_(".\nconnectToPhone::readValue", 0);
        printf("-> Stopping session..           ");
        if( (status = AMDeviceStopSession(pDevice)) != ERR_SUCCESS )
        {
            _DBG_("\nconnectToPhone::AMDeviceStopSession", status);
            return FALSE;
        }

        printColor("[OK]", greenl);
        printf("\n-> Disconnecting from device..  ");
        if( (status = AMDeviceDisconnect(pDevice)) != ERR_SUCCESS )
        {
            _DBG_("\nconnectToPhone::AMDeviceDisconnect", status);
            return FALSE;
        }
        printColor("[OK]", greenl);
        printf("\n");
        if(buf != NULL)
            free(buf);

        return FALSE;
    }

    printf("-> Starting the afc service..");

    /*#define CFSTR(cStr)  __CFStringMakeConstantString("" cStr "")*/
    if( (status = AMDeviceStartService(pDevice, CFSringMakeConstantString("com.apple.afc"), &phAfc, NULL)) != ERR_SUCCESS)
    {
        _DBG_("connectToPhone::AMDeviceStartService", status);
        return FALSE;
    }
    printColor("   [OK]", greenl);
    printf(".\n-> Opening AFC..");

    if( (status = AFCConnectionOpen(phAfc, 0, &pAfcCo)) != ERR_SUCCESS)
    {
        _DBG_("connectToPhone::AFCConnectionOpen", status);
        return FALSE;
    }

    printColor("                [OK]", greenl);
    free(buf);
    buf = (char*)malloc(sizeof(char)*100);
    memset(buf, 0, 100);

    printf(".\n-> Dumping the file..");
    if(getFileContent(TESTFILE, buf, &size, imgBase))
        printf("\n%doctets -> '%s'\n", size, buf);

    printf("-> Stopping session..           ");
    if( (status = AMDeviceStopSession(pDevice)) != ERR_SUCCESS )
    {
        _DBG_("\nconnectToPhone::AMDeviceStopSession", status);
        return FALSE;
    }

    printColor("[OK]", greenl);
    printf(".\n-> Disconnecting from device..  ");

    if( (status = AMDeviceDisconnect(pDevice)) != ERR_SUCCESS )
    {
        _DBG_("\nconnectToPhone::AMDeviceDisconnect", status);
        return FALSE;
    }

    printColor("[OK]", greenl);
    printf(".\n");

    free(buf);
    return TRUE;
}

void notificationCallBack(PAM_DEVICE_NOTIFICATION_CALLBACK_INFO pInfo, int x)
{
    switch(pInfo->msg)
    {
        case MSG_CONNECTED:
            pDevice = pInfo->dev;
            SetEvent(hEvent);
            break;

        case MSG_DISCONNECTED:
            break;

        default:
        {
            _DBG_("notificationCallback::default in switch case", 0x1337);
            break;
        }
    }
    return;
}

BOOL readValue(PAM_DEVICE pDevice, char* name, char** buf, HINSTANCE imgBaseMD)
{
    static AMDEVICECOPY AMDeviceCopyValue = NULL;
    static CFSTRINGCREATE CFStringCreateWithCString = NULL;
    static CFRELEASE CFRelease = NULL;
    static CFSTRINGGETLENGTH CFStringGetLength = NULL;
    static CFSTRINGGETCSTRING CFStringGetCString = NULL;
    static HINSTANCE imgBaseCF = NULL;
    static BOOL firstTime = TRUE;
    CFIndex sizeStr = 0;
    CFStringRef str = NULL, key = NULL;

    /*it's the first time !*/
    if(firstTime == TRUE)
    {
        imgBaseCF = GetModuleHandle("CoreFoundation.dll");
        if(imgBaseCF == NULL)
        {
            _DBG_("readValue::CoreFoundation.dll loading", (unsigned int)imgBaseCF);
            return FALSE;
        }

        CFRelease                 = (CFRELEASE)GetProcAddress(imgBaseCF, "CFRelease");
        AMDeviceCopyValue         = (AMDEVICECOPY)GetProcAddress(imgBaseMD, "AMDeviceCopyValue");
        CFStringCreateWithCString = (CFSTRINGCREATE)GetProcAddress(imgBaseCF, "CFStringCreateWithCString");
        CFStringGetLength         = (CFSTRINGGETLENGTH)GetProcAddress(imgBaseCF, "CFStringGetLength");
        CFStringGetCString        = (CFSTRINGGETCSTRING)GetProcAddress(imgBaseCF, "CFStringGetCString");

        if(!CFRelease || !AMDeviceCopyValue || !CFStringCreateWithCString || !CFStringGetLength || !CFStringGetCString)
        {
            _DBG_("readValue::Functions loading", 0);
            return FALSE;
        }
        firstTime = FALSE;
    }

    key = CFStringCreateWithCString(kCFAllocatorDefault, name, kCFStringEncodingUTF8);

    if(key == NULL)
    {
        _DBG_("readValue::CFStringCreateWithCString", (unsigned int)key);
        return FALSE;
    }

	/* Reads various device settings. One of domain or cfstring arguments should be NULL.
         *
         * Possible values for cfstring:
	 * ActivationState
	 * ActivationStateAcknowledged
	 * BasebandBootloaderVersion
	 * BasebandVersion
	 * BluetoothAddress
	 * BuildVersion
	 * DeviceCertificate
	 * DeviceClass
	 * DeviceName
	 * DevicePublicKey
	 * FirmwareVersion
	 * HostAttached
	 * IntegratedCircuitCardIdentity
	 * InternationalMobileEquipmentIdentity
	 * InternationalMobileSubscriberIdentity
	 * ModelNumber
	 * PhoneNumber
	 * ProductType
	 * ProductVersion
	 * ProtocolVersion
	 * RegionInfo
	 * SBLockdownEverRegisteredKey
	 * SIMStatus
	 * SerialNumber
	 * SomebodySetTimeZone
	 * TimeIntervalSince1970
	 * TimeZone
	 * TimeZoneOffsetFromUTC
	 * TrustedHostAttached
	 * UniqueDeviceID
	 * Uses24HourClock
	 * WiFiAddress
	 * iTunesHasConnected
         *
         * Possible values for domain:
         * com.apple.mobile.battery
	 */
    str = AMDeviceCopyValue(pDevice, NULL, key);
    CFRelease(key);
    if(str == NULL)
    {
        _DBG_("readValue::AMDeviceCopyValue", (unsigned int)str);
        return FALSE;
    }

    sizeStr = CFStringGetLength(str);

    *buf = (char*)malloc((sizeof(char) * sizeStr)+1);
    memset(*buf, 0, (sizeof(char) * sizeStr)+1);

    if(CFStringGetCString(str, *buf, sizeStr+1, kCFStringEncodingUTF8) == FALSE)
    {
        _DBG_("readValue::CFStringGetCString", FALSE);
        free(*buf);
        return FALSE;
    }

    return TRUE;
}

BOOL getFileContent(char* fullPath, char* buff, unsigned int* size, HINSTANCE imgBase)
{
    static AFCOPEN AFCFileRefOpen   = NULL;
    static AFCREAD AFCFileRefRead   = NULL;
    static AFCCLOSE AFCFileRefClose = NULL;
    static BOOL firstTime = TRUE;
    int status = 0;
    afc_file_ref handle;

    if(firstTime)
    {
        AFCFileRefOpen  = (AFCOPEN)GetProcAddress(imgBase, "AFCFileRefOpen");
        AFCFileRefRead  = (AFCREAD)GetProcAddress(imgBase, "AFCFileRefRead");
        AFCFileRefClose = (AFCCLOSE)GetProcAddress(imgBase, "AFCFileRefClose");

        if(!AFCFileRefOpen || !AFCFileRefRead || !AFCFileRefClose)
        {
            _DBG_("getFileContent::Functions loading", 0);
            return FALSE;
        }
        firstTime = FALSE;
    }
    printf("Size of file : %d\n", getFileSize(fullPath, imgBase));
	/* Opens file for reading or writing without locking it in any way. afc_file_ref should not be shared between threads -
     * opening file in one thread and closing it in another will lead to possible crash.
	 * path - UTF-8 encoded absolute path to file
	 * mode 2 = read, mode 3 = write; None = 0
	 * ref - receives file handle
	 */
    if( (status = AFCFileRefOpen(pAfcCo, fullPath, 2, &handle)) != ERR_SUCCESS)
    {
        _DBG_("getFileContent::AFCFileRefOpen", status);
        return FALSE;
    }

    if( (status = AFCFileRefRead(pAfcCo, handle, buff, size)) != ERR_SUCCESS)
    {
        _DBG_("getFileContent::AFCFileRefRead", status);
        AFCFileRefClose(pAfcCo, handle);
        return FALSE;
    }

    printf("%s", buff);

    if( (status = AFCFileRefClose(pAfcCo, handle)) != ERR_SUCCESS)
    {
        _DBG_("getFileContent::AFCFileRefClose", status);
        return FALSE;
    }
    return TRUE;
}

void printColor(char* str, int color)
{
    HANDLE hStdout = GetStdHandle(STD_OUTPUT_HANDLE);
    SetConsoleTextAttribute(hStdout, color);
    printf("%s", str);
    SetConsoleTextAttribute(hStdout, white);
    return;
}

int getFileSize(char* fullPath, HINSTANCE imgBase)
{
    static AFCINFO AFCFileInfoOpen = NULL;
    static AFCKEYREAD AFCKeyValueRead = NULL;
    static AFCKEYCLOSE AFCKeyValueClose  = NULL;
    static BOOL firstTime = TRUE;
    char *key = NULL, *val = NULL;
    int size = 0, status = 0;
    PAFCDICTIONARY pDico = NULL;

    if(firstTime)
    {
        AFCFileInfoOpen = (AFCINFO)GetProcAddress(imgBase, "AFCFileInfoOpen");
        AFCKeyValueRead = (AFCKEYREAD)GetProcAddress(imgBase, "AFCKeyValueRead");
        AFCKeyValueClose = (AFCKEYCLOSE)GetProcAddress(imgBase, "AFCKeyValueClose");
        if(!AFCFileInfoOpen || !AFCKeyValueRead)
        {
            _DBG_("getFileSize::Functions loading", 0);
            return 0;
        }
        firstTime = FALSE;
    }

    if( (status = AFCFileInfoOpen(pAfcCo, fullPath, &pDico)) != ERR_SUCCESS)
    {
        _DBG_("getFileSize::AFCFileInfoOpen", status);
        return 0;
    }

    while(1)
    {
        /* Reads next entry from dictionary. When last entry is read, function returns NULL in key argument
            Possible keys:
	     "st_size":     val - size in bytes
	     "st_blocks":   val - size in blocks
	     "st_nlink":    val - number of hardlinks
	     "st_ifmt":     val - "S_IFDIR" for folders
	                        "S_IFLNK" for symlinks
	     "LinkTarget":  val - path to symlink target
        */
        AFCKeyValueRead(pDico, &key, &val);
        if (!key || !val)
            break;

        if (!strcmp(key, "st_size"))
        {
            sscanf(val, "%u", &size);
            AFCKeyValueClose(pDico);
            return size;
        }
    }
    AFCKeyValueClose(pDico);
    return 0;
}
