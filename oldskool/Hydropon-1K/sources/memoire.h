#ifndef _MEMOIRE
#define _MEMOIRE

#define zeroMemory(x, y) memset_((void*)x, 0, y)

//Fonction equivalent à celle présente dans la libc
void* memcpy(void*, void*, const unsigned int);

//Fonction qui remplis une zone mémoire à un octet precis
void memset_(void* src, unsigned char c, unsigned int taille);

#endif
