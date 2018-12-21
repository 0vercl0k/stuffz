#include "pagination.h"
#include "commun.h"
#include "memoire.h"

void miseEnPlacePagination(void)
{
	int* repertoireTablePage = (int*)ADDR_DIRECTORY_TABLE_PAGE, *tablePage0 = (int*)ADDR_TABLE_PAGE0, *tablePage1 = (int*) ADDR_TABLE_PAGE1, *tablePage2 = (int*)ADDR_TABLE_PAGE2,  i, addrPage = 0;
	
	//On remet à 0 le repertoire de page
	zeroMemory(repertoireTablePage, 1024*4);
	
	//Identity Mapping, de 0x0-0x003ffff (Addr Physique) <-> 0x0-0x003fffff (AddrVirtuel)
	//Une entrée dans le repertoire de page suffit à adresse 4Mo => 1024 entrée dans la table de page, donc 1024 page de 4ko adressable soit 1024*(1024*4)=0x40000000
	repertoireTablePage[0] = (int)((char*)tablePage0 + 1 + (1<<1)); //P=1, RW=1, US=0 (non acces au ring3)
		
	//Nous remplissons la table de page n°0
	for(i = 0; i < 1024; i++, addrPage += 1024*4) //Chaque page = 4ko = 1024*4
		tablePage0[i] = addrPage + (1<<1) + 1; //P=1, RW=1, US=0
	
	//Mapping de 0x0040000 (Addr Phys) <-> 0x40000000 (AddrV)
	repertoireTablePage[IndiceDansLeRepertoireDePage(0x40000000)] = (int)((char*)tablePage1 + 1 + (1<<1) + (1<<2)); //P=1, RW=1, US=1 (access au ring3)

	//Nous remplissons la table de page n°1
	for(i = 0; i < 1024; i++, addrPage += 1024*4)//1; i++, addrPage += 1024*4)
		tablePage1[i] = addrPage + (1<<2) + (1<<1) + 1;//P=1, RW=1, US=1
	
	repertoireTablePage[IndiceDansLeRepertoireDePage(0x50000000)] = (int)((char*)tablePage2 + 1 + (1<<1) + (1<<2)); //P=1, RW=1, US=1 (access au ring3)

	//Nous remplissons la table de page n°2
	for(i = 0; i < 1; i++, addrPage += 1024*4)//1; i++, addrPage += 1024*4)
		tablePage2[i] = addrPage + (1<<2) + (1<<1) + 1;//P=1, RW=1, US=1

	//On stock dans le cr3 l'adresse du repertoire de table de pages
	ModifierCr3(repertoireTablePage);
	
	//On set la pagination en modifiant le bit n°31 (debut à 0) à 1 (cr0.PG)
	asm volatile
	(
		"movl %cr0, %eax\n"
		"or $0x80000000, %eax\n"
		"movl %eax, %cr0\n"
	);
	
	//On stocke un identifiant valide
	*((char*)0x40313233) = 154;

	return;
}

