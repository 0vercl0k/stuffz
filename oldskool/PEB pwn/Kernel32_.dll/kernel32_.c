#include <windows.h>
#define DLLEXPORT __declspec (dllexport)
#define FAKE_LIB "kernel32_.dll"
unsigned long tmp;

#define JMP( lib, func )            \
   __asm                            \
   (   "pushad                \n"   \
       " push edx             \n"   \
       " push %1              \n"   \
       " call eax             \n"   \
       " pop edx              \n"   \
       " push %2              \n"   \
       " push eax             \n"   \
       " call edx             \n"   \
       " mov %4, eax          \n"   \
       " popad                \n"   \
                                    \
       : :                          \
       "a" (GetModuleHandle) ,      \
       "g" (lib)             ,      \
       "g" (func)            ,      \
       "d" (GetProcAddress)  ,      \
       "g" (tmp)                    \
    );                              \
   asm ( "jmp %0" : : "g" (tmp) );
   
DLLEXPORT void _ActivateActCtx(void)
{
	JMP(FAKE_LIB, 1);
}

DLLEXPORT void _AddAtomA(void)
{
	JMP(FAKE_LIB, 2);
}

DLLEXPORT void _AddAtomW(void)
{
	JMP(FAKE_LIB, 3);
}

DLLEXPORT void _AddConsoleAliasA(void)
{
	JMP(FAKE_LIB, 4);
}

DLLEXPORT void _AddConsoleAliasW(void)
{
	JMP(FAKE_LIB, 5);
}

DLLEXPORT void _AddLocalAlternateComputerNameA(void)
{
	JMP(FAKE_LIB, 6);
}

DLLEXPORT void _AddLocalAlternateComputerNameW(void)
{
	JMP(FAKE_LIB, 7);
}

DLLEXPORT void _AddRefActCtx(void)
{
	JMP(FAKE_LIB, 8);
}

DLLEXPORT void _AddVectoredExceptionHandler(void)
{
	JMP(FAKE_LIB, 9);
}

DLLEXPORT void _AllocConsole(void)
{
	JMP(FAKE_LIB, 10);
}

DLLEXPORT void _AllocateUserPhysicalPages(void)
{
	JMP(FAKE_LIB, 11);
}

DLLEXPORT void _AreFileApisANSI(void)
{
	JMP(FAKE_LIB, 12);
}

DLLEXPORT void _AssignProcessToJobObject(void)
{
	JMP(FAKE_LIB, 13);
}

DLLEXPORT void _AttachConsole(void)
{
	JMP(FAKE_LIB, 14);
}

DLLEXPORT void _BackupRead(void)
{
	JMP(FAKE_LIB, 15);
}

DLLEXPORT void _BackupSeek(void)
{
	JMP(FAKE_LIB, 16);
}

DLLEXPORT void _BackupWrite(void)
{
	JMP(FAKE_LIB, 17);
}

DLLEXPORT void _BaseCheckAppcompatCache(void)
{
	JMP(FAKE_LIB, 18);
}

DLLEXPORT void _BaseCleanupAppcompatCache(void)
{
	JMP(FAKE_LIB, 19);
}

DLLEXPORT void _BaseCleanupAppcompatCacheSupport(void)
{
	JMP(FAKE_LIB, 20);
}

DLLEXPORT void _BaseDumpAppcompatCache(void)
{
	JMP(FAKE_LIB, 21);
}

DLLEXPORT void _BaseFlushAppcompatCache(void)
{
	JMP(FAKE_LIB, 22);
}

DLLEXPORT void _BaseInitAppcompatCache(void)
{
	JMP(FAKE_LIB, 23);
}

DLLEXPORT void _BaseInitAppcompatCacheSupport(void)
{
	JMP(FAKE_LIB, 24);
}

DLLEXPORT void _BaseProcessInitPostImport(void)
{
	JMP(FAKE_LIB, 25);
}

DLLEXPORT void _BaseQueryModuleData(void)
{
	JMP(FAKE_LIB, 26);
}

DLLEXPORT void _BaseUpdateAppcompatCache(void)
{
	JMP(FAKE_LIB, 27);
}

DLLEXPORT void _BasepCheckWinSaferRestrictions(void)
{
	JMP(FAKE_LIB, 28);
}
/*
DLLEXPORT void _Beep(void)
{
	JMP(FAKE_LIB, 29);
}
*/
DLLEXPORT void _BeginUpdateResourceA(void)
{
	JMP(FAKE_LIB, 30);
}

DLLEXPORT void _BeginUpdateResourceW(void)
{
	JMP(FAKE_LIB, 31);
}

DLLEXPORT void _BindIoCompletionCallback(void)
{
	JMP(FAKE_LIB, 32);
}

DLLEXPORT void _BuildCommDCBA(void)
{
	JMP(FAKE_LIB, 33);
}

DLLEXPORT void _BuildCommDCBAndTimeoutsA(void)
{
	JMP(FAKE_LIB, 34);
}

DLLEXPORT void _BuildCommDCBAndTimeoutsW(void)
{
	JMP(FAKE_LIB, 35);
}

DLLEXPORT void _BuildCommDCBW(void)
{
	JMP(FAKE_LIB, 36);
}

DLLEXPORT void _CallNamedPipeA(void)
{
	JMP(FAKE_LIB, 37);
}

DLLEXPORT void _CallNamedPipeW(void)
{
	JMP(FAKE_LIB, 38);
}

DLLEXPORT void _CancelDeviceWakeupRequest(void)
{
	JMP(FAKE_LIB, 39);
}

DLLEXPORT void _CancelIo(void)
{
	JMP(FAKE_LIB, 40);
}

DLLEXPORT void _CancelTimerQueueTimer(void)
{
	JMP(FAKE_LIB, 41);
}

DLLEXPORT void _CancelWaitableTimer(void)
{
	JMP(FAKE_LIB, 42);
}

DLLEXPORT void _ChangeTimerQueueTimer(void)
{
	JMP(FAKE_LIB, 43);
}

DLLEXPORT void _CheckNameLegalDOS8Dot3A(void)
{
	JMP(FAKE_LIB, 44);
}

DLLEXPORT void _CheckNameLegalDOS8Dot3W(void)
{
	JMP(FAKE_LIB, 45);
}

DLLEXPORT void _CheckRemoteDebuggerPresent(void)
{
	JMP(FAKE_LIB, 46);
}

DLLEXPORT void _ClearCommBreak(void)
{
	JMP(FAKE_LIB, 47);
}

DLLEXPORT void _ClearCommError(void)
{
	JMP(FAKE_LIB, 48);
}

DLLEXPORT void _CloseConsoleHandle(void)
{
	JMP(FAKE_LIB, 49);
}

DLLEXPORT void _CloseHandle(void)
{
	JMP(FAKE_LIB, 50);
}

DLLEXPORT void _CloseProfileUserMapping(void)
{
	JMP(FAKE_LIB, 51);
}

DLLEXPORT void _CmdBatNotification(void)
{
	JMP(FAKE_LIB, 52);
}

DLLEXPORT void _CommConfigDialogA(void)
{
	JMP(FAKE_LIB, 53);
}

DLLEXPORT void _CommConfigDialogW(void)
{
	JMP(FAKE_LIB, 54);
}

DLLEXPORT void _CompareFileTime(void)
{
	JMP(FAKE_LIB, 55);
}

DLLEXPORT void _CompareStringA(void)
{
	JMP(FAKE_LIB, 56);
}

DLLEXPORT void _CompareStringW(void)
{
	JMP(FAKE_LIB, 57);
}

DLLEXPORT void _ConnectNamedPipe(void)
{
	JMP(FAKE_LIB, 58);
}

DLLEXPORT void _ConsoleMenuControl(void)
{
	JMP(FAKE_LIB, 59);
}

DLLEXPORT void _ContinueDebugEvent(void)
{
	JMP(FAKE_LIB, 60);
}

DLLEXPORT void _ConvertDefaultLocale(void)
{
	JMP(FAKE_LIB, 61);
}

DLLEXPORT void _ConvertFiberToThread(void)
{
	JMP(FAKE_LIB, 62);
}

DLLEXPORT void _ConvertThreadToFiber(void)
{
	JMP(FAKE_LIB, 63);
}

DLLEXPORT void _CopyFileA(void)
{
	JMP(FAKE_LIB, 64);
}

DLLEXPORT void _CopyFileExA(void)
{
	JMP(FAKE_LIB, 65);
}

DLLEXPORT void _CopyFileExW(void)
{
	JMP(FAKE_LIB, 66);
}

DLLEXPORT void _CopyFileW(void)
{
	JMP(FAKE_LIB, 67);
}

DLLEXPORT void _CopyLZFile(void)
{
	JMP(FAKE_LIB, 68);
}

DLLEXPORT void _CreateActCtxA(void)
{
	JMP(FAKE_LIB, 69);
}

DLLEXPORT void _CreateActCtxW(void)
{
	JMP(FAKE_LIB, 70);
}

DLLEXPORT void _CreateConsoleScreenBuffer(void)
{
	JMP(FAKE_LIB, 71);
}

DLLEXPORT void _CreateDirectoryA(void)
{
	JMP(FAKE_LIB, 72);
}

DLLEXPORT void _CreateDirectoryExA(void)
{
	JMP(FAKE_LIB, 73);
}

DLLEXPORT void _CreateDirectoryExW(void)
{
	JMP(FAKE_LIB, 74);
}

DLLEXPORT void _CreateDirectoryW(void)
{
	JMP(FAKE_LIB, 75);
}

DLLEXPORT void _CreateEventA(void)
{
	JMP(FAKE_LIB, 76);
}

DLLEXPORT void _CreateEventW(void)
{
	JMP(FAKE_LIB, 77);
}

DLLEXPORT void _CreateFiber(void)
{
	JMP(FAKE_LIB, 78);
}

DLLEXPORT void _CreateFiberEx(void)
{
	JMP(FAKE_LIB, 79);
}

DLLEXPORT void _CreateFileA(void)
{
	JMP(FAKE_LIB, 80);
}

DLLEXPORT void _CreateFileMappingA(void)
{
	JMP(FAKE_LIB, 81);
}

DLLEXPORT void _CreateFileMappingW(void)
{
	JMP(FAKE_LIB, 82);
}

DLLEXPORT void _CreateFileW(void)
{
	JMP(FAKE_LIB, 83);
}

DLLEXPORT void _CreateHardLinkA(void)
{
	JMP(FAKE_LIB, 84);
}

DLLEXPORT void _CreateHardLinkW(void)
{
	JMP(FAKE_LIB, 85);
}

DLLEXPORT void _CreateIoCompletionPort(void)
{
	JMP(FAKE_LIB, 86);
}

DLLEXPORT void _CreateJobObjectA(void)
{
	JMP(FAKE_LIB, 87);
}

DLLEXPORT void _CreateJobObjectW(void)
{
	JMP(FAKE_LIB, 88);
}

DLLEXPORT void _CreateJobSet(void)
{
	JMP(FAKE_LIB, 89);
}

DLLEXPORT void _CreateMailslotA(void)
{
	JMP(FAKE_LIB, 90);
}

DLLEXPORT void _CreateMailslotW(void)
{
	JMP(FAKE_LIB, 91);
}

DLLEXPORT void _CreateMemoryResourceNotification(void)
{
	JMP(FAKE_LIB, 92);
}

DLLEXPORT void _CreateMutexA(void)
{
	JMP(FAKE_LIB, 93);
}

DLLEXPORT void _CreateMutexW(void)
{
	JMP(FAKE_LIB, 94);
}

DLLEXPORT void _CreateNamedPipeA(void)
{
	JMP(FAKE_LIB, 95);
}

DLLEXPORT void _CreateNamedPipeW(void)
{
	JMP(FAKE_LIB, 96);
}

DLLEXPORT void _CreateNlsSecurityDescriptor(void)
{
	JMP(FAKE_LIB, 97);
}

DLLEXPORT void _CreatePipe(void)
{
	JMP(FAKE_LIB, 98);
}

DLLEXPORT void _CreateProcessA(void)
{
	JMP(FAKE_LIB, 99);
}

DLLEXPORT void _CreateProcessInternalA(void)
{
	JMP(FAKE_LIB, 100);
}

DLLEXPORT void _CreateProcessInternalW(void)
{
	JMP(FAKE_LIB, 101);
}

DLLEXPORT void _CreateProcessInternalWSecure(void)
{
	JMP(FAKE_LIB, 102);
}

DLLEXPORT void _CreateProcessW(void)
{
	JMP(FAKE_LIB, 103);
}

DLLEXPORT void _CreateRemoteThread(void)
{
	JMP(FAKE_LIB, 104);
}

DLLEXPORT void _CreateSemaphoreA(void)
{
	JMP(FAKE_LIB, 105);
}

DLLEXPORT void _CreateSemaphoreW(void)
{
	JMP(FAKE_LIB, 106);
}

DLLEXPORT void _CreateSocketHandle(void)
{
	JMP(FAKE_LIB, 107);
}

DLLEXPORT void _CreateTapePartition(void)
{
	JMP(FAKE_LIB, 108);
}

DLLEXPORT void _CreateThread(void)
{
	JMP(FAKE_LIB, 109);
}

DLLEXPORT void _CreateTimerQueue(void)
{
	JMP(FAKE_LIB, 110);
}

DLLEXPORT void _CreateTimerQueueTimer(void)
{
	JMP(FAKE_LIB, 111);
}

DLLEXPORT void _CreateToolhelp32Snapshot(void)
{
	JMP(FAKE_LIB, 112);
}

DLLEXPORT void _CreateVirtualBuffer(void)
{
	JMP(FAKE_LIB, 113);
}

DLLEXPORT void _CreateWaitableTimerA(void)
{
	JMP(FAKE_LIB, 114);
}

DLLEXPORT void _CreateWaitableTimerW(void)
{
	JMP(FAKE_LIB, 115);
}

DLLEXPORT void _DeactivateActCtx(void)
{
	JMP(FAKE_LIB, 116);
}

DLLEXPORT void _DebugActiveProcess(void)
{
	JMP(FAKE_LIB, 117);
}

DLLEXPORT void _DebugActiveProcessStop(void)
{
	JMP(FAKE_LIB, 118);
}

DLLEXPORT void _DebugBreak(void)
{
	JMP(FAKE_LIB, 119);
}

DLLEXPORT void _DebugBreakProcess(void)
{
	JMP(FAKE_LIB, 120);
}

DLLEXPORT void _DebugSetProcessKillOnExit(void)
{
	JMP(FAKE_LIB, 121);
}

DLLEXPORT void _DecodePointer(void)
{
	JMP(FAKE_LIB, 122);
}

DLLEXPORT void _DecodeSystemPointer(void)
{
	JMP(FAKE_LIB, 123);
}

DLLEXPORT void _DefineDosDeviceA(void)
{
	JMP(FAKE_LIB, 124);
}

DLLEXPORT void _DefineDosDeviceW(void)
{
	JMP(FAKE_LIB, 125);
}

DLLEXPORT void _DelayLoadFailureHook(void)
{
	JMP(FAKE_LIB, 126);
}

DLLEXPORT void _DeleteAtom(void)
{
	JMP(FAKE_LIB, 127);
}

DLLEXPORT void _DeleteCriticalSection(void)
{
	JMP(FAKE_LIB, 128);
}

DLLEXPORT void _DeleteFiber(void)
{
	JMP(FAKE_LIB, 129);
}

DLLEXPORT void _DeleteFileA(void)
{
	JMP(FAKE_LIB, 130);
}

DLLEXPORT void _DeleteFileW(void)
{
	JMP(FAKE_LIB, 131);
}

DLLEXPORT void _DeleteTimerQueue(void)
{
	JMP(FAKE_LIB, 132);
}

DLLEXPORT void _DeleteTimerQueueEx(void)
{
	JMP(FAKE_LIB, 133);
}

DLLEXPORT void _DeleteTimerQueueTimer(void)
{
	JMP(FAKE_LIB, 134);
}

DLLEXPORT void _DeleteVolumeMountPointA(void)
{
	JMP(FAKE_LIB, 135);
}

DLLEXPORT void _DeleteVolumeMountPointW(void)
{
	JMP(FAKE_LIB, 136);
}

DLLEXPORT void _DeviceIoControl(void)
{
	JMP(FAKE_LIB, 137);
}

DLLEXPORT void _DisableThreadLibraryCalls(void)
{
	JMP(FAKE_LIB, 138);
}

DLLEXPORT void _DisconnectNamedPipe(void)
{
	JMP(FAKE_LIB, 139);
}

DLLEXPORT void _DnsHostnameToComputerNameA(void)
{
	JMP(FAKE_LIB, 140);
}

DLLEXPORT void _DnsHostnameToComputerNameW(void)
{
	JMP(FAKE_LIB, 141);
}

DLLEXPORT void _DosDateTimeToFileTime(void)
{
	JMP(FAKE_LIB, 142);
}

DLLEXPORT void _DosPathToSessionPathA(void)
{
	JMP(FAKE_LIB, 143);
}

DLLEXPORT void _DosPathToSessionPathW(void)
{
	JMP(FAKE_LIB, 144);
}

DLLEXPORT void _DuplicateConsoleHandle(void)
{
	JMP(FAKE_LIB, 145);
}

DLLEXPORT void _DuplicateHandle(void)
{
	JMP(FAKE_LIB, 146);
}

DLLEXPORT void _EncodePointer(void)
{
	JMP(FAKE_LIB, 147);
}

DLLEXPORT void _EncodeSystemPointer(void)
{
	JMP(FAKE_LIB, 148);
}

DLLEXPORT void _EndUpdateResourceA(void)
{
	JMP(FAKE_LIB, 149);
}

DLLEXPORT void _EndUpdateResourceW(void)
{
	JMP(FAKE_LIB, 150);
}

DLLEXPORT void _EnterCriticalSection(void)
{
	JMP(FAKE_LIB, 151);
}

DLLEXPORT void _EnumCalendarInfoA(void)
{
	JMP(FAKE_LIB, 152);
}

DLLEXPORT void _EnumCalendarInfoExA(void)
{
	JMP(FAKE_LIB, 153);
}

DLLEXPORT void _EnumCalendarInfoExW(void)
{
	JMP(FAKE_LIB, 154);
}

DLLEXPORT void _EnumCalendarInfoW(void)
{
	JMP(FAKE_LIB, 155);
}

DLLEXPORT void _EnumDateFormatsA(void)
{
	JMP(FAKE_LIB, 156);
}

DLLEXPORT void _EnumDateFormatsExA(void)
{
	JMP(FAKE_LIB, 157);
}

DLLEXPORT void _EnumDateFormatsExW(void)
{
	JMP(FAKE_LIB, 158);
}

DLLEXPORT void _EnumDateFormatsW(void)
{
	JMP(FAKE_LIB, 159);
}

DLLEXPORT void _EnumLanguageGroupLocalesA(void)
{
	JMP(FAKE_LIB, 160);
}

DLLEXPORT void _EnumLanguageGroupLocalesW(void)
{
	JMP(FAKE_LIB, 161);
}

DLLEXPORT void _EnumResourceLanguagesA(void)
{
	JMP(FAKE_LIB, 162);
}

DLLEXPORT void _EnumResourceLanguagesW(void)
{
	JMP(FAKE_LIB, 163);
}

DLLEXPORT void _EnumResourceNamesA(void)
{
	JMP(FAKE_LIB, 164);
}

DLLEXPORT void _EnumResourceNamesW(void)
{
	JMP(FAKE_LIB, 165);
}

DLLEXPORT void _EnumResourceTypesA(void)
{
	JMP(FAKE_LIB, 166);
}

DLLEXPORT void _EnumResourceTypesW(void)
{
	JMP(FAKE_LIB, 167);
}

DLLEXPORT void _EnumSystemCodePagesA(void)
{
	JMP(FAKE_LIB, 168);
}

DLLEXPORT void _EnumSystemCodePagesW(void)
{
	JMP(FAKE_LIB, 169);
}

DLLEXPORT void _EnumSystemGeoID(void)
{
	JMP(FAKE_LIB, 170);
}

DLLEXPORT void _EnumSystemLanguageGroupsA(void)
{
	JMP(FAKE_LIB, 171);
}

DLLEXPORT void _EnumSystemLanguageGroupsW(void)
{
	JMP(FAKE_LIB, 172);
}

DLLEXPORT void _EnumSystemLocalesA(void)
{
	JMP(FAKE_LIB, 173);
}

DLLEXPORT void _EnumSystemLocalesW(void)
{
	JMP(FAKE_LIB, 174);
}

DLLEXPORT void _EnumTimeFormatsA(void)
{
	JMP(FAKE_LIB, 175);
}

DLLEXPORT void _EnumTimeFormatsW(void)
{
	JMP(FAKE_LIB, 176);
}

DLLEXPORT void _EnumUILanguagesA(void)
{
	JMP(FAKE_LIB, 177);
}

DLLEXPORT void _EnumUILanguagesW(void)
{
	JMP(FAKE_LIB, 178);
}

DLLEXPORT void _EnumerateLocalComputerNamesA(void)
{
	JMP(FAKE_LIB, 179);
}

DLLEXPORT void _EnumerateLocalComputerNamesW(void)
{
	JMP(FAKE_LIB, 180);
}

DLLEXPORT void _EraseTape(void)
{
	JMP(FAKE_LIB, 181);
}

DLLEXPORT void _EscapeCommFunction(void)
{
	JMP(FAKE_LIB, 182);
}

DLLEXPORT void _ExitProcess(void)
{
	JMP(FAKE_LIB, 183);
}

DLLEXPORT void _ExitThread(void)
{
	JMP(FAKE_LIB, 184);
}

DLLEXPORT void _ExitVDM(void)
{
	JMP(FAKE_LIB, 185);
}

DLLEXPORT void _ExpandEnvironmentStringsA(void)
{
	JMP(FAKE_LIB, 186);
}

DLLEXPORT void _ExpandEnvironmentStringsW(void)
{
	JMP(FAKE_LIB, 187);
}

DLLEXPORT void _ExpungeConsoleCommandHistoryA(void)
{
	JMP(FAKE_LIB, 188);
}

DLLEXPORT void _ExpungeConsoleCommandHistoryW(void)
{
	JMP(FAKE_LIB, 189);
}

DLLEXPORT void _ExtendVirtualBuffer(void)
{
	JMP(FAKE_LIB, 190);
}

DLLEXPORT void _FatalAppExitA(void)
{
	JMP(FAKE_LIB, 191);
}

DLLEXPORT void _FatalAppExitW(void)
{
	JMP(FAKE_LIB, 192);
}

DLLEXPORT void _FatalExit(void)
{
	JMP(FAKE_LIB, 193);
}

DLLEXPORT void _FileTimeToDosDateTime(void)
{
	JMP(FAKE_LIB, 194);
}

DLLEXPORT void _FileTimeToLocalFileTime(void)
{
	JMP(FAKE_LIB, 195);
}

DLLEXPORT void _FileTimeToSystemTime(void)
{
	JMP(FAKE_LIB, 196);
}

DLLEXPORT void _FillConsoleOutputAttribute(void)
{
	JMP(FAKE_LIB, 197);
}

DLLEXPORT void _FillConsoleOutputCharacterA(void)
{
	JMP(FAKE_LIB, 198);
}

DLLEXPORT void _FillConsoleOutputCharacterW(void)
{
	JMP(FAKE_LIB, 199);
}

DLLEXPORT void _FindActCtxSectionGuid(void)
{
	JMP(FAKE_LIB, 200);
}

DLLEXPORT void _FindActCtxSectionStringA(void)
{
	JMP(FAKE_LIB, 201);
}

DLLEXPORT void _FindActCtxSectionStringW(void)
{
	JMP(FAKE_LIB, 202);
}

DLLEXPORT void _FindAtomA(void)
{
	JMP(FAKE_LIB, 203);
}

DLLEXPORT void _FindAtomW(void)
{
	JMP(FAKE_LIB, 204);
}

DLLEXPORT void _FindClose(void)
{
	JMP(FAKE_LIB, 205);
}

DLLEXPORT void _FindCloseChangeNotification(void)
{
	JMP(FAKE_LIB, 206);
}

DLLEXPORT void _FindFirstChangeNotificationA(void)
{
	JMP(FAKE_LIB, 207);
}

DLLEXPORT void _FindFirstChangeNotificationW(void)
{
	JMP(FAKE_LIB, 208);
}

DLLEXPORT void _FindFirstFileA(void)
{
	JMP(FAKE_LIB, 209);
}

DLLEXPORT void _FindFirstFileExA(void)
{
	JMP(FAKE_LIB, 210);
}

DLLEXPORT void _FindFirstFileExW(void)
{
	JMP(FAKE_LIB, 211);
}

DLLEXPORT void _FindFirstFileW(void)
{
	JMP(FAKE_LIB, 212);
}

DLLEXPORT void _FindFirstVolumeA(void)
{
	JMP(FAKE_LIB, 213);
}

DLLEXPORT void _FindFirstVolumeMountPointA(void)
{
	JMP(FAKE_LIB, 214);
}

DLLEXPORT void _FindFirstVolumeMountPointW(void)
{
	JMP(FAKE_LIB, 215);
}

DLLEXPORT void _FindFirstVolumeW(void)
{
	JMP(FAKE_LIB, 216);
}

DLLEXPORT void _FindNextChangeNotification(void)
{
	JMP(FAKE_LIB, 217);
}

DLLEXPORT void _FindNextFileA(void)
{
	JMP(FAKE_LIB, 218);
}

DLLEXPORT void _FindNextFileW(void)
{
	JMP(FAKE_LIB, 219);
}

DLLEXPORT void _FindNextVolumeA(void)
{
	JMP(FAKE_LIB, 220);
}

DLLEXPORT void _FindNextVolumeMountPointA(void)
{
	JMP(FAKE_LIB, 221);
}

DLLEXPORT void _FindNextVolumeMountPointW(void)
{
	JMP(FAKE_LIB, 222);
}

DLLEXPORT void _FindNextVolumeW(void)
{
	JMP(FAKE_LIB, 223);
}

DLLEXPORT void _FindResourceA(void)
{
	JMP(FAKE_LIB, 224);
}

DLLEXPORT void _FindResourceExA(void)
{
	JMP(FAKE_LIB, 225);
}

DLLEXPORT void _FindResourceExW(void)
{
	JMP(FAKE_LIB, 226);
}

DLLEXPORT void _FindResourceW(void)
{
	JMP(FAKE_LIB, 227);
}

DLLEXPORT void _FindVolumeClose(void)
{
	JMP(FAKE_LIB, 228);
}

DLLEXPORT void _FindVolumeMountPointClose(void)
{
	JMP(FAKE_LIB, 229);
}

DLLEXPORT void _FlushConsoleInputBuffer(void)
{
	JMP(FAKE_LIB, 230);
}

DLLEXPORT void _FlushFileBuffers(void)
{
	JMP(FAKE_LIB, 231);
}

DLLEXPORT void _FlushInstructionCache(void)
{
	JMP(FAKE_LIB, 232);
}

DLLEXPORT void _FlushViewOfFile(void)
{
	JMP(FAKE_LIB, 233);
}

DLLEXPORT void _FoldStringA(void)
{
	JMP(FAKE_LIB, 234);
}

DLLEXPORT void _FoldStringW(void)
{
	JMP(FAKE_LIB, 235);
}

DLLEXPORT void _FormatMessageA(void)
{
	JMP(FAKE_LIB, 236);
}

DLLEXPORT void _FormatMessageW(void)
{
	JMP(FAKE_LIB, 237);
}

DLLEXPORT void _FreeConsole(void)
{
	JMP(FAKE_LIB, 238);
}

DLLEXPORT void _FreeEnvironmentStringsA(void)
{
	JMP(FAKE_LIB, 239);
}

DLLEXPORT void _FreeEnvironmentStringsW(void)
{
	JMP(FAKE_LIB, 240);
}

DLLEXPORT void _FreeLibrary(void)
{
	JMP(FAKE_LIB, 241);
}

DLLEXPORT void _FreeLibraryAndExitThread(void)
{
	JMP(FAKE_LIB, 242);
}

DLLEXPORT void _FreeResource(void)
{
	JMP(FAKE_LIB, 243);
}

DLLEXPORT void _FreeUserPhysicalPages(void)
{
	JMP(FAKE_LIB, 244);
}

DLLEXPORT void _FreeVirtualBuffer(void)
{
	JMP(FAKE_LIB, 245);
}

DLLEXPORT void _GenerateConsoleCtrlEvent(void)
{
	JMP(FAKE_LIB, 246);
}

DLLEXPORT void _GetACP(void)
{
	JMP(FAKE_LIB, 247);
}

DLLEXPORT void _GetAtomNameA(void)
{
	JMP(FAKE_LIB, 248);
}

DLLEXPORT void _GetAtomNameW(void)
{
	JMP(FAKE_LIB, 249);
}

DLLEXPORT void _GetBinaryType(void)
{
	JMP(FAKE_LIB, 250);
}

DLLEXPORT void _GetBinaryTypeA(void)
{
	JMP(FAKE_LIB, 251);
}

DLLEXPORT void _GetBinaryTypeW(void)
{
	JMP(FAKE_LIB, 252);
}

DLLEXPORT void _GetCPFileNameFromRegistry(void)
{
	JMP(FAKE_LIB, 253);
}

DLLEXPORT void _GetCPInfo(void)
{
	JMP(FAKE_LIB, 254);
}

DLLEXPORT void _GetCPInfoExA(void)
{
	JMP(FAKE_LIB, 255);
}

DLLEXPORT void _GetCPInfoExW(void)
{
	JMP(FAKE_LIB, 256);
}

DLLEXPORT void _GetCalendarInfoA(void)
{
	JMP(FAKE_LIB, 257);
}

DLLEXPORT void _GetCalendarInfoW(void)
{
	JMP(FAKE_LIB, 258);
}

DLLEXPORT void _GetComPlusPackageInstallStatus(void)
{
	JMP(FAKE_LIB, 259);
}

DLLEXPORT void _GetCommConfig(void)
{
	JMP(FAKE_LIB, 260);
}

DLLEXPORT void _GetCommMask(void)
{
	JMP(FAKE_LIB, 261);
}

DLLEXPORT void _GetCommModemStatus(void)
{
	JMP(FAKE_LIB, 262);
}

DLLEXPORT void _GetCommProperties(void)
{
	JMP(FAKE_LIB, 263);
}

DLLEXPORT void _GetCommState(void)
{
	JMP(FAKE_LIB, 264);
}

DLLEXPORT void _GetCommTimeouts(void)
{
	JMP(FAKE_LIB, 265);
}

DLLEXPORT void _GetCommandLineA(void)
{
	JMP(FAKE_LIB, 266);
}

DLLEXPORT void _GetCommandLineW(void)
{
	JMP(FAKE_LIB, 267);
}

DLLEXPORT void _GetCompressedFileSizeA(void)
{
	JMP(FAKE_LIB, 268);
}

DLLEXPORT void _GetCompressedFileSizeW(void)
{
	JMP(FAKE_LIB, 269);
}

DLLEXPORT void _GetComputerNameA(void)
{
	JMP(FAKE_LIB, 270);
}

DLLEXPORT void _GetComputerNameExA(void)
{
	JMP(FAKE_LIB, 271);
}

DLLEXPORT void _GetComputerNameExW(void)
{
	JMP(FAKE_LIB, 272);
}

DLLEXPORT void _GetComputerNameW(void)
{
	JMP(FAKE_LIB, 273);
}

DLLEXPORT void _GetConsoleAliasA(void)
{
	JMP(FAKE_LIB, 274);
}

DLLEXPORT void _GetConsoleAliasExesA(void)
{
	JMP(FAKE_LIB, 275);
}

DLLEXPORT void _GetConsoleAliasExesLengthA(void)
{
	JMP(FAKE_LIB, 276);
}

DLLEXPORT void _GetConsoleAliasExesLengthW(void)
{
	JMP(FAKE_LIB, 277);
}

DLLEXPORT void _GetConsoleAliasExesW(void)
{
	JMP(FAKE_LIB, 278);
}

DLLEXPORT void _GetConsoleAliasW(void)
{
	JMP(FAKE_LIB, 279);
}

DLLEXPORT void _GetConsoleAliasesA(void)
{
	JMP(FAKE_LIB, 280);
}

DLLEXPORT void _GetConsoleAliasesLengthA(void)
{
	JMP(FAKE_LIB, 281);
}

DLLEXPORT void _GetConsoleAliasesLengthW(void)
{
	JMP(FAKE_LIB, 282);
}

DLLEXPORT void _GetConsoleAliasesW(void)
{
	JMP(FAKE_LIB, 283);
}

DLLEXPORT void _GetConsoleCP(void)
{
	JMP(FAKE_LIB, 284);
}

DLLEXPORT void _GetConsoleCharType(void)
{
	JMP(FAKE_LIB, 285);
}

DLLEXPORT void _GetConsoleCommandHistoryA(void)
{
	JMP(FAKE_LIB, 286);
}

DLLEXPORT void _GetConsoleCommandHistoryLengthA(void)
{
	JMP(FAKE_LIB, 287);
}

DLLEXPORT void _GetConsoleCommandHistoryLengthW(void)
{
	JMP(FAKE_LIB, 288);
}

DLLEXPORT void _GetConsoleCommandHistoryW(void)
{
	JMP(FAKE_LIB, 289);
}

DLLEXPORT void _GetConsoleCursorInfo(void)
{
	JMP(FAKE_LIB, 290);
}

DLLEXPORT void _GetConsoleCursorMode(void)
{
	JMP(FAKE_LIB, 291);
}

DLLEXPORT void _GetConsoleDisplayMode(void)
{
	JMP(FAKE_LIB, 292);
}

DLLEXPORT void _GetConsoleFontInfo(void)
{
	JMP(FAKE_LIB, 293);
}

DLLEXPORT void _GetConsoleFontSize(void)
{
	JMP(FAKE_LIB, 294);
}

DLLEXPORT void _GetConsoleHardwareState(void)
{
	JMP(FAKE_LIB, 295);
}

DLLEXPORT void _GetConsoleInputExeNameA(void)
{
	JMP(FAKE_LIB, 296);
}

DLLEXPORT void _GetConsoleInputExeNameW(void)
{
	JMP(FAKE_LIB, 297);
}

DLLEXPORT void _GetConsoleInputWaitHandle(void)
{
	JMP(FAKE_LIB, 298);
}

DLLEXPORT void _GetConsoleKeyboardLayoutNameA(void)
{
	JMP(FAKE_LIB, 299);
}

DLLEXPORT void _GetConsoleKeyboardLayoutNameW(void)
{
	JMP(FAKE_LIB, 300);
}

DLLEXPORT void _GetConsoleMode(void)
{
	JMP(FAKE_LIB, 301);
}

DLLEXPORT void _GetConsoleNlsMode(void)
{
	JMP(FAKE_LIB, 302);
}

DLLEXPORT void _GetConsoleOutputCP(void)
{
	JMP(FAKE_LIB, 303);
}

DLLEXPORT void _GetConsoleProcessList(void)
{
	JMP(FAKE_LIB, 304);
}

DLLEXPORT void _GetConsoleScreenBufferInfo(void)
{
	JMP(FAKE_LIB, 305);
}

DLLEXPORT void _GetConsoleSelectionInfo(void)
{
	JMP(FAKE_LIB, 306);
}

DLLEXPORT void _GetConsoleTitleA(void)
{
	JMP(FAKE_LIB, 307);
}

DLLEXPORT void _GetConsoleTitleW(void)
{
	JMP(FAKE_LIB, 308);
}

DLLEXPORT void _GetConsoleWindow(void)
{
	JMP(FAKE_LIB, 309);
}

DLLEXPORT void _GetCurrencyFormatA(void)
{
	JMP(FAKE_LIB, 310);
}

DLLEXPORT void _GetCurrencyFormatW(void)
{
	JMP(FAKE_LIB, 311);
}

DLLEXPORT void _GetCurrentActCtx(void)
{
	JMP(FAKE_LIB, 312);
}

DLLEXPORT void _GetCurrentConsoleFont(void)
{
	JMP(FAKE_LIB, 313);
}

DLLEXPORT void _GetCurrentDirectoryA(void)
{
	JMP(FAKE_LIB, 314);
}

DLLEXPORT void _GetCurrentDirectoryW(void)
{
	JMP(FAKE_LIB, 315);
}

DLLEXPORT void _GetCurrentProcess(void)
{
	JMP(FAKE_LIB, 316);
}

DLLEXPORT void _GetCurrentProcessId(void)
{
	JMP(FAKE_LIB, 317);
}

DLLEXPORT void _GetCurrentThread(void)
{
	JMP(FAKE_LIB, 318);
}

DLLEXPORT void _GetCurrentThreadId(void)
{
	JMP(FAKE_LIB, 319);
}

DLLEXPORT void _GetDateFormatA(void)
{
	JMP(FAKE_LIB, 320);
}

DLLEXPORT void _GetDateFormatW(void)
{
	JMP(FAKE_LIB, 321);
}

DLLEXPORT void _GetDefaultCommConfigA(void)
{
	JMP(FAKE_LIB, 322);
}

DLLEXPORT void _GetDefaultCommConfigW(void)
{
	JMP(FAKE_LIB, 323);
}

DLLEXPORT void _GetDefaultSortkeySize(void)
{
	JMP(FAKE_LIB, 324);
}

DLLEXPORT void _GetDevicePowerState(void)
{
	JMP(FAKE_LIB, 325);
}

DLLEXPORT void _GetDiskFreeSpaceA(void)
{
	JMP(FAKE_LIB, 326);
}

DLLEXPORT void _GetDiskFreeSpaceExA(void)
{
	JMP(FAKE_LIB, 327);
}

DLLEXPORT void _GetDiskFreeSpaceExW(void)
{
	JMP(FAKE_LIB, 328);
}

DLLEXPORT void _GetDiskFreeSpaceW(void)
{
	JMP(FAKE_LIB, 329);
}

DLLEXPORT void _GetDllDirectoryA(void)
{
	JMP(FAKE_LIB, 330);
}

DLLEXPORT void _GetDllDirectoryW(void)
{
	JMP(FAKE_LIB, 331);
}

DLLEXPORT void _GetDriveTypeA(void)
{
	JMP(FAKE_LIB, 332);
}

DLLEXPORT void _GetDriveTypeW(void)
{
	JMP(FAKE_LIB, 333);
}

DLLEXPORT void _GetEnvironmentStrings(void)
{
	JMP(FAKE_LIB, 334);
}

DLLEXPORT void _GetEnvironmentStringsA(void)
{
	JMP(FAKE_LIB, 335);
}

DLLEXPORT void _GetEnvironmentStringsW(void)
{
	JMP(FAKE_LIB, 336);
}

DLLEXPORT void _GetEnvironmentVariableA(void)
{
	JMP(FAKE_LIB, 337);
}

DLLEXPORT void _GetEnvironmentVariableW(void)
{
	JMP(FAKE_LIB, 338);
}

DLLEXPORT void _GetExitCodeProcess(void)
{
	JMP(FAKE_LIB, 339);
}

DLLEXPORT void _GetExitCodeThread(void)
{
	JMP(FAKE_LIB, 340);
}

DLLEXPORT void _GetExpandedNameA(void)
{
	JMP(FAKE_LIB, 341);
}

DLLEXPORT void _GetExpandedNameW(void)
{
	JMP(FAKE_LIB, 342);
}

DLLEXPORT void _GetFileAttributesA(void)
{
	JMP(FAKE_LIB, 343);
}

DLLEXPORT void _GetFileAttributesExA(void)
{
	JMP(FAKE_LIB, 344);
}

DLLEXPORT void _GetFileAttributesExW(void)
{
	JMP(FAKE_LIB, 345);
}

DLLEXPORT void _GetFileAttributesW(void)
{
	JMP(FAKE_LIB, 346);
}

DLLEXPORT void _GetFileInformationByHandle(void)
{
	JMP(FAKE_LIB, 347);
}

DLLEXPORT void _GetFileSize(void)
{
	JMP(FAKE_LIB, 348);
}

DLLEXPORT void _GetFileSizeEx(void)
{
	JMP(FAKE_LIB, 349);
}

DLLEXPORT void _GetFileTime(void)
{
	JMP(FAKE_LIB, 350);
}

DLLEXPORT void _GetFileType(void)
{
	JMP(FAKE_LIB, 351);
}

DLLEXPORT void _GetFirmwareEnvironmentVariableA(void)
{
	JMP(FAKE_LIB, 352);
}

DLLEXPORT void _GetFirmwareEnvironmentVariableW(void)
{
	JMP(FAKE_LIB, 353);
}

DLLEXPORT void _GetFullPathNameA(void)
{
	JMP(FAKE_LIB, 354);
}

DLLEXPORT void _GetFullPathNameW(void)
{
	JMP(FAKE_LIB, 355);
}

DLLEXPORT void _GetGeoInfoA(void)
{
	JMP(FAKE_LIB, 356);
}

DLLEXPORT void _GetGeoInfoW(void)
{
	JMP(FAKE_LIB, 357);
}

DLLEXPORT void _GetHandleContext(void)
{
	JMP(FAKE_LIB, 358);
}

DLLEXPORT void _GetHandleInformation(void)
{
	JMP(FAKE_LIB, 359);
}

DLLEXPORT void _GetLargestConsoleWindowSize(void)
{
	JMP(FAKE_LIB, 360);
}

DLLEXPORT void _GetLastError(void)
{
	JMP(FAKE_LIB, 361);
}

DLLEXPORT void _GetLinguistLangSize(void)
{
	JMP(FAKE_LIB, 362);
}

DLLEXPORT void _GetLocalTime(void)
{
	JMP(FAKE_LIB, 363);
}

DLLEXPORT void _GetLocaleInfoA(void)
{
	JMP(FAKE_LIB, 364);
}

DLLEXPORT void _GetLocaleInfoW(void)
{
	JMP(FAKE_LIB, 365);
}

DLLEXPORT void _GetLogicalDriveStringsA(void)
{
	JMP(FAKE_LIB, 366);
}

DLLEXPORT void _GetLogicalDriveStringsW(void)
{
	JMP(FAKE_LIB, 367);
}

DLLEXPORT void _GetLogicalDrives(void)
{
	JMP(FAKE_LIB, 368);
}

DLLEXPORT void _GetLongPathNameA(void)
{
	JMP(FAKE_LIB, 369);
}

DLLEXPORT void _GetLongPathNameW(void)
{
	JMP(FAKE_LIB, 370);
}

DLLEXPORT void _GetMailslotInfo(void)
{
	JMP(FAKE_LIB, 371);
}

DLLEXPORT void _GetModuleFileNameA(void)
{
	JMP(FAKE_LIB, 372);
}

DLLEXPORT void _GetModuleFileNameW(void)
{
	JMP(FAKE_LIB, 373);
}

DLLEXPORT void _GetModuleHandleA(void)
{
	JMP(FAKE_LIB, 374);
}

DLLEXPORT void _GetModuleHandleExA(void)
{
	JMP(FAKE_LIB, 375);
}

DLLEXPORT void _GetModuleHandleExW(void)
{
	JMP(FAKE_LIB, 376);
}

DLLEXPORT void _GetModuleHandleW(void)
{
	JMP(FAKE_LIB, 377);
}

DLLEXPORT void _GetNamedPipeHandleStateA(void)
{
	JMP(FAKE_LIB, 378);
}

DLLEXPORT void _GetNamedPipeHandleStateW(void)
{
	JMP(FAKE_LIB, 379);
}

DLLEXPORT void _GetNamedPipeInfo(void)
{
	JMP(FAKE_LIB, 380);
}

DLLEXPORT void _GetNativeSystemInfo(void)
{
	JMP(FAKE_LIB, 381);
}

DLLEXPORT void _GetNextVDMCommand(void)
{
	JMP(FAKE_LIB, 382);
}

DLLEXPORT void _GetNlsSectionName(void)
{
	JMP(FAKE_LIB, 383);
}

DLLEXPORT void _GetNumaAvailableMemory(void)
{
	JMP(FAKE_LIB, 384);
}

DLLEXPORT void _GetNumaAvailableMemoryNode(void)
{
	JMP(FAKE_LIB, 385);
}

DLLEXPORT void _GetNumaHighestNodeNumber(void)
{
	JMP(FAKE_LIB, 386);
}

DLLEXPORT void _GetNumaNodeProcessorMask(void)
{
	JMP(FAKE_LIB, 387);
}

DLLEXPORT void _GetNumaProcessorMap(void)
{
	JMP(FAKE_LIB, 388);
}

DLLEXPORT void _GetNumaProcessorNode(void)
{
	JMP(FAKE_LIB, 389);
}

DLLEXPORT void _GetNumberFormatA(void)
{
	JMP(FAKE_LIB, 390);
}

DLLEXPORT void _GetNumberFormatW(void)
{
	JMP(FAKE_LIB, 391);
}

DLLEXPORT void _GetNumberOfConsoleFonts(void)
{
	JMP(FAKE_LIB, 392);
}

DLLEXPORT void _GetNumberOfConsoleInputEvents(void)
{
	JMP(FAKE_LIB, 393);
}

DLLEXPORT void _GetNumberOfConsoleMouseButtons(void)
{
	JMP(FAKE_LIB, 394);
}

DLLEXPORT void _GetOEMCP(void)
{
	JMP(FAKE_LIB, 395);
}

DLLEXPORT void _GetOverlappedResult(void)
{
	JMP(FAKE_LIB, 396);
}

DLLEXPORT void _GetPriorityClass(void)
{
	JMP(FAKE_LIB, 397);
}

DLLEXPORT void _GetPrivateProfileIntA(void)
{
	JMP(FAKE_LIB, 398);
}

DLLEXPORT void _GetPrivateProfileIntW(void)
{
	JMP(FAKE_LIB, 399);
}

DLLEXPORT void _GetPrivateProfileSectionA(void)
{
	JMP(FAKE_LIB, 400);
}

DLLEXPORT void _GetPrivateProfileSectionNamesA(void)
{
	JMP(FAKE_LIB, 401);
}

DLLEXPORT void _GetPrivateProfileSectionNamesW(void)
{
	JMP(FAKE_LIB, 402);
}

DLLEXPORT void _GetPrivateProfileSectionW(void)
{
	JMP(FAKE_LIB, 403);
}

DLLEXPORT void _GetPrivateProfileStringA(void)
{
	JMP(FAKE_LIB, 404);
}

DLLEXPORT void _GetPrivateProfileStringW(void)
{
	JMP(FAKE_LIB, 405);
}

DLLEXPORT void _GetPrivateProfileStructA(void)
{
	JMP(FAKE_LIB, 406);
}

DLLEXPORT void _GetPrivateProfileStructW(void)
{
	JMP(FAKE_LIB, 407);
}

DLLEXPORT void _GetProcAddress(void)
{
	JMP(FAKE_LIB, 408);
}

DLLEXPORT void _GetProcessAffinityMask(void)
{
	JMP(FAKE_LIB, 409);
}

DLLEXPORT void _GetProcessHandleCount(void)
{
	JMP(FAKE_LIB, 410);
}

DLLEXPORT void _GetProcessHeap(void)
{
	JMP(FAKE_LIB, 411);
}

DLLEXPORT void _GetProcessHeaps(void)
{
	JMP(FAKE_LIB, 412);
}

DLLEXPORT void _GetProcessId(void)
{
	JMP(FAKE_LIB, 413);
}

DLLEXPORT void _GetProcessIoCounters(void)
{
	JMP(FAKE_LIB, 414);
}

DLLEXPORT void _GetProcessPriorityBoost(void)
{
	JMP(FAKE_LIB, 415);
}

DLLEXPORT void _GetProcessShutdownParameters(void)
{
	JMP(FAKE_LIB, 416);
}

DLLEXPORT void _GetProcessTimes(void)
{
	JMP(FAKE_LIB, 417);
}

DLLEXPORT void _GetProcessVersion(void)
{
	JMP(FAKE_LIB, 418);
}

DLLEXPORT void _GetProcessWorkingSetSize(void)
{
	JMP(FAKE_LIB, 419);
}

DLLEXPORT void _GetProfileIntA(void)
{
	JMP(FAKE_LIB, 420);
}

DLLEXPORT void _GetProfileIntW(void)
{
	JMP(FAKE_LIB, 421);
}

DLLEXPORT void _GetProfileSectionA(void)
{
	JMP(FAKE_LIB, 422);
}

DLLEXPORT void _GetProfileSectionW(void)
{
	JMP(FAKE_LIB, 423);
}

DLLEXPORT void _GetProfileStringA(void)
{
	JMP(FAKE_LIB, 424);
}

DLLEXPORT void _GetProfileStringW(void)
{
	JMP(FAKE_LIB, 425);
}

DLLEXPORT void _GetQueuedCompletionStatus(void)
{
	JMP(FAKE_LIB, 426);
}

DLLEXPORT void _GetShortPathNameA(void)
{
	JMP(FAKE_LIB, 427);
}

DLLEXPORT void _GetShortPathNameW(void)
{
	JMP(FAKE_LIB, 428);
}

DLLEXPORT void _GetStartupInfoA(void)
{
	JMP(FAKE_LIB, 429);
}

DLLEXPORT void _GetStartupInfoW(void)
{
	JMP(FAKE_LIB, 430);
}

DLLEXPORT void _GetStdHandle(void)
{
	JMP(FAKE_LIB, 431);
}

DLLEXPORT void _GetStringTypeA(void)
{
	JMP(FAKE_LIB, 432);
}

DLLEXPORT void _GetStringTypeExA(void)
{
	JMP(FAKE_LIB, 433);
}

DLLEXPORT void _GetStringTypeExW(void)
{
	JMP(FAKE_LIB, 434);
}

DLLEXPORT void _GetStringTypeW(void)
{
	JMP(FAKE_LIB, 435);
}

DLLEXPORT void _GetSystemDefaultLCID(void)
{
	JMP(FAKE_LIB, 436);
}

DLLEXPORT void _GetSystemDefaultLangID(void)
{
	JMP(FAKE_LIB, 437);
}

DLLEXPORT void _GetSystemDefaultUILanguage(void)
{
	JMP(FAKE_LIB, 438);
}

DLLEXPORT void _GetSystemDirectoryA(void)
{
	JMP(FAKE_LIB, 439);
}

DLLEXPORT void _GetSystemDirectoryW(void)
{
	JMP(FAKE_LIB, 440);
}

DLLEXPORT void _GetSystemInfo(void)
{
	JMP(FAKE_LIB, 441);
}

DLLEXPORT void _GetSystemPowerStatus(void)
{
	JMP(FAKE_LIB, 442);
}

DLLEXPORT void _GetSystemRegistryQuota(void)
{
	JMP(FAKE_LIB, 443);
}

DLLEXPORT void _GetSystemTime(void)
{
	JMP(FAKE_LIB, 444);
}

DLLEXPORT void _GetSystemTimeAdjustment(void)
{
	JMP(FAKE_LIB, 445);
}

DLLEXPORT void _GetSystemTimeAsFileTime(void)
{
	JMP(FAKE_LIB, 446);
}

DLLEXPORT void _GetSystemTimes(void)
{
	JMP(FAKE_LIB, 447);
}

DLLEXPORT void _GetSystemWindowsDirectoryA(void)
{
	JMP(FAKE_LIB, 448);
}

DLLEXPORT void _GetSystemWindowsDirectoryW(void)
{
	JMP(FAKE_LIB, 449);
}

DLLEXPORT void _GetSystemWow64DirectoryA(void)
{
	JMP(FAKE_LIB, 450);
}

DLLEXPORT void _GetSystemWow64DirectoryW(void)
{
	JMP(FAKE_LIB, 451);
}

DLLEXPORT void _GetTapeParameters(void)
{
	JMP(FAKE_LIB, 452);
}

DLLEXPORT void _GetTapePosition(void)
{
	JMP(FAKE_LIB, 453);
}

DLLEXPORT void _GetTapeStatus(void)
{
	JMP(FAKE_LIB, 454);
}

DLLEXPORT void _GetTempFileNameA(void)
{
	JMP(FAKE_LIB, 455);
}

DLLEXPORT void _GetTempFileNameW(void)
{
	JMP(FAKE_LIB, 456);
}

DLLEXPORT void _GetTempPathA(void)
{
	JMP(FAKE_LIB, 457);
}

DLLEXPORT void _GetTempPathW(void)
{
	JMP(FAKE_LIB, 458);
}

DLLEXPORT void _GetThreadContext(void)
{
	JMP(FAKE_LIB, 459);
}

DLLEXPORT void _GetThreadIOPendingFlag(void)
{
	JMP(FAKE_LIB, 460);
}

DLLEXPORT void _GetThreadLocale(void)
{
	JMP(FAKE_LIB, 461);
}

DLLEXPORT void _GetThreadPriority(void)
{
	JMP(FAKE_LIB, 462);
}

DLLEXPORT void _GetThreadPriorityBoost(void)
{
	JMP(FAKE_LIB, 463);
}

DLLEXPORT void _GetThreadSelectorEntry(void)
{
	JMP(FAKE_LIB, 464);
}

DLLEXPORT void _GetThreadTimes(void)
{
	JMP(FAKE_LIB, 465);
}

DLLEXPORT void _GetTickCount(void)
{
	JMP(FAKE_LIB, 466);
}

DLLEXPORT void _GetTimeFormatA(void)
{
	JMP(FAKE_LIB, 467);
}

DLLEXPORT void _GetTimeFormatW(void)
{
	JMP(FAKE_LIB, 468);
}

DLLEXPORT void _GetTimeZoneInformation(void)
{
	JMP(FAKE_LIB, 469);
}

DLLEXPORT void _GetUserDefaultLCID(void)
{
	JMP(FAKE_LIB, 470);
}

DLLEXPORT void _GetUserDefaultLangID(void)
{
	JMP(FAKE_LIB, 471);
}

DLLEXPORT void _GetUserDefaultUILanguage(void)
{
	JMP(FAKE_LIB, 472);
}

DLLEXPORT void _GetUserGeoID(void)
{
	JMP(FAKE_LIB, 473);
}

DLLEXPORT void _GetVDMCurrentDirectories(void)
{
	JMP(FAKE_LIB, 474);
}

DLLEXPORT void _GetVersion(void)
{
	JMP(FAKE_LIB, 475);
}

DLLEXPORT void _GetVersionExA(void)
{
	JMP(FAKE_LIB, 476);
}

DLLEXPORT void _GetVersionExW(void)
{
	JMP(FAKE_LIB, 477);
}

DLLEXPORT void _GetVolumeInformationA(void)
{
	JMP(FAKE_LIB, 478);
}

DLLEXPORT void _GetVolumeInformationW(void)
{
	JMP(FAKE_LIB, 479);
}

DLLEXPORT void _GetVolumeNameForVolumeMountPointA(void)
{
	JMP(FAKE_LIB, 480);
}

DLLEXPORT void _GetVolumeNameForVolumeMountPointW(void)
{
	JMP(FAKE_LIB, 481);
}

DLLEXPORT void _GetVolumePathNameA(void)
{
	JMP(FAKE_LIB, 482);
}

DLLEXPORT void _GetVolumePathNameW(void)
{
	JMP(FAKE_LIB, 483);
}

DLLEXPORT void _GetVolumePathNamesForVolumeNameA(void)
{
	JMP(FAKE_LIB, 484);
}

DLLEXPORT void _GetVolumePathNamesForVolumeNameW(void)
{
	JMP(FAKE_LIB, 485);
}

DLLEXPORT void _GetWindowsDirectoryA(void)
{
	JMP(FAKE_LIB, 486);
}

DLLEXPORT void _GetWindowsDirectoryW(void)
{
	JMP(FAKE_LIB, 487);
}

DLLEXPORT void _GetWriteWatch(void)
{
	JMP(FAKE_LIB, 488);
}

DLLEXPORT void _GlobalAddAtomA(void)
{
	JMP(FAKE_LIB, 489);
}

DLLEXPORT void _GlobalAddAtomW(void)
{
	JMP(FAKE_LIB, 490);
}

DLLEXPORT void _GlobalAlloc(void)
{
	JMP(FAKE_LIB, 491);
}

DLLEXPORT void _GlobalCompact(void)
{
	JMP(FAKE_LIB, 492);
}

DLLEXPORT void _GlobalDeleteAtom(void)
{
	JMP(FAKE_LIB, 493);
}

DLLEXPORT void _GlobalFindAtomA(void)
{
	JMP(FAKE_LIB, 494);
}

DLLEXPORT void _GlobalFindAtomW(void)
{
	JMP(FAKE_LIB, 495);
}

DLLEXPORT void _GlobalFix(void)
{
	JMP(FAKE_LIB, 496);
}

DLLEXPORT void _GlobalFlags(void)
{
	JMP(FAKE_LIB, 497);
}

DLLEXPORT void _GlobalFree(void)
{
	JMP(FAKE_LIB, 498);
}

DLLEXPORT void _GlobalGetAtomNameA(void)
{
	JMP(FAKE_LIB, 499);
}

DLLEXPORT void _GlobalGetAtomNameW(void)
{
	JMP(FAKE_LIB, 500);
}

DLLEXPORT void _GlobalHandle(void)
{
	JMP(FAKE_LIB, 501);
}

DLLEXPORT void _GlobalLock(void)
{
	JMP(FAKE_LIB, 502);
}

DLLEXPORT void _GlobalMemoryStatus(void)
{
	JMP(FAKE_LIB, 503);
}

DLLEXPORT void _GlobalMemoryStatusEx(void)
{
	JMP(FAKE_LIB, 504);
}

DLLEXPORT void _GlobalReAlloc(void)
{
	JMP(FAKE_LIB, 505);
}

DLLEXPORT void _GlobalSize(void)
{
	JMP(FAKE_LIB, 506);
}

DLLEXPORT void _GlobalUnWire(void)
{
	JMP(FAKE_LIB, 507);
}

DLLEXPORT void _GlobalUnfix(void)
{
	JMP(FAKE_LIB, 508);
}

DLLEXPORT void _GlobalUnlock(void)
{
	JMP(FAKE_LIB, 509);
}

DLLEXPORT void _GlobalWire(void)
{
	JMP(FAKE_LIB, 510);
}

DLLEXPORT void _Heap32First(void)
{
	JMP(FAKE_LIB, 511);
}

DLLEXPORT void _Heap32ListFirst(void)
{
	JMP(FAKE_LIB, 512);
}

DLLEXPORT void _Heap32ListNext(void)
{
	JMP(FAKE_LIB, 513);
}

DLLEXPORT void _Heap32Next(void)
{
	JMP(FAKE_LIB, 514);
}

DLLEXPORT void _HeapAlloc(void)
{
	JMP(FAKE_LIB, 515);
}

DLLEXPORT void _HeapCompact(void)
{
	JMP(FAKE_LIB, 516);
}

DLLEXPORT void _HeapCreate(void)
{
	JMP(FAKE_LIB, 517);
}

DLLEXPORT void _HeapCreateTagsW(void)
{
	JMP(FAKE_LIB, 518);
}

DLLEXPORT void _HeapDestroy(void)
{
	JMP(FAKE_LIB, 519);
}

DLLEXPORT void _HeapExtend(void)
{
	JMP(FAKE_LIB, 520);
}

DLLEXPORT void _HeapFree(void)
{
	JMP(FAKE_LIB, 521);
}

DLLEXPORT void _HeapLock(void)
{
	JMP(FAKE_LIB, 522);
}

DLLEXPORT void _HeapQueryInformation(void)
{
	JMP(FAKE_LIB, 523);
}

DLLEXPORT void _HeapQueryTagW(void)
{
	JMP(FAKE_LIB, 524);
}

DLLEXPORT void _HeapReAlloc(void)
{
	JMP(FAKE_LIB, 525);
}

DLLEXPORT void _HeapSetInformation(void)
{
	JMP(FAKE_LIB, 526);
}

DLLEXPORT void _HeapSize(void)
{
	JMP(FAKE_LIB, 527);
}

DLLEXPORT void _HeapSummary(void)
{
	JMP(FAKE_LIB, 528);
}

DLLEXPORT void _HeapUnlock(void)
{
	JMP(FAKE_LIB, 529);
}

DLLEXPORT void _HeapUsage(void)
{
	JMP(FAKE_LIB, 530);
}

DLLEXPORT void _HeapValidate(void)
{
	JMP(FAKE_LIB, 531);
}

DLLEXPORT void _HeapWalk(void)
{
	JMP(FAKE_LIB, 532);
}

DLLEXPORT void _InitAtomTable(void)
{
	JMP(FAKE_LIB, 533);
}

DLLEXPORT void _InitializeCriticalSection(void)
{
	JMP(FAKE_LIB, 534);
}

DLLEXPORT void _InitializeCriticalSectionAndSpinCount(void)
{
	JMP(FAKE_LIB, 535);
}

DLLEXPORT void _InitializeSListHead(void)
{
	JMP(FAKE_LIB, 536);
}

DLLEXPORT void _InterlockedCompareExchange(void)
{
	JMP(FAKE_LIB, 537);
}

DLLEXPORT void _InterlockedDecrement(void)
{
	JMP(FAKE_LIB, 538);
}

DLLEXPORT void _InterlockedExchange(void)
{
	JMP(FAKE_LIB, 539);
}

DLLEXPORT void _InterlockedExchangeAdd(void)
{
	JMP(FAKE_LIB, 540);
}

DLLEXPORT void _InterlockedFlushSList(void)
{
	JMP(FAKE_LIB, 541);
}

DLLEXPORT void _InterlockedIncrement(void)
{
	JMP(FAKE_LIB, 542);
}

DLLEXPORT void _InterlockedPopEntrySList(void)
{
	JMP(FAKE_LIB, 543);
}

DLLEXPORT void _InterlockedPushEntrySList(void)
{
	JMP(FAKE_LIB, 544);
}

DLLEXPORT void _InvalidateConsoleDIBits(void)
{
	JMP(FAKE_LIB, 545);
}

DLLEXPORT void _IsBadCodePtr(void)
{
	JMP(FAKE_LIB, 546);
}

DLLEXPORT void _IsBadHugeReadPtr(void)
{
	JMP(FAKE_LIB, 547);
}

DLLEXPORT void _IsBadHugeWritePtr(void)
{
	JMP(FAKE_LIB, 548);
}

DLLEXPORT void _IsBadReadPtr(void)
{
	JMP(FAKE_LIB, 549);
}

DLLEXPORT void _IsBadStringPtrA(void)
{
	JMP(FAKE_LIB, 550);
}

DLLEXPORT void _IsBadStringPtrW(void)
{
	JMP(FAKE_LIB, 551);
}

DLLEXPORT void _IsBadWritePtr(void)
{
	JMP(FAKE_LIB, 552);
}

DLLEXPORT void _IsDBCSLeadByte(void)
{
	JMP(FAKE_LIB, 553);
}

DLLEXPORT void _IsDBCSLeadByteEx(void)
{
	JMP(FAKE_LIB, 554);
}

DLLEXPORT void _IsDebuggerPresent(void)
{
	JMP(FAKE_LIB, 555);
}

DLLEXPORT void _IsProcessInJob(void)
{
	JMP(FAKE_LIB, 556);
}

DLLEXPORT void _IsProcessorFeaturePresent(void)
{
	JMP(FAKE_LIB, 557);
}

DLLEXPORT void _IsSystemResumeAutomatic(void)
{
	JMP(FAKE_LIB, 558);
}

DLLEXPORT void _IsValidCodePage(void)
{
	JMP(FAKE_LIB, 559);
}

DLLEXPORT void _IsValidLanguageGroup(void)
{
	JMP(FAKE_LIB, 560);
}

DLLEXPORT void _IsValidLocale(void)
{
	JMP(FAKE_LIB, 561);
}

DLLEXPORT void _IsValidUILanguage(void)
{
	JMP(FAKE_LIB, 562);
}

DLLEXPORT void _IsWow64Process(void)
{
	JMP(FAKE_LIB, 563);
}

DLLEXPORT void _LCMapStringA(void)
{
	JMP(FAKE_LIB, 564);
}

DLLEXPORT void _LCMapStringW(void)
{
	JMP(FAKE_LIB, 565);
}

DLLEXPORT void _LZClose(void)
{
	JMP(FAKE_LIB, 566);
}

DLLEXPORT void _LZCloseFile(void)
{
	JMP(FAKE_LIB, 567);
}

DLLEXPORT void _LZCopy(void)
{
	JMP(FAKE_LIB, 568);
}

DLLEXPORT void _LZCreateFileW(void)
{
	JMP(FAKE_LIB, 569);
}

DLLEXPORT void _LZDone(void)
{
	JMP(FAKE_LIB, 570);
}

DLLEXPORT void _LZInit(void)
{
	JMP(FAKE_LIB, 571);
}

DLLEXPORT void _LZOpenFileA(void)
{
	JMP(FAKE_LIB, 572);
}

DLLEXPORT void _LZOpenFileW(void)
{
	JMP(FAKE_LIB, 573);
}

DLLEXPORT void _LZRead(void)
{
	JMP(FAKE_LIB, 574);
}

DLLEXPORT void _LZSeek(void)
{
	JMP(FAKE_LIB, 575);
}

DLLEXPORT void _LZStart(void)
{
	JMP(FAKE_LIB, 576);
}

DLLEXPORT void _LeaveCriticalSection(void)
{
	JMP(FAKE_LIB, 577);
}

DLLEXPORT void _LoadLibraryA(void)
{
	JMP(FAKE_LIB, 578);
}

DLLEXPORT void _LoadLibraryExA(void)
{
	JMP(FAKE_LIB, 579);
}

DLLEXPORT void _LoadLibraryExW(void)
{
	JMP(FAKE_LIB, 580);
}

DLLEXPORT void _LoadLibraryW(void)
{
	JMP(FAKE_LIB, 581);
}

DLLEXPORT void _LoadModule(void)
{
	JMP(FAKE_LIB, 582);
}

DLLEXPORT void _LoadResource(void)
{
	JMP(FAKE_LIB, 583);
}

DLLEXPORT void _LocalAlloc(void)
{
	JMP(FAKE_LIB, 584);
}

DLLEXPORT void _LocalCompact(void)
{
	JMP(FAKE_LIB, 585);
}

DLLEXPORT void _LocalFileTimeToFileTime(void)
{
	JMP(FAKE_LIB, 586);
}

DLLEXPORT void _LocalFlags(void)
{
	JMP(FAKE_LIB, 587);
}

DLLEXPORT void _LocalFree(void)
{
	JMP(FAKE_LIB, 588);
}

DLLEXPORT void _LocalHandle(void)
{
	JMP(FAKE_LIB, 589);
}

DLLEXPORT void _LocalLock(void)
{
	JMP(FAKE_LIB, 590);
}

DLLEXPORT void _LocalReAlloc(void)
{
	JMP(FAKE_LIB, 591);
}

DLLEXPORT void _LocalShrink(void)
{
	JMP(FAKE_LIB, 592);
}

DLLEXPORT void _LocalSize(void)
{
	JMP(FAKE_LIB, 593);
}

DLLEXPORT void _LocalUnlock(void)
{
	JMP(FAKE_LIB, 594);
}

DLLEXPORT void _LockFile(void)
{
	JMP(FAKE_LIB, 595);
}

DLLEXPORT void _LockFileEx(void)
{
	JMP(FAKE_LIB, 596);
}

DLLEXPORT void _LockResource(void)
{
	JMP(FAKE_LIB, 597);
}

DLLEXPORT void _MapUserPhysicalPages(void)
{
	JMP(FAKE_LIB, 598);
}

DLLEXPORT void _MapUserPhysicalPagesScatter(void)
{
	JMP(FAKE_LIB, 599);
}

DLLEXPORT void _MapViewOfFile(void)
{
	JMP(FAKE_LIB, 600);
}

DLLEXPORT void _MapViewOfFileEx(void)
{
	JMP(FAKE_LIB, 601);
}

DLLEXPORT void _Module32First(void)
{
	JMP(FAKE_LIB, 602);
}

DLLEXPORT void _Module32FirstW(void)
{
	JMP(FAKE_LIB, 603);
}

DLLEXPORT void _Module32Next(void)
{
	JMP(FAKE_LIB, 604);
}

DLLEXPORT void _Module32NextW(void)
{
	JMP(FAKE_LIB, 605);
}

DLLEXPORT void _MoveFileA(void)
{
	JMP(FAKE_LIB, 606);
}

DLLEXPORT void _MoveFileExA(void)
{
	JMP(FAKE_LIB, 607);
}

DLLEXPORT void _MoveFileExW(void)
{
	JMP(FAKE_LIB, 608);
}

DLLEXPORT void _MoveFileW(void)
{
	JMP(FAKE_LIB, 609);
}

DLLEXPORT void _MoveFileWithProgressA(void)
{
	JMP(FAKE_LIB, 610);
}

DLLEXPORT void _MoveFileWithProgressW(void)
{
	JMP(FAKE_LIB, 611);
}

DLLEXPORT void _MulDiv(void)
{
	JMP(FAKE_LIB, 612);
}

DLLEXPORT void _MultiByteToWideChar(void)
{
	JMP(FAKE_LIB, 613);
}

DLLEXPORT void _NlsConvertIntegerToString(void)
{
	JMP(FAKE_LIB, 614);
}

DLLEXPORT void _NlsGetCacheUpdateCount(void)
{
	JMP(FAKE_LIB, 615);
}

DLLEXPORT void _NlsResetProcessLocale(void)
{
	JMP(FAKE_LIB, 616);
}

DLLEXPORT void _NumaVirtualQueryNode(void)
{
	JMP(FAKE_LIB, 617);
}

DLLEXPORT void _OpenConsoleW(void)
{
	JMP(FAKE_LIB, 618);
}

DLLEXPORT void _OpenDataFile(void)
{
	JMP(FAKE_LIB, 619);
}

DLLEXPORT void _OpenEventA(void)
{
	JMP(FAKE_LIB, 620);
}

DLLEXPORT void _OpenEventW(void)
{
	JMP(FAKE_LIB, 621);
}

DLLEXPORT void _OpenFile(void)
{
	JMP(FAKE_LIB, 622);
}

DLLEXPORT void _OpenFileMappingA(void)
{
	JMP(FAKE_LIB, 623);
}

DLLEXPORT void _OpenFileMappingW(void)
{
	JMP(FAKE_LIB, 624);
}

DLLEXPORT void _OpenJobObjectA(void)
{
	JMP(FAKE_LIB, 625);
}

DLLEXPORT void _OpenJobObjectW(void)
{
	JMP(FAKE_LIB, 626);
}

DLLEXPORT void _OpenMutexA(void)
{
	JMP(FAKE_LIB, 627);
}

DLLEXPORT void _OpenMutexW(void)
{
	JMP(FAKE_LIB, 628);
}

DLLEXPORT void _OpenProcess(void)
{
	JMP(FAKE_LIB, 629);
}

DLLEXPORT void _OpenProfileUserMapping(void)
{
	JMP(FAKE_LIB, 630);
}

DLLEXPORT void _OpenSemaphoreA(void)
{
	JMP(FAKE_LIB, 631);
}

DLLEXPORT void _OpenSemaphoreW(void)
{
	JMP(FAKE_LIB, 632);
}

DLLEXPORT void _OpenThread(void)
{
	JMP(FAKE_LIB, 633);
}

DLLEXPORT void _OpenWaitableTimerA(void)
{
	JMP(FAKE_LIB, 634);
}

DLLEXPORT void _OpenWaitableTimerW(void)
{
	JMP(FAKE_LIB, 635);
}

DLLEXPORT void _OutputDebugStringA(void)
{
	JMP(FAKE_LIB, 636);
}

DLLEXPORT void _OutputDebugStringW(void)
{
	JMP(FAKE_LIB, 637);
}

DLLEXPORT void _PeekConsoleInputA(void)
{
	JMP(FAKE_LIB, 638);
}

DLLEXPORT void _PeekConsoleInputW(void)
{
	JMP(FAKE_LIB, 639);
}

DLLEXPORT void _PeekNamedPipe(void)
{
	JMP(FAKE_LIB, 640);
}

DLLEXPORT void _PostQueuedCompletionStatus(void)
{
	JMP(FAKE_LIB, 641);
}

DLLEXPORT void _PrepareTape(void)
{
	JMP(FAKE_LIB, 642);
}

DLLEXPORT void _PrivCopyFileExW(void)
{
	JMP(FAKE_LIB, 643);
}

DLLEXPORT void _PrivMoveFileIdentityW(void)
{
	JMP(FAKE_LIB, 644);
}

DLLEXPORT void _Process32First(void)
{
	JMP(FAKE_LIB, 645);
}

DLLEXPORT void _Process32FirstW(void)
{
	JMP(FAKE_LIB, 646);
}

DLLEXPORT void _Process32Next(void)
{
	JMP(FAKE_LIB, 647);
}

DLLEXPORT void _Process32NextW(void)
{
	JMP(FAKE_LIB, 648);
}

DLLEXPORT void _ProcessIdToSessionId(void)
{
	JMP(FAKE_LIB, 649);
}

DLLEXPORT void _PulseEvent(void)
{
	JMP(FAKE_LIB, 650);
}

DLLEXPORT void _PurgeComm(void)
{
	JMP(FAKE_LIB, 651);
}

DLLEXPORT void _QueryActCtxW(void)
{
	JMP(FAKE_LIB, 652);
}

DLLEXPORT void _QueryDepthSList(void)
{
	JMP(FAKE_LIB, 653);
}

DLLEXPORT void _QueryDosDeviceA(void)
{
	JMP(FAKE_LIB, 654);
}

DLLEXPORT void _QueryDosDeviceW(void)
{
	JMP(FAKE_LIB, 655);
}

DLLEXPORT void _QueryInformationJobObject(void)
{
	JMP(FAKE_LIB, 656);
}

DLLEXPORT void _QueryMemoryResourceNotification(void)
{
	JMP(FAKE_LIB, 657);
}

DLLEXPORT void _QueryPerformanceCounter(void)
{
	JMP(FAKE_LIB, 658);
}

DLLEXPORT void _QueryPerformanceFrequency(void)
{
	JMP(FAKE_LIB, 659);
}

DLLEXPORT void _QueryWin31IniFilesMappedToRegistry(void)
{
	JMP(FAKE_LIB, 660);
}

DLLEXPORT void _QueueUserAPC(void)
{
	JMP(FAKE_LIB, 661);
}

DLLEXPORT void _QueueUserWorkItem(void)
{
	JMP(FAKE_LIB, 662);
}

DLLEXPORT void _RaiseException(void)
{
	JMP(FAKE_LIB, 663);
}

DLLEXPORT void _ReadConsoleA(void)
{
	JMP(FAKE_LIB, 664);
}

DLLEXPORT void _ReadConsoleInputA(void)
{
	JMP(FAKE_LIB, 665);
}

DLLEXPORT void _ReadConsoleInputExA(void)
{
	JMP(FAKE_LIB, 666);
}

DLLEXPORT void _ReadConsoleInputExW(void)
{
	JMP(FAKE_LIB, 667);
}

DLLEXPORT void _ReadConsoleInputW(void)
{
	JMP(FAKE_LIB, 668);
}

DLLEXPORT void _ReadConsoleOutputA(void)
{
	JMP(FAKE_LIB, 669);
}

DLLEXPORT void _ReadConsoleOutputAttribute(void)
{
	JMP(FAKE_LIB, 670);
}

DLLEXPORT void _ReadConsoleOutputCharacterA(void)
{
	JMP(FAKE_LIB, 671);
}

DLLEXPORT void _ReadConsoleOutputCharacterW(void)
{
	JMP(FAKE_LIB, 672);
}

DLLEXPORT void _ReadConsoleOutputW(void)
{
	JMP(FAKE_LIB, 673);
}

DLLEXPORT void _ReadConsoleW(void)
{
	JMP(FAKE_LIB, 674);
}

DLLEXPORT void _ReadDirectoryChangesW(void)
{
	JMP(FAKE_LIB, 675);
}

DLLEXPORT void _ReadFile(void)
{
	JMP(FAKE_LIB, 676);
}

DLLEXPORT void _ReadFileEx(void)
{
	JMP(FAKE_LIB, 677);
}

DLLEXPORT void _ReadFileScatter(void)
{
	JMP(FAKE_LIB, 678);
}

DLLEXPORT void _ReadProcessMemory(void)
{
	JMP(FAKE_LIB, 679);
}

DLLEXPORT void _RegisterConsoleIME(void)
{
	JMP(FAKE_LIB, 680);
}

DLLEXPORT void _RegisterConsoleOS2(void)
{
	JMP(FAKE_LIB, 681);
}

DLLEXPORT void _RegisterConsoleVDM(void)
{
	JMP(FAKE_LIB, 682);
}

DLLEXPORT void _RegisterWaitForInputIdle(void)
{
	JMP(FAKE_LIB, 683);
}

DLLEXPORT void _RegisterWaitForSingleObject(void)
{
	JMP(FAKE_LIB, 684);
}

DLLEXPORT void _RegisterWaitForSingleObjectEx(void)
{
	JMP(FAKE_LIB, 685);
}

DLLEXPORT void _RegisterWowBaseHandlers(void)
{
	JMP(FAKE_LIB, 686);
}

DLLEXPORT void _RegisterWowExec(void)
{
	JMP(FAKE_LIB, 687);
}

DLLEXPORT void _ReleaseActCtx(void)
{
	JMP(FAKE_LIB, 688);
}

DLLEXPORT void _ReleaseMutex(void)
{
	JMP(FAKE_LIB, 689);
}

DLLEXPORT void _ReleaseSemaphore(void)
{
	JMP(FAKE_LIB, 690);
}

DLLEXPORT void _RemoveDirectoryA(void)
{
	JMP(FAKE_LIB, 691);
}

DLLEXPORT void _RemoveDirectoryW(void)
{
	JMP(FAKE_LIB, 692);
}

DLLEXPORT void _RemoveLocalAlternateComputerNameA(void)
{
	JMP(FAKE_LIB, 693);
}

DLLEXPORT void _RemoveLocalAlternateComputerNameW(void)
{
	JMP(FAKE_LIB, 694);
}

DLLEXPORT void _RemoveVectoredExceptionHandler(void)
{
	JMP(FAKE_LIB, 695);
}

DLLEXPORT void _ReplaceFile(void)
{
	JMP(FAKE_LIB, 696);
}

DLLEXPORT void _ReplaceFileA(void)
{
	JMP(FAKE_LIB, 697);
}

DLLEXPORT void _ReplaceFileW(void)
{
	JMP(FAKE_LIB, 698);
}

DLLEXPORT void _RequestDeviceWakeup(void)
{
	JMP(FAKE_LIB, 699);
}

DLLEXPORT void _RequestWakeupLatency(void)
{
	JMP(FAKE_LIB, 700);
}

DLLEXPORT void _ResetEvent(void)
{
	JMP(FAKE_LIB, 701);
}

DLLEXPORT void _ResetWriteWatch(void)
{
	JMP(FAKE_LIB, 702);
}

DLLEXPORT void _RestoreLastError(void)
{
	JMP(FAKE_LIB, 703);
}

DLLEXPORT void _ResumeThread(void)
{
	JMP(FAKE_LIB, 704);
}

DLLEXPORT void _RtlCaptureContext(void)
{
	JMP(FAKE_LIB, 705);
}

DLLEXPORT void _RtlCaptureStackBackTrace(void)
{
	JMP(FAKE_LIB, 706);
}

DLLEXPORT void _RtlFillMemory(void)
{
	JMP(FAKE_LIB, 707);
}

DLLEXPORT void _RtlMoveMemory(void)
{
	JMP(FAKE_LIB, 708);
}

DLLEXPORT void _RtlUnwind(void)
{
	JMP(FAKE_LIB, 709);
}

DLLEXPORT void _RtlZeroMemory(void)
{
	JMP(FAKE_LIB, 710);
}

DLLEXPORT void _ScrollConsoleScreenBufferA(void)
{
	JMP(FAKE_LIB, 711);
}

DLLEXPORT void _ScrollConsoleScreenBufferW(void)
{
	JMP(FAKE_LIB, 712);
}

DLLEXPORT void _SearchPathA(void)
{
	JMP(FAKE_LIB, 713);
}

DLLEXPORT void _SearchPathW(void)
{
	JMP(FAKE_LIB, 714);
}

DLLEXPORT void _SetCPGlobal(void)
{
	JMP(FAKE_LIB, 715);
}

DLLEXPORT void _SetCalendarInfoA(void)
{
	JMP(FAKE_LIB, 716);
}

DLLEXPORT void _SetCalendarInfoW(void)
{
	JMP(FAKE_LIB, 717);
}

DLLEXPORT void _SetClientTimeZoneInformation(void)
{
	JMP(FAKE_LIB, 718);
}

DLLEXPORT void _SetComPlusPackageInstallStatus(void)
{
	JMP(FAKE_LIB, 719);
}

DLLEXPORT void _SetCommBreak(void)
{
	JMP(FAKE_LIB, 720);
}

DLLEXPORT void _SetCommConfig(void)
{
	JMP(FAKE_LIB, 721);
}

DLLEXPORT void _SetCommMask(void)
{
	JMP(FAKE_LIB, 722);
}

DLLEXPORT void _SetCommState(void)
{
	JMP(FAKE_LIB, 723);
}

DLLEXPORT void _SetCommTimeouts(void)
{
	JMP(FAKE_LIB, 724);
}

DLLEXPORT void _SetComputerNameA(void)
{
	JMP(FAKE_LIB, 725);
}

DLLEXPORT void _SetComputerNameExA(void)
{
	JMP(FAKE_LIB, 726);
}

DLLEXPORT void _SetComputerNameExW(void)
{
	JMP(FAKE_LIB, 727);
}

DLLEXPORT void _SetComputerNameW(void)
{
	JMP(FAKE_LIB, 728);
}

DLLEXPORT void _SetConsoleActiveScreenBuffer(void)
{
	JMP(FAKE_LIB, 729);
}

DLLEXPORT void _SetConsoleCP(void)
{
	JMP(FAKE_LIB, 730);
}

DLLEXPORT void _SetConsoleCommandHistoryMode(void)
{
	JMP(FAKE_LIB, 731);
}

DLLEXPORT void _SetConsoleCtrlHandler(void)
{
	JMP(FAKE_LIB, 732);
}

DLLEXPORT void _SetConsoleCursor(void)
{
	JMP(FAKE_LIB, 733);
}

DLLEXPORT void _SetConsoleCursorInfo(void)
{
	JMP(FAKE_LIB, 734);
}

DLLEXPORT void _SetConsoleCursorMode(void)
{
	JMP(FAKE_LIB, 735);
}

DLLEXPORT void _SetConsoleCursorPosition(void)
{
	JMP(FAKE_LIB, 736);
}

DLLEXPORT void _SetConsoleDisplayMode(void)
{
	JMP(FAKE_LIB, 737);
}

DLLEXPORT void _SetConsoleFont(void)
{
	JMP(FAKE_LIB, 738);
}

DLLEXPORT void _SetConsoleHardwareState(void)
{
	JMP(FAKE_LIB, 739);
}

DLLEXPORT void _SetConsoleIcon(void)
{
	JMP(FAKE_LIB, 740);
}

DLLEXPORT void _SetConsoleInputExeNameA(void)
{
	JMP(FAKE_LIB, 741);
}

DLLEXPORT void _SetConsoleInputExeNameW(void)
{
	JMP(FAKE_LIB, 742);
}

DLLEXPORT void _SetConsoleKeyShortcuts(void)
{
	JMP(FAKE_LIB, 743);
}

DLLEXPORT void _SetConsoleLocalEUDC(void)
{
	JMP(FAKE_LIB, 744);
}

DLLEXPORT void _SetConsoleMaximumWindowSize(void)
{
	JMP(FAKE_LIB, 745);
}

DLLEXPORT void _SetConsoleMenuClose(void)
{
	JMP(FAKE_LIB, 746);
}

DLLEXPORT void _SetConsoleMode(void)
{
	JMP(FAKE_LIB, 747);
}

DLLEXPORT void _SetConsoleNlsMode(void)
{
	JMP(FAKE_LIB, 748);
}

DLLEXPORT void _SetConsoleNumberOfCommandsA(void)
{
	JMP(FAKE_LIB, 749);
}

DLLEXPORT void _SetConsoleNumberOfCommandsW(void)
{
	JMP(FAKE_LIB, 750);
}

DLLEXPORT void _SetConsoleOS2OemFormat(void)
{
	JMP(FAKE_LIB, 751);
}

DLLEXPORT void _SetConsoleOutputCP(void)
{
	JMP(FAKE_LIB, 752);
}

DLLEXPORT void _SetConsolePalette(void)
{
	JMP(FAKE_LIB, 753);
}

DLLEXPORT void _SetConsoleScreenBufferSize(void)
{
	JMP(FAKE_LIB, 754);
}

DLLEXPORT void _SetConsoleTextAttribute(void)
{
	JMP(FAKE_LIB, 755);
}

DLLEXPORT void _SetConsoleTitleA(void)
{
	JMP(FAKE_LIB, 756);
}

DLLEXPORT void _SetConsoleTitleW(void)
{
	JMP(FAKE_LIB, 757);
}

DLLEXPORT void _SetConsoleWindowInfo(void)
{
	JMP(FAKE_LIB, 758);
}

DLLEXPORT void _SetCriticalSectionSpinCount(void)
{
	JMP(FAKE_LIB, 759);
}

DLLEXPORT void _SetCurrentDirectoryA(void)
{
	JMP(FAKE_LIB, 760);
}

DLLEXPORT void _SetCurrentDirectoryW(void)
{
	JMP(FAKE_LIB, 761);
}

DLLEXPORT void _SetDefaultCommConfigA(void)
{
	JMP(FAKE_LIB, 762);
}

DLLEXPORT void _SetDefaultCommConfigW(void)
{
	JMP(FAKE_LIB, 763);
}

DLLEXPORT void _SetDllDirectoryA(void)
{
	JMP(FAKE_LIB, 764);
}

DLLEXPORT void _SetDllDirectoryW(void)
{
	JMP(FAKE_LIB, 765);
}

DLLEXPORT void _SetEndOfFile(void)
{
	JMP(FAKE_LIB, 766);
}

DLLEXPORT void _SetEnvironmentVariableA(void)
{
	JMP(FAKE_LIB, 767);
}

DLLEXPORT void _SetEnvironmentVariableW(void)
{
	JMP(FAKE_LIB, 768);
}

DLLEXPORT void _SetErrorMode(void)
{
	JMP(FAKE_LIB, 769);
}

DLLEXPORT void _SetEvent(void)
{
	JMP(FAKE_LIB, 770);
}

DLLEXPORT void _SetFileApisToANSI(void)
{
	JMP(FAKE_LIB, 771);
}

DLLEXPORT void _SetFileApisToOEM(void)
{
	JMP(FAKE_LIB, 772);
}

DLLEXPORT void _SetFileAttributesA(void)
{
	JMP(FAKE_LIB, 773);
}

DLLEXPORT void _SetFileAttributesW(void)
{
	JMP(FAKE_LIB, 774);
}

DLLEXPORT void _SetFilePointer(void)
{
	JMP(FAKE_LIB, 775);
}

DLLEXPORT void _SetFilePointerEx(void)
{
	JMP(FAKE_LIB, 776);
}

DLLEXPORT void _SetFileShortNameA(void)
{
	JMP(FAKE_LIB, 777);
}

DLLEXPORT void _SetFileShortNameW(void)
{
	JMP(FAKE_LIB, 778);
}

DLLEXPORT void _SetFileTime(void)
{
	JMP(FAKE_LIB, 779);
}

DLLEXPORT void _SetFileValidData(void)
{
	JMP(FAKE_LIB, 780);
}

DLLEXPORT void _SetFirmwareEnvironmentVariableA(void)
{
	JMP(FAKE_LIB, 781);
}

DLLEXPORT void _SetFirmwareEnvironmentVariableW(void)
{
	JMP(FAKE_LIB, 782);
}

DLLEXPORT void _SetHandleContext(void)
{
	JMP(FAKE_LIB, 783);
}

DLLEXPORT void _SetHandleCount(void)
{
	JMP(FAKE_LIB, 784);
}

DLLEXPORT void _SetHandleInformation(void)
{
	JMP(FAKE_LIB, 785);
}

DLLEXPORT void _SetInformationJobObject(void)
{
	JMP(FAKE_LIB, 786);
}

DLLEXPORT void _SetLastConsoleEventActive(void)
{
	JMP(FAKE_LIB, 787);
}

DLLEXPORT void _SetLastError(void)
{
	JMP(FAKE_LIB, 788);
}

DLLEXPORT void _SetLocalPrimaryComputerNameA(void)
{
	JMP(FAKE_LIB, 789);
}

DLLEXPORT void _SetLocalPrimaryComputerNameW(void)
{
	JMP(FAKE_LIB, 790);
}

DLLEXPORT void _SetLocalTime(void)
{
	JMP(FAKE_LIB, 791);
}

DLLEXPORT void _SetLocaleInfoA(void)
{
	JMP(FAKE_LIB, 792);
}

DLLEXPORT void _SetLocaleInfoW(void)
{
	JMP(FAKE_LIB, 793);
}

DLLEXPORT void _SetMailslotInfo(void)
{
	JMP(FAKE_LIB, 794);
}

DLLEXPORT void _SetMessageWaitingIndicator(void)
{
	JMP(FAKE_LIB, 795);
}

DLLEXPORT void _SetNamedPipeHandleState(void)
{
	JMP(FAKE_LIB, 796);
}

DLLEXPORT void _SetPriorityClass(void)
{
	JMP(FAKE_LIB, 797);
}

DLLEXPORT void _SetProcessAffinityMask(void)
{
	JMP(FAKE_LIB, 798);
}

DLLEXPORT void _SetProcessPriorityBoost(void)
{
	JMP(FAKE_LIB, 799);
}

DLLEXPORT void _SetProcessShutdownParameters(void)
{
	JMP(FAKE_LIB, 800);
}

DLLEXPORT void _SetProcessWorkingSetSize(void)
{
	JMP(FAKE_LIB, 801);
}

DLLEXPORT void _SetSearchPathMode(void)
{
	JMP(FAKE_LIB, 802);
}

DLLEXPORT void _SetStdHandle(void)
{
	JMP(FAKE_LIB, 803);
}

DLLEXPORT void _SetSystemPowerState(void)
{
	JMP(FAKE_LIB, 804);
}

DLLEXPORT void _SetSystemTime(void)
{
	JMP(FAKE_LIB, 805);
}

DLLEXPORT void _SetSystemTimeAdjustment(void)
{
	JMP(FAKE_LIB, 806);
}

DLLEXPORT void _SetTapeParameters(void)
{
	JMP(FAKE_LIB, 807);
}

DLLEXPORT void _SetTapePosition(void)
{
	JMP(FAKE_LIB, 808);
}

DLLEXPORT void _SetTermsrvAppInstallMode(void)
{
	JMP(FAKE_LIB, 809);
}

DLLEXPORT void _SetThreadAffinityMask(void)
{
	JMP(FAKE_LIB, 810);
}

DLLEXPORT void _SetThreadContext(void)
{
	JMP(FAKE_LIB, 811);
}

DLLEXPORT void _SetThreadExecutionState(void)
{
	JMP(FAKE_LIB, 812);
}

DLLEXPORT void _SetThreadIdealProcessor(void)
{
	JMP(FAKE_LIB, 813);
}

DLLEXPORT void _SetThreadLocale(void)
{
	JMP(FAKE_LIB, 814);
}

DLLEXPORT void _SetThreadPriority(void)
{
	JMP(FAKE_LIB, 815);
}

DLLEXPORT void _SetThreadPriorityBoost(void)
{
	JMP(FAKE_LIB, 816);
}

DLLEXPORT void _SetThreadUILanguage(void)
{
	JMP(FAKE_LIB, 817);
}

DLLEXPORT void _SetTimeZoneInformation(void)
{
	JMP(FAKE_LIB, 818);
}

DLLEXPORT void _SetTimerQueueTimer(void)
{
	JMP(FAKE_LIB, 819);
}

DLLEXPORT void _SetUnhandledExceptionFilter(void)
{
	JMP(FAKE_LIB, 820);
}

DLLEXPORT void _SetUserGeoID(void)
{
	JMP(FAKE_LIB, 821);
}

DLLEXPORT void _SetVDMCurrentDirectories(void)
{
	JMP(FAKE_LIB, 822);
}

DLLEXPORT void _SetVolumeLabelA(void)
{
	JMP(FAKE_LIB, 823);
}

DLLEXPORT void _SetVolumeLabelW(void)
{
	JMP(FAKE_LIB, 824);
}

DLLEXPORT void _SetVolumeMountPointA(void)
{
	JMP(FAKE_LIB, 825);
}

DLLEXPORT void _SetVolumeMountPointW(void)
{
	JMP(FAKE_LIB, 826);
}

DLLEXPORT void _SetWaitableTimer(void)
{
	JMP(FAKE_LIB, 827);
}

DLLEXPORT void _SetupComm(void)
{
	JMP(FAKE_LIB, 828);
}

DLLEXPORT void _ShowConsoleCursor(void)
{
	JMP(FAKE_LIB, 829);
}

DLLEXPORT void _SignalObjectAndWait(void)
{
	JMP(FAKE_LIB, 830);
}

DLLEXPORT void _SizeofResource(void)
{
	JMP(FAKE_LIB, 831);
}

DLLEXPORT void _Sleep(void)
{
	JMP(FAKE_LIB, 832);
}

DLLEXPORT void _SleepEx(void)
{
	JMP(FAKE_LIB, 833);
}

DLLEXPORT void _SuspendThread(void)
{
	JMP(FAKE_LIB, 834);
}

DLLEXPORT void _SwitchToFiber(void)
{
	JMP(FAKE_LIB, 835);
}

DLLEXPORT void _SwitchToThread(void)
{
	JMP(FAKE_LIB, 836);
}

DLLEXPORT void _SystemTimeToFileTime(void)
{
	JMP(FAKE_LIB, 837);
}

DLLEXPORT void _SystemTimeToTzSpecificLocalTime(void)
{
	JMP(FAKE_LIB, 838);
}

DLLEXPORT void _TerminateJobObject(void)
{
	JMP(FAKE_LIB, 839);
}

DLLEXPORT void _TerminateProcess(void)
{
	JMP(FAKE_LIB, 840);
}

DLLEXPORT void _TerminateThread(void)
{
	JMP(FAKE_LIB, 841);
}

DLLEXPORT void _TermsrvAppInstallMode(void)
{
	JMP(FAKE_LIB, 842);
}

DLLEXPORT void _Thread32First(void)
{
	JMP(FAKE_LIB, 843);
}

DLLEXPORT void _Thread32Next(void)
{
	JMP(FAKE_LIB, 844);
}

DLLEXPORT void _TlsAlloc(void)
{
	JMP(FAKE_LIB, 845);
}

DLLEXPORT void _TlsFree(void)
{
	JMP(FAKE_LIB, 846);
}

DLLEXPORT void _TlsGetValue(void)
{
	JMP(FAKE_LIB, 847);
}

DLLEXPORT void _TlsSetValue(void)
{
	JMP(FAKE_LIB, 848);
}

DLLEXPORT void _Toolhelp32ReadProcessMemory(void)
{
	JMP(FAKE_LIB, 849);
}

DLLEXPORT void _TransactNamedPipe(void)
{
	JMP(FAKE_LIB, 850);
}

DLLEXPORT void _TransmitCommChar(void)
{
	JMP(FAKE_LIB, 851);
}

DLLEXPORT void _TrimVirtualBuffer(void)
{
	JMP(FAKE_LIB, 852);
}

DLLEXPORT void _TryEnterCriticalSection(void)
{
	JMP(FAKE_LIB, 853);
}

DLLEXPORT void _TzSpecificLocalTimeToSystemTime(void)
{
	JMP(FAKE_LIB, 854);
}

DLLEXPORT void _UTRegister(void)
{
	JMP(FAKE_LIB, 855);
}

DLLEXPORT void _UTUnRegister(void)
{
	JMP(FAKE_LIB, 856);
}

DLLEXPORT void _UnhandledExceptionFilter(void)
{
	JMP(FAKE_LIB, 857);
}

DLLEXPORT void _UnlockFile(void)
{
	JMP(FAKE_LIB, 858);
}

DLLEXPORT void _UnlockFileEx(void)
{
	JMP(FAKE_LIB, 859);
}

DLLEXPORT void _UnmapViewOfFile(void)
{
	JMP(FAKE_LIB, 860);
}

DLLEXPORT void _UnregisterConsoleIME(void)
{
	JMP(FAKE_LIB, 861);
}

DLLEXPORT void _UnregisterWait(void)
{
	JMP(FAKE_LIB, 862);
}

DLLEXPORT void _UnregisterWaitEx(void)
{
	JMP(FAKE_LIB, 863);
}

DLLEXPORT void _UpdateResourceA(void)
{
	JMP(FAKE_LIB, 864);
}

DLLEXPORT void _UpdateResourceW(void)
{
	JMP(FAKE_LIB, 865);
}

DLLEXPORT void _VDMConsoleOperation(void)
{
	JMP(FAKE_LIB, 866);
}

DLLEXPORT void _VDMOperationStarted(void)
{
	JMP(FAKE_LIB, 867);
}

DLLEXPORT void _ValidateLCType(void)
{
	JMP(FAKE_LIB, 868);
}

DLLEXPORT void _ValidateLocale(void)
{
	JMP(FAKE_LIB, 869);
}

DLLEXPORT void _VerLanguageNameA(void)
{
	JMP(FAKE_LIB, 870);
}

DLLEXPORT void _VerLanguageNameW(void)
{
	JMP(FAKE_LIB, 871);
}

DLLEXPORT void _VerSetConditionMask(void)
{
	JMP(FAKE_LIB, 872);
}

DLLEXPORT void _VerifyConsoleIoHandle(void)
{
	JMP(FAKE_LIB, 873);
}

DLLEXPORT void _VerifyVersionInfoA(void)
{
	JMP(FAKE_LIB, 874);
}

DLLEXPORT void _VerifyVersionInfoW(void)
{
	JMP(FAKE_LIB, 875);
}

DLLEXPORT void _VirtualAlloc(void)
{
	JMP(FAKE_LIB, 876);
}

DLLEXPORT void _VirtualAllocEx(void)
{
	JMP(FAKE_LIB, 877);
}

DLLEXPORT void _VirtualBufferExceptionHandler(void)
{
	JMP(FAKE_LIB, 878);
}

DLLEXPORT void _VirtualFree(void)
{
	JMP(FAKE_LIB, 879);
}

DLLEXPORT void _VirtualFreeEx(void)
{
	JMP(FAKE_LIB, 880);
}

DLLEXPORT void _VirtualLock(void)
{
	JMP(FAKE_LIB, 881);
}

DLLEXPORT void _VirtualProtect(void)
{
	JMP(FAKE_LIB, 882);
}

DLLEXPORT void _VirtualProtectEx(void)
{
	JMP(FAKE_LIB, 883);
}

DLLEXPORT void _VirtualQuery(void)
{
	JMP(FAKE_LIB, 884);
}

DLLEXPORT void _VirtualQueryEx(void)
{
	JMP(FAKE_LIB, 885);
}

DLLEXPORT void _VirtualUnlock(void)
{
	JMP(FAKE_LIB, 886);
}

DLLEXPORT void _WTSGetActiveConsoleSessionId(void)
{
	JMP(FAKE_LIB, 887);
}

DLLEXPORT void _WaitCommEvent(void)
{
	JMP(FAKE_LIB, 888);
}

DLLEXPORT void _WaitForDebugEvent(void)
{
	JMP(FAKE_LIB, 889);
}

DLLEXPORT void _WaitForMultipleObjects(void)
{
	JMP(FAKE_LIB, 890);
}

DLLEXPORT void _WaitForMultipleObjectsEx(void)
{
	JMP(FAKE_LIB, 891);
}

DLLEXPORT void _WaitForSingleObject(void)
{
	JMP(FAKE_LIB, 892);
}

DLLEXPORT void _WaitForSingleObjectEx(void)
{
	JMP(FAKE_LIB, 893);
}

DLLEXPORT void _WaitNamedPipeA(void)
{
	JMP(FAKE_LIB, 894);
}

DLLEXPORT void _WaitNamedPipeW(void)
{
	JMP(FAKE_LIB, 895);
}

DLLEXPORT void _WideCharToMultiByte(void)
{
	JMP(FAKE_LIB, 896);
}

DLLEXPORT void _WinExec(void)
{
	JMP(FAKE_LIB, 897);
}

DLLEXPORT void _WriteConsoleA(void)
{
	JMP(FAKE_LIB, 898);
}

DLLEXPORT void _WriteConsoleInputA(void)
{
	JMP(FAKE_LIB, 899);
}

DLLEXPORT void _WriteConsoleInputVDMA(void)
{
	JMP(FAKE_LIB, 900);
}

DLLEXPORT void _WriteConsoleInputVDMW(void)
{
	JMP(FAKE_LIB, 901);
}

DLLEXPORT void _WriteConsoleInputW(void)
{
	JMP(FAKE_LIB, 902);
}

DLLEXPORT void _WriteConsoleOutputA(void)
{
	JMP(FAKE_LIB, 903);
}

DLLEXPORT void _WriteConsoleOutputAttribute(void)
{
	JMP(FAKE_LIB, 904);
}

DLLEXPORT void _WriteConsoleOutputCharacterA(void)
{
	JMP(FAKE_LIB, 905);
}

DLLEXPORT void _WriteConsoleOutputCharacterW(void)
{
	JMP(FAKE_LIB, 906);
}

DLLEXPORT void _WriteConsoleOutputW(void)
{
	JMP(FAKE_LIB, 907);
}

DLLEXPORT void _WriteConsoleW(void)
{
	JMP(FAKE_LIB, 908);
}

DLLEXPORT void _WriteFile(void)
{
	JMP(FAKE_LIB, 909);
}

DLLEXPORT void _WriteFileEx(void)
{
	JMP(FAKE_LIB, 910);
}

DLLEXPORT void _WriteFileGather(void)
{
	JMP(FAKE_LIB, 911);
}

DLLEXPORT void _WritePrivateProfileSectionA(void)
{
	JMP(FAKE_LIB, 912);
}

DLLEXPORT void _WritePrivateProfileSectionW(void)
{
	JMP(FAKE_LIB, 913);
}

DLLEXPORT void _WritePrivateProfileStringA(void)
{
	JMP(FAKE_LIB, 914);
}

DLLEXPORT void _WritePrivateProfileStringW(void)
{
	JMP(FAKE_LIB, 915);
}

DLLEXPORT void _WritePrivateProfileStructA(void)
{
	JMP(FAKE_LIB, 916);
}

DLLEXPORT void _WritePrivateProfileStructW(void)
{
	JMP(FAKE_LIB, 917);
}

DLLEXPORT void _WriteProcessMemory(void)
{
	JMP(FAKE_LIB, 918);
}

DLLEXPORT void _WriteProfileSectionA(void)
{
	JMP(FAKE_LIB, 919);
}

DLLEXPORT void _WriteProfileSectionW(void)
{
	JMP(FAKE_LIB, 920);
}

DLLEXPORT void _WriteProfileStringA(void)
{
	JMP(FAKE_LIB, 921);
}

DLLEXPORT void _WriteProfileStringW(void)
{
	JMP(FAKE_LIB, 922);
}

DLLEXPORT void _WriteTapemark(void)
{
	JMP(FAKE_LIB, 923);
}

DLLEXPORT void _ZombifyActCtx(void)
{
	JMP(FAKE_LIB, 924);
}

DLLEXPORT void __hread(void)
{
	JMP(FAKE_LIB, 925);
}

DLLEXPORT void __hwrite(void)
{
	JMP(FAKE_LIB, 926);
}

DLLEXPORT void __lclose(void)
{
	JMP(FAKE_LIB, 927);
}

DLLEXPORT void __lcreat(void)
{
	JMP(FAKE_LIB, 928);
}

DLLEXPORT void __llseek(void)
{
	JMP(FAKE_LIB, 929);
}

DLLEXPORT void __lopen(void)
{
	JMP(FAKE_LIB, 930);
}

DLLEXPORT void __lread(void)
{
	JMP(FAKE_LIB, 931);
}

DLLEXPORT void __lwrite(void)
{
	JMP(FAKE_LIB, 932);
}

DLLEXPORT void _lstrcat(void)
{
	JMP(FAKE_LIB, 933);
}

DLLEXPORT void _lstrcatA(void)
{
	JMP(FAKE_LIB, 934);
}

DLLEXPORT void _lstrcatW(void)
{
	JMP(FAKE_LIB, 935);
}

DLLEXPORT void _lstrcmp(void)
{
	JMP(FAKE_LIB, 936);
}

DLLEXPORT void _lstrcmpA(void)
{
	JMP(FAKE_LIB, 937);
}

DLLEXPORT void _lstrcmpW(void)
{
	JMP(FAKE_LIB, 938);
}

DLLEXPORT void _lstrcmpi(void)
{
	JMP(FAKE_LIB, 939);
}

DLLEXPORT void _lstrcmpiA(void)
{
	JMP(FAKE_LIB, 940);
}

DLLEXPORT void _lstrcmpiW(void)
{
	JMP(FAKE_LIB, 941);
}

DLLEXPORT void _lstrcpy(void)
{
	JMP(FAKE_LIB, 942);
}

DLLEXPORT void _lstrcpyA(void)
{
	JMP(FAKE_LIB, 943);
}

DLLEXPORT void _lstrcpyW(void)
{
	JMP(FAKE_LIB, 944);
}

DLLEXPORT void _lstrcpyn(void)
{
	JMP(FAKE_LIB, 945);
}

DLLEXPORT void _lstrcpynA(void)
{
	JMP(FAKE_LIB, 946);
}

DLLEXPORT void _lstrcpynW(void)
{
	JMP(FAKE_LIB, 947);
}

DLLEXPORT void _lstrlen(void)
{
	JMP(FAKE_LIB, 948);
}

DLLEXPORT void _lstrlenA(void)
{
	JMP(FAKE_LIB, 949);
}

DLLEXPORT void _lstrlenW(void)
{
	JMP(FAKE_LIB, 950);
}
