#include "commun.h"
#include "memoire.h"

void* memcpy(void* src, void* dest, const unsigned int taille)
{
	unsigned int i;
	char* pDest = (char*) dest;
	for(i = 0; i < taille; i++)
		pDest[i] = ((char*)src)[i];
	
	return pDest;
}

void memset_(void* src, unsigned char c, unsigned int taille)
{
	unsigned int i;
	char* dest = (char*)src;
	
	for(i = 0 ; i < taille ; i++)
		dest[i] = c;
	return;
}
