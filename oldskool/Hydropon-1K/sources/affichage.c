#include "affichage.h"
#include "commun.h"
#include "memoire.h"

unsigned char posX = 0;
unsigned char posY = 18;

void afficheUnCaractere(const PCARACTERE a)
{
	char* pVideo = MemoireVideo;
		
	//Si nous arrivons à la fin de la ligne
	if(posX > LARGEUR_ECRAN)
	{
		posY += 1;
		posX = 0;
	}
	
	switch(a->caractere)
	{
		case '\n':
			posY += 1;
			posX = 0;
		break;
		
		case '\t':
			posX+=4;
		break;
		
		
		case '\b':
			//Si nous reculons et que nous sommes au debut de la première ligne
			if( (posX == 0) && (posY > 0) )
			{
				//Nous remontons à la ligne precedente
				posY--;
								
				//Nous remettons le curseur à la fin de la ligne
				posX = LARGEUR_ECRAN;
			}
			//Sinan, on peut réécrire le caractère precedent
			else
			{
				pVideo[posX+posY*LARGEUR_ECRAN -1] = 0;
				pVideo[posX+posY*LARGEUR_ECRAN -2] = 0;
				posX -= 2;
			}
		break;
		
		
		default:
		pVideo[posX + posY*LARGEUR_ECRAN]     = a->caractere;
		pVideo[posX + posY*LARGEUR_ECRAN + 1] = a->attribut;
		posX+=2;
	}
	return;
}
	
void afficheUneChaine(const PCHAINE a)
{
	CARACTERE ch;
	char* chaine = a->chaine;
	
	ch.attribut = a->attribut;
	
	for(; *chaine ; chaine++)
	{
		ch.caractere = *chaine;
		afficheUnCaractere(&ch);
	}
	return;
}

void afficheUneChaineVerte(const char * a)
{
	CHAINE ch;
	
	ch.chaine = (char*)a;
	ch.attribut = forgeCouleurClair(Vert);
	
	afficheUneChaine(&ch);
	return;
}

void afficheNoyauOk(void)
{
	CHAINE b;
	
	b.chaine   = "Noyau\t\t\t\t\t\t\t\t\t\t\t [OK]\n";
	b.attribut = forgeCouleur(Blanc);
	
	afficheUneChaine(&b);
	zeroMemory((char*)0x713233, 7);
	return;
}

void afficheChargementIDTOk(void)
{
	CHAINE b;
	
	b.chaine = "IDT \t\t\t\t\t\t\t\t\t\t\t\t[OK]\n";
	b.attribut = forgeCouleur(Blanc);
	
	afficheUneChaine(&b);
	return;
}

void afficheInterruptionsDemasquesOk(void)
{
	CHAINE b;
	
	b.chaine = "Interruptions Demasquees\t\t[OK]\n";
	b.attribut = forgeCouleur(Blanc);
	
	afficheUneChaine(&b);

	return;
}

void affichageInterruption(void)
{
	CHAINE ch;
	
	ch.chaine   = "Clavier!! !\n";
	ch.attribut = forgeCouleurClair(Rouge);
	
	afficheUneChaine(&ch);
	return;
}

void afficheConfigurationControleursIntsOk(void)
{
	CHAINE ch;
	
	ch.chaine = "Controleurs d'interruptions [OK]\n";
	ch.attribut = forgeCouleur(Blanc);
	
	afficheUneChaine(&ch);
	return;
}

void afficheUnEntier(const PENTIER in)
{
	unsigned char i, digit;
	char chaine[10];
	CHAINE ch;
	
	ch.attribut = in->attribut;
	ch.chaine   = chaine;
		
	//Null terminated string
	chaine[9] = 0;
	
	//On ajoute un espace
	chaine[8] = ' ';
	
	//On parcours chaque digit de l'entier
	for(i = 0; i < 8; i++)
	{
		//On forge notre chaine
		digit = RecupereDigit(i, in->entier);

		//Si le nombre est > 9, on fait en sorte que le digit (nombre entres 10 et 15) affiche la lettre associé ('A' = 0x41, le nombre minimal etant 10, 0x41-10=0x37)
		if(digit > 9)
			chaine[7-i] = 0x37 + digit;	
		else
			//Sinan c'est un nombre entres 0 et 9
			chaine[7-i] =  digit + '0';
	}
		
	afficheUneChaine(&ch);
	
	return;
}
