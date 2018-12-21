#ifndef _CLAVIER
#define _CLAVIER

#define PortLectureOuTransmissionDonnees 0x60

//Scan code des touches "special"
#define LSHIFTKEY   0x2a
#define RSHIFTKEY   0x36
#define ALTKEY      0x38
#define CTRLKEY     0x1D


//Il nous faut un scancode indiquant que la combinaisons realisé avec la touche ne produit aucun affichage
#define SANSAFFICHAGE 0

//Si le scancode a le bit n°7 (on commence à 0) à 1 c'est un break code, sinan un make code
#define ToucheEnfonce(x) (x < 0x80) //Si touche enfoncé scancode = make code, si la touche est relaché scancode = break code = make code + 0x80

char kbdmap[] = {
	0xFF, 0xFF, 0xFF,
	SANSAFFICHAGE, SANSAFFICHAGE, SANSAFFICHAGE,	//Echap (0x01)
	'&', '1', SANSAFFICHAGE,
	'é', '2', '~',
	'"', '3', '#',
	'\'', '4', '{',
	'(', '5', '[',
	'-', '6', '|',
	'è', '7', '`',
	'_', '8', '\\',
	'ç', '9', '^',
	'à', '0', '@',
	')', '°', ']',
	'=', '+', '}',
	'\b', '\b', SANSAFFICHAGE,	//backspace (0xE)
	'\t', '\t', '\t',	//tab (0xF)
	'a', 'A', 'a',
	'z', 'Z', 'z',
	'e', 'E', 'e',
	'r', 'R', 'r',
	't', 'T', 't',
	'y', 'Y', 'y',
	'u', 'U', 'u',
	'i', 'I', 'i',
	'o', 'O', 'o',
	'p', 'P', 'p',
	'^', '¨', '^',
	'$', '£', '$',
	'\n', '\n', '\n',//Enter (0x1C)
	SANSAFFICHAGE,SANSAFFICHAGE, SANSAFFICHAGE,//Ctrl (0x1D)
	'q', 'Q', 'q',
	's', 'S', 's',
	'd', 'D', 'd',
	'f', 'F', 'f',
	'g', 'G', 'g',
	'h', 'H', 'h',
	'j', 'J', 'j',
	'k', 'K', 'k',
	'l', 'L', 'l',
	'm', 'M', 'm',
	'ù', '%', SANSAFFICHAGE,
	'²', SANSAFFICHAGE, SANSAFFICHAGE,	//²
	SANSAFFICHAGE, SANSAFFICHAGE, SANSAFFICHAGE, //LShift (0x2a)
	'*', 'µ', SANSAFFICHAGE,
	'w', 'W', 'w',
	'x', 'X', 'x',
	'c', 'C', 'c',
	'v', 'V', 'v',
	'b', 'B', 'b',
	'n', 'N', 'n',
	',', '?', ',',
	';', '.', ';',
	':', '/', ':',
	'!', '§', '!',
	SANSAFFICHAGE, SANSAFFICHAGE, SANSAFFICHAGE, //Rshift (0x36)
	0xFF, 0xFF, 0xFF,
	0xFF, 0xFF, 0xFF,
	' ' , ' ', ' ',  //Espace (0x39)
	0xFF, 0xFF, 0xFF,
	SANSAFFICHAGE, SANSAFFICHAGE, SANSAFFICHAGE, //F1 (0x3B)
	SANSAFFICHAGE, SANSAFFICHAGE, SANSAFFICHAGE, //F2 (0x3C)
	SANSAFFICHAGE, SANSAFFICHAGE, SANSAFFICHAGE, //F3 (0x3D)
	SANSAFFICHAGE, SANSAFFICHAGE, SANSAFFICHAGE, //F4 (0x3E)
	SANSAFFICHAGE, SANSAFFICHAGE, SANSAFFICHAGE, //F5 (0x3F)
	SANSAFFICHAGE, SANSAFFICHAGE, SANSAFFICHAGE, //F6 (0x40)
	SANSAFFICHAGE, SANSAFFICHAGE, SANSAFFICHAGE, //F7 (0x41)
	SANSAFFICHAGE, SANSAFFICHAGE, SANSAFFICHAGE, //F8 (0x42)
	SANSAFFICHAGE, SANSAFFICHAGE, SANSAFFICHAGE, //F9 (0x43)
	SANSAFFICHAGE, SANSAFFICHAGE, SANSAFFICHAGE, //F10 (0x44)
	0xFF, 0xFF, 0xFF,
	0xFF, 0xFF, 0xFF,
	SANSAFFICHAGE, SANSAFFICHAGE, SANSAFFICHAGE,// Fleche oblique vers la gauche(0x47)
	0xFF, 0xFF, 0xFF,
	SANSAFFICHAGE, SANSAFFICHAGE, SANSAFFICHAGE,//Fleche rapide vers le haut(0x49)
	0xFF, 0xFF, 0xFF,
	SANSAFFICHAGE, SANSAFFICHAGE, SANSAFFICHAGE,//Fleche de gauche(0x4B)
	0xFF, 0xFF, 0xFF,
	SANSAFFICHAGE, SANSAFFICHAGE, SANSAFFICHAGE,//Fleche de droite (0x4D)
	0xFF, 0xFF, 0xFF,
	SANSAFFICHAGE, SANSAFFICHAGE, SANSAFFICHAGE,//Touche 'fin' (0x4F)
	SANSAFFICHAGE, SANSAFFICHAGE, SANSAFFICHAGE,//Fleche du bas (0x50)
	SANSAFFICHAGE, SANSAFFICHAGE, SANSAFFICHAGE,//Fleche rapide vers le bas(0x51)
	SANSAFFICHAGE, SANSAFFICHAGE, SANSAFFICHAGE,//Insert(0x52)
	SANSAFFICHAGE, SANSAFFICHAGE, SANSAFFICHAGE,//Suppr(0x53)
	0xFF, 0xFF, 0xFF,
	0xFF, 0xFF, 0xFF,
	0xFF, 0xFF, 0xFF,
	'<', '>', SANSAFFICHAGE,//<> (0x56)
	SANSAFFICHAGE, SANSAFFICHAGE, SANSAFFICHAGE,
	SANSAFFICHAGE, SANSAFFICHAGE, SANSAFFICHAGE,
	SANSAFFICHAGE, SANSAFFICHAGE, SANSAFFICHAGE,
	SANSAFFICHAGE, SANSAFFICHAGE, SANSAFFICHAGE, //Windows (0x5B)
	SANSAFFICHAGE, SANSAFFICHAGE, SANSAFFICHAGE,
	SANSAFFICHAGE, SANSAFFICHAGE, SANSAFFICHAGE, //Menu (0x5D)
};

#endif
