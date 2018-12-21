#include "interruption.h"
#include "affichage.h"
#include "memoire.h"
#include "clavier.h"
#include "commun.h"


INTERRUPTGATE idt[256]; //256 entrée -> 0-255

unsigned char* pBuffer = 0;
unsigned int   taille  = 0;

void initialiseDescripteurDeVecteurInt(void* routine, unsigned short segSelecteur, unsigned short type, PINTERRUPTGATE pDescVecteur)
{
	pDescVecteur->offset0_15      = ((unsigned int)routine&0xffff); //On récupère les 2 premiers octets (coté LSB)
	pDescVecteur->offset16_31     = ((unsigned int)routine>>16); //On récupère les 2 derniers octets (du coté MSB)
	pDescVecteur->segmentSelector = segSelecteur;
	pDescVecteur->type            = type;
	return;
}

void chargementIDT(void)
{
	unsigned short i;
	IDTR idtr;

	//On forge notre IDT en mémoire
	for(i = 0 ; i < 256 ; i++)
		initialiseDescripteurDeVecteurInt(AligneAddrSurSegCode(traiteInterruptionParDefaut), SEGCODER0, INTGATETYPER0, &idt[i]);

	//Les ints hw doivent envoyer le EOI au pic
	//Ici un EOI au controleur maitre
	for(i = 32; i < 39+1; i++)
		initialiseDescripteurDeVecteurInt(AligneAddrSurSegCode(traiteInterruptionHardwareParDefautCtrlM), SEGCODER0, INTGATETYPER0, &idt[i]);

	//Ici un EOI au controleur esclave
	for(i = 40; i < 46+1; i++)
		initialiseDescripteurDeVecteurInt(AligneAddrSurSegCode(traiteInterruptionHardwareParDefautCtrlE), SEGCODER0, INTGATETYPER0, &idt[i]);

	//On pose des ISRs pour les interruptions qui nous interessent, celle du clavier en particulier
	//Le clavier est relie à la broche n°2 (en commençant a 1) du controleur d'interruption maitre ;
	//or la première IRQ est associé à l'interruption n° 32 (d'apres notre configuration), c'est donc l'interruption n°33 (en commençant à 0) (0-31 => Reservé pour les exceptions)
	initialiseDescripteurDeVecteurInt(AligneAddrSurSegCode(traiteInterruptionClavier), SEGCODER0, INTGATETYPER0, &idt[33]);

	
	//On installe un handler pour les pagefaults (#PF)
	initialiseDescripteurDeVecteurInt(AligneAddrSurSegCode(traitePageFault), SEGCODER0, INTGATETYPER0, &idt[14]);
	
	//On installe un handler pour gerer les appels systemes
	initialiseDescripteurDeVecteurInt(AligneAddrSurSegCode(traiteAppelSysteme), SEGCODER0, TRAPGATETYPER3, &idt[137]); //stay l33t wiz 137
	
	//On installe un #GP handler
	initialiseDescripteurDeVecteurInt(AligneAddrSurSegCode(traiteGP), SEGCODER0, INTGATETYPER0, &idt[13]);

	//On prepare le registre IDTR contenant l'adresse de base/limite de notre IDT
	idtr.base   = (unsigned int)idt;
	idtr.limite = 256 * TAILLEINTGATE;

	//A present on écrit dans le réel registre IDTR par le bias de l'instruction lidt
	lidt(idtr);
	
	//Il faut stocker le nbr d'interrupt d'horloge a avoir
	*((char*)0x713238) = 59;
	
	//Le chargement de l'idt est ok
	afficheChargementIDTOk();
	return;
}

void configurationControleursInteruptions(void)
{
	//Configuration du registre ICW1 (Initialization Command Word)
	//Configurons le registre ICW1 du port1 maitre -> 00010001
	EcritureSurPort(Port1Maitre, 0x11);     //Registre sur 8b => |0|0|0|1|x|0|x|x|
										   //                            |   | +--- avec ICW4 (1) ou sans (0)
										   //                            |   +----- un seul contrôleur (1), ou cascadés (0)
										   //                            +--------- declenchement par niveau (level) (1) ou par front (edge) (0)
	
	//Configurons le registre ICW1 du port1 esclave
	EcritureSurPort(Port1Esclave, 0x11);


	//Configuration du registre ICW2
	//Configurons le registre ICW2 du port2 maitre
	//IRQ0-7 seront utilisé pour les interruptions n° 32 à 39
	EcritureSurPort(Port2Maitre, 32);	   //Registre sur 8b => |x|x|x|x|x|0|0|0|  
										   //				        	| | | | |
										   //				         	+----------------- adresse de base des vecteurs d'interruption

	//Configurons le registre ICW2 du port2 esclave
	//IRQ8-15 seront utilisé pour les interruptions n° 112 à 120
	EcritureSurPort(Port2Esclave, 112);
	
	//Configuration du registre ICW3
	//Configurons le registre ICW3 du port2 maitre -> 00000100
	//Chaque bit correspond à une broche, le lsb à la broche n° 0 bien evidement, nous avons qu'un controleur d'int branché à la broche n°2
	EcritureSurPort(Port2Maitre, 4);		//Registre sur 8b => |x|x|x|x|x|x|x|x|  pour le maître
										    //                    | | | | | | | |
                                            //                    +------------------ contrôleur esclave rattaché à la broche d'interruption (1), ou non (0)

	//Configurons le registre ICW3 du port2 esclave
	//Le controleur esclave est branché sur la broche n° 2 du controleur maitre
	EcritureSurPort(Port2Esclave, 2);	//Registre sur 8b => |0|0|0|0|0|x|x|x|  pour l'esclave
										//                              | | |
										//                              +-------- Identifiant de l'esclave, qui correspond au numéro de broche IR sur le maître
	
	//Configuration du registre ICW4
	//Configurons le registre ICW4 du port2 maitre
	EcritureSurPort(Port2Maitre, 1);		//Registre sur 8b => |0|0|0|x|x|x|x|1|
											//       					| | | +------ mode "automatic end of interrupt" AEOI (1)
											//					       	| | +-------- mode bufferisé esclave (0) ou maître (1)
											//       					| +---------- mode bufferisé (1)
											//       					+------------ mode "fully nested" (1)
	
	//Configurons le registre ICW4 du port2 esclave
	EcritureSurPort(Port2Esclave, 1);
	
	//On masque l'interruption du clavier
	MasqueInterruptionClavier;
	
	//Les controlleurs sont configurés
	afficheConfigurationControleursIntsOk();
	return;
}

void isrIntClavier(void)
{
	//Pour nous ballader dans le tableau de caractere, on n'est oblige de prendre en compte les touches accompagné d'une autre (ctr, alt, shift etc)
	unsigned char scancode, estMakeCode, estCaractereControle = 0, ajout, caractere;
	static unsigned char shiftPresse = 0, altPresse = 0, ctrlPresse = 0;
	CARACTERE ch;
	
	ch.attribut = forgeCouleurClair(Vert);
	
	//On récupère le scancode de la touche
	LecturePort(PortLectureOuTransmissionDonnees, scancode);
	
	//Si c'est un makecode
	estMakeCode = ToucheEnfonce(scancode);
	
	if(estMakeCode == 0)
		//breakcode = makecode + 0x80
		scancode -= 0x80;
	
	//On récupere les touches spécial appuyé
	switch(scancode)
	{
		case RSHIFTKEY:
        case LSHIFTKEY:
			if(estMakeCode)
			{
				//La touche est bel et bien appuyé
				shiftPresse = 1;
				//C'est un caractère de "controle" nous ne devons pas l'afficher
				estCaractereControle = 1;
			}
			else
				//La touche est relaché
				shiftPresse = 0;
		break;
		
		case CTRLKEY:
            if(estMakeCode)
			{
				ctrlPresse = 1;
				estCaractereControle = 1;
			}
			else
				ctrlPresse = 0;
		break;
		
		case ALTKEY:
			if(estMakeCode)
			{
				altPresse = 1;
				estCaractereControle = 1;
			}
			else
				altPresse = 0;
		break;
	}

	if(estMakeCode && estCaractereControle == 0)	//c'est un makecode, et pas une touche de controle
	{
		//Je considere ici que deux combinaisons possible, shift + letter (=>min/maj), et ctrl+alt+letter (=>char spéciaux)
		//Si on fait un shift + letter
		if(shiftPresse)
			//C'est la colonne n°2 du tableau qui nous intéresse
			ajout = 1;
		else if(ctrlPresse && altPresse)
			ajout = 2;
		else
			ajout = 0;
		
		caractere = kbdmap[scancode*3 + ajout];

		//Si le caractere peut etre imprimé
		if(caractere != SANSAFFICHAGE)
		{
			if(caractere == '\n')
			{
				ch.caractere = '\n';
				((char*)(pBuffer+SEGDONNEER3BASE))[taille] = 0;
				pBuffer = (char*)0;
				taille = 0;
			}
			else
			{	
				ch.caractere = caractere;
				((char*)(pBuffer+SEGDONNEER3BASE))[taille] = caractere;
				taille++;
			}
			afficheUnCaractere(&ch);
		}
	}
	return;
}

void isrPageFault(void)
{
	CHAINE ch;
	ENTIER integ;
	int cr2 = 0;
	
	//L'adresse du defaut de page se situe dans le cr2
	asm volatile
	(
		"movl %%cr2, %0"
		: "=r" (cr2)
		:
	);
	
	ch.attribut = forgeCouleurClair(Rouge);
	ch.chaine   = "\n*** Page Fault @ 0x";
	
	integ.attribut = ch.attribut;
	integ.entier   = cr2;
	
	afficheUneChaine(&ch);
	afficheUnEntier(&integ);
	
	ch.chaine = "***\n";
	afficheUneChaine(&ch);
	
	while(1);
	return;
}

//EAX=>id syscall
void isrIntAppelSysteme(void)
{
	unsigned int idSyscall, arg1, arg2;
	CHAINE ch;
	
	ch.attribut = forgeCouleurClair(Rouge);
	
	asm volatile
	(
		"movl %%eax, %0\n"
		"movl %%ebx, %1\n"
		"movl %%ecx, %2\n"
		: "=g" (idSyscall) , "=g" (arg1), "=g" (arg2)
		:
	);
	
	switch(idSyscall)
	{
		case 0x1337:
			//EBX=>ptr sur le buffer
			pBuffer = (char*)arg1;
			DemasqueInterruptionClavier;
			while(pBuffer != 0);
		break;
		
		case 0x137:
			//EBX=>ptr sur la chaine null-terminated
			ch.chaine = (char*)(SEGDONNEER3BASE + (char*)arg1);
			afficheUneChaine(&ch);
		break;
		
		case 0x138:
			ch.chaine = "\n*** You Win !1!1§&&&! ***\n";
			afficheUneChaine(&ch);
			while(1);
		break;
	}
	return;
}

void isrGP(void)
{
	CHAINE a;
	a.attribut = forgeCouleurClair(Rouge);
	a.chaine   = "\n*** #GP ***\n";
	afficheUneChaine(&a);
	
	while(1);
	return;
}
