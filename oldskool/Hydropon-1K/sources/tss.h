#ifndef _TSS
#define _TSS

#define TAILLETSS 0x68

void miseEnPlaceTss(void);


typedef struct 
{
    unsigned short    previous_task, __previous_task_unused;
    unsigned int      esp0;
    unsigned short    ss0, __ss0_unused;
    unsigned int      esp1;
    unsigned short    ss1, __ss1_unused;
    unsigned int      esp2;
    unsigned short    ss2, __ss2_unused;
    unsigned int      cr3;
    unsigned int      eip, eflags, eax, ecx, edx, ebx, esp, ebp, esi, edi;
    unsigned short    es, __es_unused;
    unsigned short    cs, __cs_unused;
    unsigned short    ss, __ss_unused;
    unsigned short    ds, __ds_unused;
    unsigned short    fs, __fs_unused;
    unsigned short    gs, __gs_unused;
    unsigned short    ldt_selector, __ldt_sel_unused;
    unsigned short    debug_flag, io_map;
} __attribute__ ((packed)) TSS, *PTSS;

extern void YOUWINFUCKINGMOFO(void);

#endif
