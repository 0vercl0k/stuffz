#ifndef _AFFICHAGE
#define _AFFICHAGE

typedef enum
{
    Noir=0,
	Bleu,
	Vert,
	Cyan,
	Rouge,
	Magenta,
	Jaune,
	Blanc
} Couleur;

typedef struct 
{
	char caractere;
	char attribut;
}CARACTERE, *PCARACTERE;

typedef struct
{
	char* chaine;
	char attribut;
}CHAINE, *PCHAINE;

typedef struct
{
	int entier;
	char attribut;
}ENTIER, *PENTIER;

#define MemoireVideo (char*)0xB8000
#define LARGEUR_ECRAN 160

//Macro pour le parametrage du champs attribut des structures CHAINE, CARACTERE
#define forgeCouleurClair(couleur) forgeAttribut(0, Noir, 1, couleur)
#define forgeCouleur(couleur) forgeAttribut(0, Noir, 0, couleur)
#define forgeAttribut(cli, background, surInt, couleur) (char)(couleur+((surInt)<<3)+((background)<<4)+((cli)<<7))

//Fonction qui affiche un caractère à l'ecran
void afficheUnCaractere(const PCARACTERE);

//Fonction qui affiche à l'ecran une chaine de caractère null terminated
void afficheUneChaine(const PCHAINE);

//Fonction qui affiche un entier à l'ecran
void afficheUnEntier(const PENTIER);

//Fonction qui affiche à l'ecran une chaine de caractère de couleur verte clair
void afficheUneChaineVerte(const char* a);

//Fonction qui affiche le message de succès du chargement du noyau
void afficheNoyauOk(void);

//Fonction qui affiche un message nous informant que l'idt à belle ete bien chargé
void afficheChargementIDTOk(void);

//Fonction qui affiche un message nous informant que les interruptions ont été demasqué
void afficheInterruptionsDemasquesOk(void);

//Fonction appelé par les ISRs associé au interruption "basique", celle qui n'ont besoin d'aucun traitement particulier
void affichageInterruption(void);

//Fonction qui affiche un message nous informant que les controleurs d'interruptions ont été configués
void afficheConfigurationControleursIntsOk(void);

#endif
