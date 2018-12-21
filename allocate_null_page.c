#include <windows.h>
#include <stdio.h>

#if !defined(NT_SUCCESS)
#define NT_SUCCESS(Status) (((NTSTATUS)(Status)) >= 0)
#endif

#if !defined(STATUS_SUCCESS)
#define STATUS_SUCCESS ((NTSTATUS)0x00000000L)
#endif

extern NTSTATUS WINAPI NtAllocateVirtualMemory(
  __in     HANDLE ProcessHandle,
  __inout  PVOID *BaseAddress,
  __in     ULONG_PTR ZeroBits,
  __inout  PSIZE_T RegionSize,
  __in     ULONG AllocationType,
  __in     ULONG Protect
);


BOOL AllocateNullPage(DWORD size)
{
	NTSTATUS status;
	DWORD addr = 1, len = size;

	status = NtAllocateVirtualMemory(
        GetCurrentProcess(),
        (PVOID*)&addr,
        0,
        &len,
        MEM_RESERVE | MEM_COMMIT,
        PAGE_EXECUTE_READWRITE
    );

	if(!NT_SUCCESS(status))
	{
		printf("[-] Error with ZwAllocateVirtualMemory : 0x%.8x\n", status);
		return FALSE;
	}

	return TRUE;
}

int main()
{
    AllocateNullPage(0x100);
    return EXIT_SUCCESS;
}
