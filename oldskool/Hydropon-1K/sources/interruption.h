#ifndef _INTERRUPTION
#define _INTERRUPTION

//Controleur maitre
#define Port1Maitre 0x20
#define Port2Maitre 0x21

//Controleur esclave
#define Port1Esclave 0xA0
#define Port2Esclave 0xA1

//Taille (en octet) de la structure d'une entrée dans l'idt
#define TAILLEINTGATE 8

//Le type d'une interrupt gate avec P=1 && DPL=0
#define INTGATETYPER0    0x8E00 //Interrupt Gate, P=1, DPL=0 1000111000000000

//Le type d'une trap gate avec P=1 && DPL=3 //Trag gate => le flag IF n'est pas touché
#define TRAPGATETYPER3   0xEF00 //Trap Gate, P=1, DPL=3 1110111100000000

//Macro qui va permet de masque l'interruption du clavier en allant dealer avec le controleur d'int
#define MasqueInterruptionClavier EcritureSurPort(Port2Maitre, 2); //00000010

//Macro qui va permet de masque l'interruption du clavier en allant dealer avec le controleur d'int
#define DemasqueInterruptionClavier EcritureSurPort(Port2Maitre, 0); //00000000

//La structure définissant les entrées de l'idt
typedef struct 
{
    unsigned short offset0_15;
    unsigned short segmentSelector;
    unsigned short type;
    unsigned short offset16_31;    
}__attribute__ ((packed)) INTERRUPTGATE, *PINTERRUPTGATE ;

//Structure du registre IDTR
typedef struct
{
	unsigned short limite;
	unsigned int    base;
} __attribute__ ((packed)) IDTR, *PIDTR;


//Fonction qui va créer, charger l'idt (interupt descriptor table)
void chargementIDT(void);

//Fonction qui va configurer les controleurs d'interruptions (maitre/esclave)
void configurationControleursInteruptions(void);

//Fonction qui va forger et remplir une structure du type INTERRUPTGATE
void initialiseDescripteurDeVecteurInt(void*, unsigned short, unsigned short, PINTERRUPTGATE);

//Fonction de traitement des interruptions du clavier ; cette fonction est appelé par traiteInterruptionClavier
void isrIntClavier(void);

//Fonction de traitement des defauts de page, cette fonction est appelé par traitePageFault
void isrPageFault(void);

//Fonction qui prend en charge le traitement des appels systèmes
void isrIntAppelSysteme(void);

//Fonction qui se charge de la protection general
void isrGP(void);

//Fonction de traitement des interruptions qui ne necessitent pas un traitement spécial
extern void traiteInterruptionParDefaut(void);

//Fonction de traitement des interruptions hardware qui ne necessitent pas un traitement spécial (pour le controleur maitre)
extern void traiteInterruptionHardwareParDefautCtrlM(void);

//Fonction de traitement des interruptions hardware qui ne necessitent pas un traitement spécial (pour le controleur esclave)
extern void traiteInterruptionHardwareParDefautCtrlE(void);

//Fonction de traitement des interruptions du clavier
extern void traiteInterruptionClavier(void);

//Fonction de traitement des defauts de pages
extern void traitePageFault(void);

//Fonction de traitement des appels systèmes
extern void traiteAppelSysteme(void);

//Fonction de traitement #GP
extern void traiteGP(void);

#endif
