#include "tache.h"
#include "commun.h"
#include "memoire.h"

void tacheUserland1(void)
{
	int a = 0;
	a += 0xfffd;
	
	//BOF here
	funct();
	
	//Test du page fault
	//*((unsigned char*)a) = 0xFF;
	
	//Test du #gp
	//asm volatile("cli");
	
	while(1);
}

void funct(void)
{
	char tapz[3];
	asm volatile
	(
		"movl $0x1337, %%eax\n"
		"movl %0, %%ebx\n"
		"int $0x89\n"		
		"movl $0x137, %%eax\n"
		"int $0x89\n"
		:
		: "g" (tapz), "g" (tapz)
	);
}
	
void end(void){}


void YOUWINFUCKINGMOFO(void)
{
	asm volatile
	(
		"movl $0x138, %eax\n"
		"int $0x89\n"
	);
}
