#ifndef MAIN_H_INCLUDED
#define MAIN_H_INCLUDED

#define T4PZ 1
#define _DBG_(_funct_, _code_error_) if(T4PZ)printf("\n--> Error @ %s : %x. <--\n", _funct_, _code_error_)
#define SIZE_BUF 256

#define white 7
#define redl  0xc
#define greenl 0xa

/* Pour la callback notification */
#define MSG_CONNECTED     1
#define MSG_DISCONNECTED  2

#define ERR_SUCCESS 0

typedef enum {
    kCFStringEncodingMacRoman = 0,
    kCFStringEncodingWindowsLatin1 = 0x0500, /* ANSI codepage 1252 */
    kCFStringEncodingISOLatin1 = 0x0201, /* ISO 8859-1 */
    kCFStringEncodingNextStepLatin = 0x0B01, /* NextStep encoding*/
    kCFStringEncodingASCII = 0x0600, /* 0..127 (in creating CFString, values greater than 0x7F are treated as corresponding Unicode value) */
    kCFStringEncodingUnicode = 0x0100, /* kTextEncodingUnicodeDefault  + kTextEncodingDefaultFormat (aka kUnicode16BitFormat) */
    kCFStringEncodingUTF8 = 0x08000100, /* kTextEncodingUnicodeDefault + kUnicodeUTF8Format */
    kCFStringEncodingNonLossyASCII = 0x0BFF /* 7bit Unicode variants used by Cocoa & Java */
} CFStringBuiltInEncodings;

typedef unsigned long long afc_file_ref;
typedef const struct __CFAllocator * CFAllocatorRef;
typedef const struct __CFString * CFStringRef;
const CFAllocatorRef kCFAllocatorDefault;
typedef signed long             SInt32;
typedef unsigned long           UInt32;
typedef unsigned int uint16_t;
typedef SInt32 CFIndex;
typedef UInt32 CFOptionFlags;
typedef const void *	(*CFAllocatorRetainCallBack)(const void *info);
typedef void		(*CFAllocatorReleaseCallBack)(const void *info);
typedef CFStringRef	(*CFAllocatorCopyDescriptionCallBack)(const void *info);
typedef void *		(*CFAllocatorAllocateCallBack)(CFIndex allocSize, CFOptionFlags hint, void *info);
typedef void *		(*CFAllocatorReallocateCallBack)(void *ptr, CFIndex newsize, CFOptionFlags hint, void *info);
typedef void		(*CFAllocatorDeallocateCallBack)(void *ptr, void *info);
typedef CFIndex		(*CFAllocatorPreferredSizeCallBack)(CFIndex size, CFOptionFlags hint, void *info);

typedef struct __CFRuntimeBase {
    void *_isa;
#if defined(__ppc__) || defined(__ppc64__)
    uint16_t _rc;
    uint16_t _info;
#elif defined(__i386__)
    uint16_t _info;
    uint16_t _rc;
#else
#error unknown architecture
#endif
} CFRuntimeBase;

typedef struct {
    CFIndex				version;
    void *				info;
    CFAllocatorRetainCallBack		retain;
    CFAllocatorReleaseCallBack		release;
    CFAllocatorCopyDescriptionCallBack	copyDescription;
    CFAllocatorAllocateCallBack		allocate;
    CFAllocatorReallocateCallBack	reallocate;
    CFAllocatorDeallocateCallBack	deallocate;
    CFAllocatorPreferredSizeCallBack	preferredSize;
} CFAllocatorContext;

struct __CFAllocator {

    CFRuntimeBase base;
    /* some stuff here */
    CFAllocatorRef allocator;
    CFAllocatorContext context;
};

struct __CFString {
    CFRuntimeBase base;
    union {
    struct {
        SInt32 length;
    } inline1;
    struct {
        void *buffer;
        UInt32 length;
        CFAllocatorRef contentsDeallocator;
    } externalImmutable1;
    struct {
        void *buffer;
        CFAllocatorRef contentsDeallocator;
    } externalImmutable2;
    struct {
        void *buffer;
        UInt32 length;
        UInt32 capacityFields;
        UInt32 gapEtc;
        CFAllocatorRef contentsAllocator;
    } externalMutable;
    } variants;
};


/* Structure that contains internal data used by AMDevice... functions. Never try
 * to access its members directly! Use AMDeviceCopyDeviceIdentifier,
 * AMDeviceGetConnectionID, AMDeviceRetain, AMDeviceRelease instead.
 */
typedef struct
{
   		unsigned int device_id;     /* 16 */
		unsigned int product_id;    /* 20 - set to AMD_IPHONE_PRODUCT_ID */
		char        *serial;        /* 24 - set to UDID, Unique Device Identifier */
		unsigned int unknown1;      /* 28 */
		unsigned int unknown2;      /* 32 - reference counter, increased by AMDeviceRetain, decreased by AMDeviceRelease*/
		unsigned int lockdown_conn; /* 36 */
		unsigned char unknown3[8];  /* 40 */
/*
#if (__ITUNES_VER > 740)
		unsigned int unknown4;      // 48 - used to store CriticalSection Handle
#endif
#if (__ITUNES_VER >= 800)
*/
		unsigned char unknown5[24];  /* 52 */
}AM_DEVICE, *PAM_DEVICE;

struct am_device_notification_callback_info;

typedef void (*AMDEVICENOTIFCALLBACK)(struct am_device_notification_callback_info*, int);

typedef struct
{
		unsigned int unknown0;                      /* 0 */
		unsigned int unknown1;                      /* 4 */
		unsigned int unknown2;                      /* 8 */
		AMDEVICENOTIFCALLBACK callback;             /* 12 */
		unsigned int cookie;                        /* 16 */
}AM_DEVICE_NOTIFICATION, *PAM_DEVICE_NOTIFICATION, **PPAM_DEVICE_NOTIFICATION;

typedef struct am_device_notification_callback_info
{
		PAM_DEVICE dev;         /* 0    device */
		unsigned int msg;       /* 4    one of ADNCI_MSG_* */
        PAM_DEVICE_NOTIFICATION subscription;
}AM_DEVICE_NOTIFICATION_CALLBACK_INFO, *PAM_DEVICE_NOTIFICATION_CALLBACK_INFO;


typedef struct afc_connection
{
		unsigned int handle;            /* 0 */
		unsigned int unknown0;          /* 4 */
		unsigned char unknown1;         /* 8 */
		unsigned char padding[3];       /* 9 */
		unsigned int unknown2;          /* 12 */
		unsigned int unknown3;          /* 16 */
		unsigned int unknown4;          /* 20 */
		unsigned int fs_block_size;     /* 24 */
		unsigned int sock_block_size;   /* 28: always 0x3c */
		unsigned int io_timeout;        /* 32: from AFCConnectionOpen, usu. 0 */
		void *afc_lock;                 /* 36 */
		unsigned int context;           /* 40 */
} AFCCONNECTION, *PAFCCONNECTION, **PPAFCCONNECTION;

typedef struct afc_dictionary
{
		unsigned char unknown[0];   /* size unknown */
} AFCDICTIONARY, *PAFCDICTIONARY, **PPAFCDICTIONARY;

typedef unsigned int (*AMDEVICECONNECT)(PAM_DEVICE);
typedef unsigned int (*AMDEVICENOTIFSUSC)(AMDEVICENOTIFCALLBACK, unsigned int, unsigned int, unsigned int, PPAM_DEVICE_NOTIFICATION);
typedef CFStringRef  (*AMDEVICECOPY)(PAM_DEVICE, CFStringRef, CFStringRef);
typedef unsigned int (*AMDEVICESTART)(PAM_DEVICE, CFStringRef, PPAFCCONNECTION, int*);
typedef CFStringRef  (*CFSTRINGCREATE)(CFAllocatorRef, char*, CFStringBuiltInEncodings);
typedef void         (*CFRELEASE)(CFStringRef);
typedef CFIndex      (*CFSTRINGGETLENGTH)(CFStringRef);
typedef BOOL         (*CFSTRINGGETCSTRING)(CFStringRef, char*, int, CFStringBuiltInEncodings);
typedef CFStringRef  (*CFSTRINGMAKE)(char*);
typedef unsigned int (*AFCREAD)(PAFCCONNECTION, afc_file_ref, void*, unsigned int*);
typedef unsigned int (*AFCCLOSE)(PAFCCONNECTION, afc_file_ref);
typedef unsigned int (*AFCCONNOPEN)(PAFCCONNECTION, unsigned int, PPAFCCONNECTION);
typedef unsigned int (*AFCOPEN)(PAFCCONNECTION, char*, unsigned long long int, afc_file_ref*);
typedef unsigned int (*AFCINFO)(PAFCCONNECTION, char*, PPAFCDICTIONARY);
typedef unsigned int (*AFCKEYREAD)(PAFCDICTIONARY, char**, char**);
typedef unsigned int (*AFCKEYCLOSE)(PAFCDICTIONARY);

BOOL readValue(PAM_DEVICE pDevice, char* name, char** buf, HINSTANCE imgBaseMD);
char* getItuneDllPath(char* buff, int* size);
void notificationCallBack(PAM_DEVICE_NOTIFICATION_CALLBACK_INFO pInfo, int x);
BOOL connectToPhone(HINSTANCE imgBase);
void printColor(char* str, int color);
BOOL getFileContent(char* fullPath, char* buff, unsigned int* size, HINSTANCE imgBase);
int getFileSize(char* fullPath, HINSTANCE imgBase);


#endif
