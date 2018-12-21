@echo off
set nasmw="C:\Program Files\nasm-0.98.38-win32\nasmw"
set pathsrc=C:\Hydropon-1K\sources
set pathbin=C:\Hydropon-1K\binaires
set pathgcc="C:\Program Files\CodeBlocks\MinGW\bin\"


%nasmw% "%pathsrc%\bootloader.asm" -f bin -o "%pathbin%\bootloader.com"
cd %pathgcc%
gcc.exe -Wall -Wextra -nostdlib -nostartfiles -nodefaultlibs -c "%pathsrc%\affichage.c" -o "%pathbin%\affichage.o"
gcc.exe -Wall -Wextra -nostdlib -nostartfiles -nodefaultlibs -c "%pathsrc%\noyau.c" -o "%pathbin%\noyau.o"
gcc.exe -Wall -Wextra -nostdlib -nostartfiles -nodefaultlibs -c "%pathsrc%\interruption.c" -o "%pathbin%\interruption.o"
gcc.exe -Wall -Wextra -nostdlib -nostartfiles -nodefaultlibs -c "%pathsrc%\memoire.c" -o "%pathbin%\memoire.o"
gcc.exe -Wall -Wextra -nostdlib -nostartfiles -nodefaultlibs -c "%pathsrc%\pagination.c" -o "%pathbin%\pagination.o"
gcc.exe -Wall -Wextra -nostdlib -nostartfiles -nodefaultlibs -c "%pathsrc%\commun.c" -o "%pathbin%\commun.o"
gcc.exe -Wall -Wextra -nostdlib -nostartfiles -nodefaultlibs -c "%pathsrc%\tache.c" -o "%pathbin%\tache.o"
gcc.exe -Wall -Wextra -nostdlib -nostartfiles -nodefaultlibs -c "%pathsrc%\tss.c" -o "%pathbin%\tss.o"
%nasmw% "%pathsrc%\routinesInterruptions.asm" -f win32 -o "%pathbin%\routinesInterruptions.o"
ld.exe -Ttext 0x1000 "%pathbin%\noyau.o" "%pathbin%\affichage.o" "%pathbin%\routinesInterruptions.o" "%pathbin%\interruption.o" "%pathbin%\memoire.o" "%pathbin%\pagination.o" "%pathbin%\commun.o" "%pathbin%\tache.o" "%pathbin%\tss.o" -o "%pathbin%\noyau.exe"
objcopy.exe -I pe-i386 -O binary "C:\Hydropon-1K\binaires\noyau.exe" "C:\Hydropon-1K\binaires\noyau.com"
cd "%pathbin%"
copy /b bootloader.com+noyau.com Hydropon-1K.com
del  bootloader.com noyau.com *.o noyau.exe
pause