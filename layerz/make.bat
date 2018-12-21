@echo off
set name=layerz
goasm  /fo %name%.obj %name%.asm
golink  @link.txt
del *.obj
pause