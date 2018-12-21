#include <stdio.h>
#include <string.h>
#include <windows.h>

int main (int argc, char * argv[])
{
	int i = 0 , hash = 0;

	printf("j0k3r's hash generateur par 0vercl0k.\n\n");
	if (argc !=2)
    {
        printf("Usage : %s <string>\n" , argv[0]);
        return 0;
    }

	for( ; i < strlen(argv[1]) ; i++ )
	    hash += (argv[1][i] << 0xD);

	printf("Hash de %s: %x\n",argv[1],hash);
}
