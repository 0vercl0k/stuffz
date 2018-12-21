#include "commun.h"
#include "affichage.h"
#include "interruption.h"
#include "pagination.h"
#include "tache.h"
#include "memoire.h"
#include "tss.h"

void enterInMatrix(void)
{	
	char* addr = (char*)0x400000+TailleTacheUserland;
	
	//On evite invalide tout de suite la ldt (thks Ivanlef0u o/)
	asm volatile
	(
		"xor %ax, %ax\n"
		"lldt %ax\n"
	);

	//On protège l'espace userland des ptits malins (thks deim0s ;))
	memset_((void*)addr, 0xFA, 0x31f600);

	//Noyau chargé :))
	afficheNoyauOk();
	
	//Set-up la tss
	miseEnPlaceTss();

	//Nous forgeons notre IDT, nous la chargeons en mémoire
	chargementIDT();
	
	//Configuration des controleurs d'interruptions
	configurationControleursInteruptions();
		
	//On peut lancer la pagination
	miseEnPlacePagination();
	
	//On peut maintenant dé-masquer les interruptions
	DemasqueInt;
	afficheInterruptionsDemasquesOk();
	
	//On recopie la tache là où il faut
	memcpy((void*)tacheUserland1, (void*)AddrTacheUserland, TailleTacheUserland);
	
	//On recopie la fonction magique
	memcpy((void*)YOUWINFUCKINGMOFO, (void*)0x50000000, 10);
	
	//On prepare le software task switching
	asm volatile
	(
		"pushl %0\n"               //SS
		"pushl $0x9FF\n"           //ESP
		"pushfl\n" 
		"popl %%eax\n"
		"and $0xffffbfff, %%eax\n" //EFLAGS.NT = 0 => on veut pas faire de task-return hardware cf man intel
		"push %%eax\n"             //EFLAGS
		"pushl %1\n"               //CS
		"pushl $0x0\n"             //EIP
		"movw %2, %%ax\n"
		"movw %%ax, %%ds\n"
		"movw %3, %%ax\n"
		"ltr %%ax\n"
		"iret\n"
		:
		:"g" (SEGSTACKR3), "g" (SEGCODER3), "g" (SEGDONNEER3), "g" (SEGTSSR3)
	);
	while(1);
}
