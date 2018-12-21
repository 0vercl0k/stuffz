#ifndef _COMMUN
#define _COMMUN

//Fonction puissance
int puissance(int, int);

//Segment selector avec lequel nous allons chercher l'entrée x dans la gdt
#define SEGCODER0   0x8  //001-0-00
#define SEGDONNEER0 0x10 //010-0-00

#define SEGCODER3   0x1B //011-0-11
#define SEGCODE2R3  0x43 //1000-0-11
#define SEGDONNEER3 0x23 //100-0-11
#define SEGSTACKR3  SEGDONNEER3
#define SEGTSSR3    0x2B //101-0-11

#define SEGDONNEER3BASE 0x40000000
#define SEGCODER3BASE   0x40

//Addresse de base du segment de code
#define AddrBaseSegCode 0x1000

//Macro permettant d'aligner l'adresse par rapport à l'adresse de base du segment de code
#define AligneAddrSurSegCode(x) (void*)((char*)x-AddrBaseSegCode)

//Macro qui recupére un digit d'un entier
#define RecupereDigit(num, entier) (((entier)&(0xf*(puissance(0x10,num))))>>(4*num))

//Encapsulation d'instruction asm dans des macros c
//Volatile informe gcc que nous voulons que le code ne soit pas réorganisé/optimisé, il doit resté tel quel

#define ModifierCr3(x) 	asm volatile("movl %%eax, %%cr3" ::	"a" (x))

//Magic breakpoint @ bochs
#define Breakpoint  asm volatile("xchg %bx, %bx")

//Masque les interruptions
#define MasqueInt   asm volatile("cli")

//Demasque les interruptions
#define DemasqueInt asm volatile("sti")

//Ecriture sur un port I/O du processeur
#define EcritureSurPort(nPort, valeur) asm volatile("outb %%al, %%dx" :: "d" (nPort), "a" (valeur))

//lit un octet sur un port
#define LecturePort(port, var) asm volatile ("inb %%dx, %%al" : "=a" (var) : "d" (port))

//Charge une structure de type IDTR dans le registre IDTR par le biais de lidt
#define lidt(x) asm volatile("lidtl %0" :: "g"(x))

#endif
