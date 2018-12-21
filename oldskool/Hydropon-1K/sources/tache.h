#ifndef _TACHE
#define _TACHE

#define TailleTacheUserland (int)((char*)end - (char*)tacheUserland1)
#define AddrTacheUserland    0x40000A00

//Une tache quelconque userland
void tacheUserland1(void);

//une fonction qui peut devenir interessante:]]
void funct(void);

//La victoire est ici
void YOUWINFUCKINGMOFO(void);

//Fonction qui va nous servir à obtenir la taille de la tache
void end(void);

#endif
