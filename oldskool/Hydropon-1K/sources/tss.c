#include "tss.h"
#include "commun.h"
#include "memoire.h"

void miseEnPlaceTss(void)
{
	PTSS pTss = (PTSS)0x900, pTss2 = (PTSS)0x800;
	
	zeroMemory(pTss, TAILLETSS);
	zeroMemory(pTss2, TAILLETSS);
	
	pTss->esp0 = 0x8F00;
	pTss->ss0  = SEGDONNEER0;
	
	pTss2->ss0  = SEGDONNEER0;
	pTss2->esp0 = 0x8F00;
	pTss2->cs   = SEGCODE2R3;
	pTss2->esp  = 0x9FF;
	pTss2->ss   = SEGDONNEER3;
	pTss2->cr3  = (unsigned int)0x20000;	
	pTss2->eip  = (unsigned int) 0x50000000;
	return;
}
