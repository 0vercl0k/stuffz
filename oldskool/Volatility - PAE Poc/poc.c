#include <stdio.h>
#include <string.h>
#include <windows.h>

#include "toolbox.h"

typedef FILE* PFILE;

#define PKPCR       (unsigned int)0xffdff000
#define FILE2OPEN "C:\\Users\\0vercl0k\\Downloads\\hn_forensics\\hn_forensics\\Bob.vmem"

/** <OFFSET WINXPSP2 SPECIFIC> **/

/**    +0x018 DirectoryTableBase : Uint4B **/
#define PDBR_OFFSET 0x18

/**    +0x174 ImageFileName    : [16] UChar **/
#define IMAGEFILENAME_OFFSET 0x174

/**    +0x088 ActiveProcessLinks : _LIST_ENTRY **/
#define ACTIVEPROCESSLINK_OFFSET 0x88

/**    +0x084 UniqueProcessId  : Ptr32 Void **/
#define PID_OFFSET 0x84

/**
    kd> dps poi(0xffdff000+0x34)
    8054c738  0a28000f
    8054c73c  00020006
    8054c740  030c014c
    8054c744  0000002d
    8054c748  804d7000 nt!_imp__VidInitialize <PERF> (nt+0x0)
    8054c74c  ffffffff
    8054c750  8055ab20 nt!PsLoadedModuleList
    8054c754  ffffffff
    8054c758  806921f4 nt!KdpDebuggerDataListHead
    8054c75c  ffffffff
    8054c760  806921f4 nt!KdpDebuggerDataListHead
    8054c764  806921f4 nt!KdpDebuggerDataListHead
    8054c768  00000000
    8054c76c  00000000
    8054c770  4742444b
    8054c774  00000290
    8054c778  804d7000 nt!_imp__VidInitialize <PERF> (nt+0x0)
    8054c77c  00000000
    8054c780  804e3b25 nt!RtlpBreakWithStatusInstruction
    8054c784  00000000
    8054c788  00000000
    8054c78c  00000000
    8054c790  0008012c
    8054c794  00000018
    8054c798  804e3195 nt!KiCallUserMode
    8054c79c  00000000
    8054c7a0  7c91ead0
    8054c7a4  00000000
    8054c7a8  8055ab20 nt!PsLoadedModuleList
    8054c7ac  00000000
    8054c7b0  80560bd8 nt!PsActiveProcessHead
**/
#define KdVersionBlock2PsActiveProcessList 0x78

/** </OFFSET WINXPSP2 SPECIFIC> **/

/** <PAGING WITH PAE STUFF> **/

#define IsEntryPresent(x)           ((x & 0x1) == 1)
#define IsLargePage(x)              ((x & 0x80) == 0x80)
#define CR3ToPDPTE(x)               (x&0xFFFFFFE0)
#define VaddrToIdInPDPTE(x)         (x>>0x1E)
#define VaddrToIdInPageDirectory(x) ((x>>21)&0x1FF)
#define VaddrToIdInPageTable(x)     ((x>>12)&0x1FF)
#define VaddrToOffsetInPage(x)      (x&0x00000FFF)

/** </PAGING WITH PAE STUFF> **/

unsigned int getFileSize(FILE* fp)
{
    unsigned int size = 0;

    fseek(fp, 0, SEEK_END);
    size = ftell(fp);
    fseek(fp, 0, SEEK_SET);

    return size;
}

unsigned int findEprocess(FILE* fp, unsigned char* processName)
{
    unsigned int i                = 0,
                 end              = 0,
                 ret              = 0;
    unsigned char typeSign        = 0x3,
                   absoInsertSign = 0,
                   sizeSign       = 0x1b,
                   tmp[4]         = {0},
                   tmp2[16]       = {0},
                   isEprocess     = 0;

    end = getFileSize(fp);

    for(; i < end; i += 8)
    {
        fseek(fp, i, SEEK_SET);
        ret = fread(tmp, sizeof(char), 4, fp);
        if(ret != 4)
            _ERROR_();

        /**
        kd> dt nt!_EPROCESS 0x80559580 -r
           +0x000 Pcb              : _KPROCESS
              +0x000 Header           : _DISPATCHER_HEADER
                 +0x000 Type             : 0x3 ''
                 +0x001 Absolute         : 0 ''
                 +0x002 Size             : 0x1b ''
                 +0x003 Inserted         : 0 ''

        **/

        if(tmp[0] == typeSign && tmp[1] == absoInsertSign &&
           tmp[2] == sizeSign && tmp[3] == absoInsertSign)
        {
            ZeroMemory(tmp2, 16);

            fseek(fp, -4, SEEK_CUR);

            fseek(fp, IMAGEFILENAME_OFFSET, SEEK_CUR);
            ret = fread(tmp2, sizeof(char), 16, fp);
            if(ret != 16)
                _ERROR_();

            tmp2[15] = 0;

            isEprocess = (_stricmp((char*)tmp2, (char*)processName) == 0)?1:0;

            if(isEprocess)
                return i;
        }
    }

    return FAIL;
}

unsigned int findPageDirectoryBase(FILE* fp)
{
    unsigned int offsetPageDirectoryBase = FAIL,
                 offsetEprocess          = 0,
                 ret                     = 0;

    offsetEprocess = findEprocess(fp, (unsigned char*)"Idle");
    if(IsAFailure(offsetEprocess))
        _ERROR1_("Eprocess wasn't found.");

    fseek(fp, offsetEprocess+PDBR_OFFSET, SEEK_SET);

    ret = fread(&offsetPageDirectoryBase, sizeof(unsigned int), 1, fp);
    if(ret != 1)
        _ERROR_();

    return offsetPageDirectoryBase;
}

unsigned int vaddrR0ToPaddrPAE(FILE* fp, unsigned int vaddr, unsigned char enableOutput)
{
    static unsigned int cr3              = 0,
                        basePdpte        = 0;
    unsigned int paddr                   = FAIL,
                 idInPdpte               = 0,
                 idInPageDirectory       = 0,
                 idInPageTable           = 0,
                 idInPage                = 0,
                 ret                     = 0;
    unsigned long long basePageDirectory = 0,
                       basePageTable     = 0,
                       basePage          = 0;

    if(cr3 == 0)
    {
        cr3 = findPageDirectoryBase(fp);
        if(cr3 == FAIL)
            _ERROR1_("CR3 wasn't found.");

        basePdpte = CR3ToPDPTE(cr3);
    }

    if(enableOutput)
        printf("\r\n[INFOS] Page Directory is at 0x%x.\r\n", basePdpte);

    idInPdpte         = VaddrToIdInPDPTE(vaddr);
    idInPageDirectory = VaddrToIdInPageDirectory(vaddr);
    idInPageTable     = VaddrToIdInPageTable(vaddr);
    idInPage          = VaddrToOffsetInPage(vaddr);


    fseek(fp, basePdpte + (idInPdpte * 8), SEEK_SET);
    ret = fread(&basePageDirectory, sizeof(unsigned long long), 1, fp);
    if(ret != 1)
        _ERROR_();

    if(!IsEntryPresent(basePageDirectory))
        _ERROR1_("Entry isn't present.");

    if(enableOutput)
        printf("[INFOS] PAE PDPE 0x%x - 0x%llx.\r\n", (basePdpte + (idInPdpte * 8)), basePageDirectory);

    basePageDirectory &= 0x00006FFFFFFFFF000;

    fseek(fp, basePageDirectory + (idInPageDirectory * 8), SEEK_SET);
    ret = fread(&basePageTable, sizeof(unsigned long long), 1, fp);
    if(ret != 1)
        _ERROR_();

    if(enableOutput)
        printf("[INFOS] PAE PDE  0x%x - 0x%llx.\r\n", (basePageDirectory + (idInPageDirectory * 8)), basePageTable);

    if(!IsEntryPresent(basePageTable))
        _ERROR1_("Entry isn't present.");

    if(IsLargePage(basePageTable))
    {
        /** Entry which map a 2MBytes page **/
        paddr = (basePageTable&0xFFE00000) + (vaddr & 0x1fffff);
        if(enableOutput)
            printf("[INFOS] Virtual address 0x%x translates to physical address 0x%x (large page, 2MBytes page).\r\n\r\n", vaddr, paddr);

        return paddr;
    }

    basePageTable &= 0x00006FFFFFFFFF000;

    fseek(fp, basePageTable + (idInPageTable * 8), SEEK_SET);
    ret = fread(&basePage, sizeof(unsigned long long), 1, fp);
    if(ret != 1)
        _ERROR_();

    if(enableOutput)
        printf("[INFOS] PAE PTE  0x%x - 0x%llx.\r\n", (basePageTable + (idInPageTable * 8)), basePage);

    if(!IsEntryPresent(basePage))
        _ERROR1_("Entry isn't present.");

    basePage &= 0x00006FFFFFFFFF000;

    paddr = (unsigned int)basePage + idInPage;

    if(enableOutput)
        printf("[INFOS] Virtual address 0x%x translates to physical address 0x%x.\r\n\r\n", vaddr, paddr);

    return paddr;
}


int main()
{
	PFILE pFile                              = NULL;
    unsigned int vaddrKpcr                   = PKPCR,
                 paddrKpcr                   = 0,
                 vaddrKdVersionBlock         = 0,
                 paddrKdVersionBlockPsActive = 0,
                 vaddrPsActiveProcessHead    = 0,
                 paddrPsActiveProcessHead    = 0,
                 current                     = 0,
                 start                       = 0,
                 tmp                         = 0,
                 pid                         = 0,
                 startTick                   = 0,
                 endTick                     = 0;
    char processName[16]                     = {0};

	printf("** VMEM Forensic : Find the PsActiveProcessHead (IA-32 WinXpSP2-PAE-4kbPages) by 0vercl0k **\r\n");

    startTick = GetTickCount();

	pFile = fopen(FILE2OPEN, "rb");
	if(pFile == NULL)
		_ERROR_();

    paddrKpcr = vaddrR0ToPaddrPAE(pFile, vaddrKpcr, 1);
    if(IsAFailure(paddrKpcr))
        _ERROR1_("Virtual address translation fails.");

    printf("Physical address of KPCR structure : 0x%x.\r\n", paddrKpcr);

    /**    +0x034 KdVersionBlock   : 0x8054c738 **/
    paddrKpcr += 0x34;
    fseek(pFile, paddrKpcr, SEEK_SET);
    fread(&vaddrKdVersionBlock, sizeof(unsigned int), 1, pFile);

    printf("Virtual address of KdVersionBlock : 0x%x.\r\n", vaddrKdVersionBlock);

    vaddrKdVersionBlock        += KdVersionBlock2PsActiveProcessList;
    paddrKdVersionBlockPsActive = vaddrR0ToPaddrPAE(pFile, vaddrKdVersionBlock, 1);
    if(IsAFailure(paddrKdVersionBlockPsActive))
        _ERROR1_("Virtual address translation fails.");

    printf("Hmm well, you can find nt!PsActiveProcessHead at 0x%x.\r\n", paddrKdVersionBlockPsActive);

    fseek(pFile, paddrKdVersionBlockPsActive, SEEK_SET);
    fread(&vaddrPsActiveProcessHead, sizeof(unsigned int), 1, pFile);

    printf("Virtual address of nt!PsActiveProcessHead is 0x%x.\r\n", vaddrPsActiveProcessHead);
    printf("\r\n\t\t*|* DROP IT LIKE ITS HOT, DROP IT LIKE ITS HOT *|*\r\n\r\n");

    paddrPsActiveProcessHead = vaddrR0ToPaddrPAE(pFile, vaddrPsActiveProcessHead, 0);
    if(IsAFailure(paddrPsActiveProcessHead))
        _ERROR1_("Virtual address translation fails.");


    fseek(pFile, paddrPsActiveProcessHead, SEEK_SET);
    fread(&current, sizeof(unsigned int), 1, pFile);

    start = vaddrPsActiveProcessHead;

    do
    {
        current -= ACTIVEPROCESSLINK_OFFSET;
        current += IMAGEFILENAME_OFFSET;

        tmp = vaddrR0ToPaddrPAE(pFile, current, 0);
        if(IsAFailure(tmp))
            _ERROR1_("Virtual address translation fails.");

        fseek(pFile, tmp, SEEK_SET);
        fread(processName, 16, 1, pFile);

        fseek(pFile, (tmp - IMAGEFILENAME_OFFSET) + PID_OFFSET, SEEK_SET);
        fread(&pid, sizeof(unsigned int), 1, pFile);

        printf("- %s(%d).\r\n", processName, pid);

        tmp -= IMAGEFILENAME_OFFSET;
        tmp += ACTIVEPROCESSLINK_OFFSET;

        fseek(pFile, tmp, SEEK_SET);
        fread(&current, sizeof(unsigned int), 1, pFile);
    }while(start != current);

	fclose(pFile);

    endTick = GetTickCount();
    printf("Elapsed time : %u ms.\r\n", (endTick-startTick));

	return SUCCESS;
}
