@echo off
set name=decrypt_stub
goasm  /fo %name%.obj %name%.asm
golink  @link.txt
del *.obj
pause