#include <Windows.h>
#include <detours.h>

typedef NTSTATUS (__stdcall *NtSetInformationThread_t)(
  _In_  HANDLE ThreadHandle,
  _In_  DWORD ThreadInformationClass,
  _In_  PVOID ThreadInformation,
  _In_  ULONG ThreadInformationLength
);

typedef NTSTATUS (__stdcall *NtDebugActiveProcess_t)(
  _In_  HANDLE ProcessHandle,
  _In_  HANDLE DebugHandle
);

typedef NTSTATUS (__stdcall *NtCreateProcess_t)(
  _Out_ PHANDLE 	ProcessHandle,
  _In_ ACCESS_MASK 	DesiredAccess,
  _In_opt_ DWORD 	ObjectAttributes,
  _In_ HANDLE 	ParentProcess,
  _In_ BOOLEAN 	InheritObjectTable,
  _In_opt_ HANDLE 	SectionHandle,
  _In_opt_ HANDLE 	DebugPort,
  _In_opt_ HANDLE 	ExceptionPort 
);	

static NtSetInformationThread_t TrueNtSetInformationThread = NULL;
static NtDebugActiveProcess_t TrueNtDebugActiveProcess = NULL;
static NtCreateProcess_t TrueNtCreateProcess = NULL;
static DWORD TrueSyscallStub = 0;

NTSTATUS __stdcall NtSetInformationThread(
  _In_  HANDLE ThreadHandle,
  _In_  DWORD ThreadInformationClass,
  _In_  PVOID ThreadInformation,
  _In_  ULONG ThreadInformationLength
)
{
#define ThreadHideFromDebugger 0x11
#define STATUS_SUCCESS 0
    if(ThreadInformationClass == ThreadHideFromDebugger)
    {
        OutputDebugString("[PreventThreadHideFromDebugger] Just prevented a ThreadHideFromDebugger");
        return STATUS_SUCCESS;
    }

    return TrueNtSetInformationThread(
        ThreadHandle,
        ThreadInformationClass,
        ThreadInformation,
        ThreadInformationLength
    );
}

NTSTATUS __stdcall NtDebugActiveProcess(
  _In_  HANDLE ProcessHandle,
  _In_  HANDLE DebugHandle
)
{
    OutputDebugString("[PreventThreadHideFromDebugger] NtDebugActiveProcess called");
    return STATUS_SUCCESS;
}

NTSTATUS __stdcall NtCreateProcess(
  _Out_ PHANDLE 	ProcessHandle,
  _In_ ACCESS_MASK 	DesiredAccess,
  _In_opt_ DWORD 	ObjectAttributes,
  _In_ HANDLE 	ParentProcess,
  _In_ BOOLEAN 	InheritObjectTable,
  _In_opt_ HANDLE 	SectionHandle,
  _In_opt_ HANDLE 	DebugPort,
  _In_opt_ HANDLE 	ExceptionPort 
)
{
    OutputDebugString("[PreventThreadHideFromDebugger] NtCreateProcess called");
    return STATUS_INVALID_PARAMETER;
}

VOID HookNtdllByEAT()
{
    DWORD i = 0, j = 0, old_prot = 0;
    PIMAGE_DOS_HEADER img_dos_hdr = (PIMAGE_DOS_HEADER)GetModuleHandle("ntdll");
    PIMAGE_NT_HEADERS32 img_nt_hdr = (PIMAGE_NT_HEADERS32)((PUCHAR)img_dos_hdr + img_dos_hdr->e_lfanew);
    PIMAGE_EXPORT_DIRECTORY img_export = (PIMAGE_EXPORT_DIRECTORY)((PUCHAR)img_dos_hdr + img_nt_hdr->OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_EXPORT].VirtualAddress);
    PDWORD export_name_table = (PDWORD)((PUCHAR)img_dos_hdr + img_export->AddressOfNames);
    PDWORD export_function_table = (PDWORD)((PUCHAR)img_dos_hdr + img_export->AddressOfFunctions);
    PWORD export_ordinal_table = (PWORD)((PUCHAR)img_dos_hdr + img_export->AddressOfNameOrdinals);
    for(i = 0; i < img_export->NumberOfFunctions; ++i)
    {
        const PCHAR export_name = (const PCHAR)img_dos_hdr + export_name_table[i];
        WORD id_func = export_ordinal_table[i];

        if(strcmp(export_name, "NtSetInformationThread") == 0)
        {
            OutputDebugString("[PreventThreadHideFromDebugger] Just EAT hooked NtSetInformationThread");
            VirtualProtect(
                &export_function_table[id_func],
                4,
                PAGE_READWRITE,
                &old_prot
            );
            export_function_table[id_func] = (DWORD)NtSetInformationThread - (DWORD)img_dos_hdr;
            VirtualProtect(
                &export_function_table[id_func],
                4,
                PAGE_READWRITE,
                &old_prot
            );
        }
        
        if(strcmp(export_name, "NtDebugActiveProcess") == 0)
        {
            OutputDebugString("[PreventThreadHideFromDebugger] Just EAT hooked NtDebugActiveProcess");
            VirtualProtect(
                &export_function_table[id_func],
                4,
                PAGE_READWRITE,
                &old_prot
            );
            export_function_table[id_func] = (DWORD)NtDebugActiveProcess - (DWORD)img_dos_hdr;
            VirtualProtect(
                &export_function_table[id_func],
                4,
                PAGE_READWRITE,
                &old_prot
            );
        }

        if(strcmp(export_name, "NtCreateProcess") == 0)
        {
            OutputDebugString("[PreventThreadHideFromDebugger] Just EAT hooked NtCreateProcess");
            VirtualProtect(
                &export_function_table[id_func],
                4,
                PAGE_READWRITE,
                &old_prot
            );
            export_function_table[id_func] = (DWORD)NtCreateProcess - (DWORD)img_dos_hdr;
            VirtualProtect(
                &export_function_table[id_func],
                4,
                PAGE_READWRITE,
                &old_prot
            );
        }
    }
}

VOID __stdcall MySyscallStub(DWORD syscall_idx)
{
    OutputDebugString("bra");
}

__declspec(naked) void MySyscallStub_()
{
    __asm
    {
        int 3
        pushad
        push eax
        call MySyscallStub
        popad
        jmp TrueSyscallStub
    }
}

VOID HookSyscallStubWow64()
{
    __asm
    {
        mov eax, fs:[0x18]
        mov ebx, [eax + 0xC0]
        mov TrueSyscallStub, ebx
        mov ebx, MySyscallStub_
        mov [eax + 0xC0], ebx
    }
}

__declspec(dllexport) BOOL __stdcall DllMain(
  _In_  HINSTANCE hinstDLL,
  _In_  DWORD fdwReason,
  _In_  LPVOID lpvReserved
)
{
    switch(fdwReason) 
    {
        case DLL_PROCESS_ATTACH:
        {
            // The loaded DLL should call the DetourRestoreAfterWith API to restores the contents of the import table.
            // DetourRestoreAfterWith();
            
            OutputDebugString("[PreventThreadHideFromDebugger] DLL_PROCESS_ATTACH");
            TrueNtSetInformationThread = (NtSetInformationThread_t)GetProcAddress(
                GetModuleHandle("ntdll"),
                "NtSetInformationThread"
            );
            
            TrueNtDebugActiveProcess = (NtDebugActiveProcess_t)GetProcAddress(
                GetModuleHandle("ntdll"),
                "NtDebugActiveProcess"
            );

            TrueNtCreateProcess = (NtCreateProcess_t)GetProcAddress(
                GetModuleHandle("ntdll"),
                "NtCreateProcess"
            );

            if(TrueNtSetInformationThread == NULL || TrueNtDebugActiveProcess == NULL || TrueNtCreateProcess == NULL)
                return FALSE;

            //HookNtdllByEAT();
            HookSyscallStubWow64();
            OutputDebugString("Syscall stub hooked");
            break;
        }

        case DLL_PROCESS_DETACH:
        {

            OutputDebugString("[PreventThreadHideFromDebugger] DLL_PROCESS_DETACH");
            break;
        }
    }

    return TRUE;  // Successful DLL_PROCESS_ATTACH.
}
