#include "debug.c"

#define BP (PDWORD)0x00461005

int main()
{
    PROCESS_INFORMATION iProcess = {0};
    STARTUPINFOA iStartup = {0};
    unsigned int ret = 0;
    PCHAR procDump = NULL;
    DWORD tailleBin = 0;
    HANDLE hFile = 0;
    DWORD nbByte = 0, imgBase = 0;

    iStartup.cb = sizeof(STARTUPINFOA);

    printf("Defe4t Lilxam's packer par 0vercl0k.\n\n[*] Creation du processus..\n");

    ret = CreateProcess("UnpackMe.exe", NULL, NULL, NULL, FALSE, DEBUG_ONLY_THIS_PROCESS|DEBUG_PROCESS, NULL, NULL, &iStartup, &iProcess);
    if(ret == 0)
    {
        printf("[!] Erreur @ CreateProcess : 0x%x.\n", (unsigned int)GetLastError());
        return 0;
    }

    printf("[*] Initialisation du debug..\n");
    imgBase = initialisationDebug();

    printf("[*] Pose d'un hardware-breakpoint à l'original-entry-point..\n");

    if(goToHW(BP, iProcess.hThread) == 0)
    {
        printf("[!] Erreur @ goTo.\n");
        return 0;
    }

    printf("[*] Dump en cours..\n");
    procDump = dumpProcessus(iProcess.hProcess, (PCHAR)imgBase, &tailleBin, 0x1220);

    hFile = CreateFile("dumped.exe", GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
    if(hFile == INVALID_HANDLE_VALUE)
    {
        dprintf("[!] Erreur @ CreateFile() : 0x%x.\n", (unsigned int)GetLastError());
        free(procDump);
        return 0;
    }

    printf("[*] Ecriture du dump .%x.\n", tailleBin);

    ret = WriteFile(hFile, procDump, tailleBin, &nbByte, NULL);
    if(ret == FALSE || nbByte != tailleBin)
    {
        dprintf("[!] Erreur @ fwrite().\n");
        free(procDump);
        CloseHandle(hFile);
        return 0;
    }

    CloseHandle(hFile);
    free(procDump);
    return 1;
}
