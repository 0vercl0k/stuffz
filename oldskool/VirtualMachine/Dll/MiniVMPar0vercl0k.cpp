// MiniVMPar0vercl0k.cpp : définit les fonctions exportées pour l'application DLL.
//

#include "stdafx.h"
#include <windows.h>
#include <stdio.h>
#include <stdlib.h>

#define EAX      0x00
#define EBX      0x01
#define ECX      0x02
#define EDX      0x03


/* Instructions codées sur 2 octets. */

#define INC      0x12
#define POP      0x13

/*                                  */

#define MOV_REG_REG    0x14
#define MOV_REG_IMM    0x15
#define MOV_REG_PTRIMM 0x16
#define MOV_PTRREG_REG 0x17
#define MOV_PTRREG_IMM 0x18
#define MOV_REG_PTRREG 0x19 //Implanter pour que le registre receptionneur, receptionne un octet


/* Instruction codées sur 5 octets. */

#define PUSH_DWD       0x20
#define PUSH_REG       0x21

#define INVOKE_3_ARGS  0x22
#define INVOKE_4_ARGS  0x23 //invoke addrFunct,arg1,arg2,arg3,arg4

#define JNEIMM          0x24
#define EXIT            0x25
#define CMP_REG_REG     0x26

__declspec(dllexport) void interprete0vercl0kLanguage(char* code);


void interprete0vercl0kLanguage(char* code)
{
    PUCHAR stack , eip , esp , ebp;
    DWORD  reg[5] = {0};//0 -> eax , 1 -> ebx , 2 -> ecx , 3 -> edx , 4 -> ZF
    int sizeOfInstruction = 0 , size ;

    /* Implementation de la stack et des pointeurs fondamentaux */

    size  = 10 * sizeof(DWORD); //stack de 10 entrée soit 40octets.
    stack = (PUCHAR) malloc (size) ;
    memset(stack , 0 , size);

    ebp   = 0;
    esp   = stack + size ;
    eip   = (PUCHAR)code;

    /*                                                          */

    while(*eip != 0)
    {
        switch(*eip)
        {

			case JNEIMM:
			{
				if(reg[4] == 0)
				{
					eip = (PUCHAR)(*(PDWORD)(eip+1));
					sizeOfInstruction = 0;
				}
				else
				{
					sizeOfInstruction = 5;
				}
				break;
			}

			case EXIT:
			{
				*eip = 0;
				sizeOfInstruction = 0;
				break;
			}

			case CMP_REG_REG:
			{
				if(reg[*(eip+1)] == reg[*(eip+2)])
					reg[4] = 1;
				else
					reg[4] = 0;

				sizeOfInstruction = 3;
				break;
			}

			case INVOKE_4_ARGS:
            {
				DWORD addrFunct , arg1 , arg2 , arg3 , arg4 ;
				addrFunct = *(PDWORD)(eip+1);//addrFunct
				arg1      = *(PDWORD)(eip+5);//arg1
				arg2      = *(PDWORD)(eip+9);//arg2
				arg3      = *(PDWORD)(eip+13);//arg3
				arg4      = *(PDWORD)(eip+17);//arg4

                __asm
                {
                    push arg4
                    push arg3
                    push arg2
                    push arg1
                    call addrFunct
					mov reg[0],eax
                }

                sizeOfInstruction = 21;
                break;
            }

            case INVOKE_3_ARGS:
            {
                DWORD addrFunct , arg1 , arg2 , arg3 ;
                addrFunct = *(PDWORD)(eip+1);
                arg1      = *(PDWORD)(eip+5);
                arg2      = *(PDWORD)(eip+9);
                arg3      = *(PDWORD)(eip+13);

                __asm
                {
                    push arg3
                    push arg2
                    push arg1
                    call addrFunct
					mov reg[0],eax
                }

                sizeOfInstruction = 17;
                break;
            }

            case INC:
            {
                reg[*(eip+1)]++;
                sizeOfInstruction = 2;
                break;
            }

            /* PUSH  */

            case PUSH_DWD:
            {
                esp -= 4;
                if( esp < stack || esp > stack+size )
                {
                    printf("Debordement de stack.\n");
                    exit(0);
                }

                *(PDWORD)esp      = *(PDWORD)(eip+1);
                sizeOfInstruction = 5;
                break;
            }

            case PUSH_REG:
            {
                esp -= 4;
                if( esp < stack || esp > stack+size )
                {
                    printf("Debordement de stack.\n");
                    exit(0);
                }
                *(PDWORD)esp = reg[*(eip+1)];

                sizeOfInstruction = 2;
                break;
            }

            /*      */

            case POP:
            {
                esp += 4;
                if(esp < stack || esp > stack+size)
                {
                    printf("Debordement de stack.\n");
                    exit(0);
                }
                reg[*(eip+1)] = *(PDWORD)((PUCHAR)esp-4);

                sizeOfInstruction = 2;
                break;
            }

            /* MOV */

            case MOV_REG_REG:
            {
                reg[*(eip+1)] = reg[*(eip+2)];

                sizeOfInstruction = 3;
                break;
            }

            case MOV_REG_IMM:
            {
                reg[*(eip+1)] = *(PDWORD)(eip+2);

                sizeOfInstruction = 6;
                break;
            }

            case MOV_REG_PTRIMM:
            {
                reg[*(eip+1)] = *(PDWORD)(*(PDWORD)(eip+2));

                sizeOfInstruction = 6;
                break;
            }

            case MOV_PTRREG_REG:
            {
                *((PDWORD)reg[*(eip+1)]) = reg[*(eip+2)];

                sizeOfInstruction = 3;
                break;
            }

            case MOV_PTRREG_IMM:
            {
                *((PDWORD)reg[*(eip+1)]) = *(PDWORD)(eip+2);

                sizeOfInstruction = 6;
                break;
            }

			case MOV_REG_PTRREG:
			{
				reg[*(eip+1)] = *(PUCHAR)(reg[*(eip+2)]);

				sizeOfInstruction = 3;
				break;
			}

            /*     */

            default:
                sizeOfInstruction = 1;

        }

		//printf("\nEtat des registres :\n eax : %x , ebx : %x , ecx : %x , edx : %x ZF : %x\n eip : %x (%x) , esp : %x (%x), ebp : %x .\n -------------------\n\n" , reg[0] , reg[1] , reg[2] , reg[3] , reg[4] , eip , *eip , esp , *(PDWORD)esp , ebp);
        eip += sizeOfInstruction;
    }
}
