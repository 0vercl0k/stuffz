# -*- coding:Latin-1 -*-

import sys
import pefile
import os

macro = """
#define JMP( lib, func )            \\
   __asm                            \\
   (   "pushad                \\n"   \\
       " push edx             \\n"   \\
       " push %1              \\n"   \\
       " call eax             \\n"   \\
       " pop edx              \\n"   \\
       " push %2              \\n"   \\
       " push eax             \\n"   \\
       " call edx             \\n"   \\
       " mov %4, eax          \\n"   \\
       " popad                \\n"   \\
                                    \\
       : :                          \\
       "a" (GetModuleHandle) ,      \\
       "g" (lib)             ,      \\
       "g" (func)            ,      \\
       "d" (GetProcAddress)  ,      \\
       "g" (tmp)                    \\
    );                              \\
   asm ( "jmp %0" : : "g" (tmp) );
   """

templateFunct = """
DLLEXPORT void _%s(void)
{
	JMP(FAKE_LIB, %d);
}
"""

path = 'C:\\WINDOWS\\System32\\'
pathOut = 'C:\\'

class generateDll :
	'Genere un code C d\'une dll x, ayant les m�mes importations que la dll y.'
	def __init__(self, nomDll, nomFichierSortie, cheminBase = path, cheminBaseSortie = pathOut):
		self.nameDll = nomDll
		self.pathDllIn = cheminBase + nomDll
		self.pathFileOut = cheminBaseSortie + nomFichierSortie
		self.functs = []
		self.macro = macro
		self.templateFunct = templateFunct
	
	def parseEAT(self):
		try:
			pe = pefile.PE(self.pathDllIn)
		except:
			print '\t[!] Impossible d\'ouvrir votre fichier.\n'
			return []
		for export in pe.DIRECTORY_ENTRY_EXPORT.symbols:				
			self.functs.append([export.name, export.ordinal])
		return self.functs

	def serialise(self):
		if len(self.functs) == 0:
			return 0
		
		fakeDll = self.nameDll.replace('.dll', '') + '_.dll'
		
		hFileDef = open(self.pathFileOut.replace('.c', '.def'), 'a')
		hFile = open(self.pathFileOut, 'a')
		
		hFileDef.write('LIBRARY %s\nEXPORTS\n\n' % (self.nameDll.replace('.dll', '')))
		
		hFile.write('#include <windows.h>\n#define DLLEXPORT __declspec (dllexport)\n#define FAKE_LIB "%s"\nunsigned long tmp;\n' % fakeDll)
		hFile.write(self.macro)
		for funct in self.functs:
			hFile.write(self.templateFunct % (funct[0], funct[1]))
			hFileDef.write('%s=_%s @ %d\n' % (funct[0], funct[0], funct[1]))
		hFile.close()
		return 1
		
#Main
if len(sys.argv) != 2:
	print 'Usage : %s <binaireEntree>' % sys.argv[0]
	sys.exit(0)

print 'Ouverture de \'%s\' ..' % (path+sys.argv[1])
fileOut = sys.argv[1].replace('.dll', '') + '_.c'

a = generateDll(sys.argv[1], fileOut)
functions = a.parseEAT()

if len(functions) != 0:
	print '%d Exportations r�cup�r�es.\nCr�ation du fichier de sortie..' % len(functions)
	if a.serialise() == 1:
		print '%s cr�� avec succ�s.' % (pathOut + fileOut)
		print '%s cr�� avec succ�s.' % (pathOut + fileOut.replace('.c', '.def'))
	else:
		print 'Probl�me lors de la g�n�ration du fichier.'
		sys.exit(0)
else:
	print 'Aucune exportation r�cup�r�e.'