/**
 * \file classDebug.hpp
 * \author 0vercl0k
 */

#ifndef CLASS_DEBUG
#define CLASS_DEBUG

#include <windows.h>
#include <string>
#include <iostream>


class DebugUrProcess
{
    private:
        std::string m_ProcessName;
        PROCESS_INFORMATION m_iProcess;
        STARTUPINFOA m_iStartup;
        DEBUG_EVENT m_DbgEvent;
        DWORD m_imgBase, m_ep;
        IMAGE_DOS_HEADER m_imgDos;
        IMAGE_NT_HEADERS m_imgPe;

        /**
         * \fn void goToI3(const DWORD addr)
         * \brief Permet de poser un breakpoint-logiciel � une adresse addr et d'ex�cuter le debugge jusqu'� celle-ci.
         * \param addr Adresse absolue (imgBase+offset) du breakpoint
         */
        void goToI3(DWORD addr);

        /**
         * \fn void goToHW(const DWORD addr)
         * \brief Permet de poser un breakpoint-mat�riel � une adresse addr et d'ex�cuter le debugge jusqu'� celle-ci.
         * \param addr Adresse absolue (imgBase+offset) du breakpoint
         */
        void goToHW(DWORD addr);

        /**
         * \fn void getDosAndPeHeaders(void);
         * \brief R�cup�re et stock les en-t�tes DOS et PE
         */
        void getDosAndPeHeaders(void);

    public:
        enum BreakpointType
        {
            HardwareBreakpoint,
            SoftwareBreakpoint
        };

        /**
         * \fn DebugUrProcess(const std::string& processName, const std::string & directory = "")
         * \brief Constructeur de la classe, ex�cute le binaire jusqu'� son point d'entr�e.
         * \param processName Nom du binaire � debug
         * \param directory Dossier qui contient le binaire
         */
        DebugUrProcess(const std::string& processName, const std::string & directory = "");
       ~DebugUrProcess();

        /**
         * \fn static std::string errorDescription(const DWORD num)
         * \brief M�thode permettant de r�cuperer des informations sur une erreur survenue dans le programme.
         * \param num Num�ro de l'erreur
         * \return Texte descriptif de l'erreur en question
         */
        static std::string errorDescription(DWORD num);

        /**
         * \fn template <typename T> static std::string toString(const T& obj)
         * \brief Permet la conversion d'un type T en une chaine de caract�re.
         * \param obj Instance de l'objet � convertir
         * \return Chaine de caract�re correspondant � l'objet
         */
        template <typename T> static std::string toString(const T& obj);

        /**
         * \fn void goTo(const DWORD addr, BreakpointType bp = SoftwareBreakpoint)
         * \brief M�thode qui pose un breakpoint de type bp � l'adresse addr, et ex�cute le debugg� jusqu'� cette adresse.
         * \param addr Adresse absolue (imgBase+offset)
         * \param bp Type du breakpoint qui va �tre poser
         */
        void goTo(DWORD addr, BreakpointType bp = SoftwareBreakpoint);

        /**
         * \fn PUCHAR dump(PULONG pSize, const DWORD oep = 0)
         * \brief Fonction qui va cr�er un dump de l'ex�cutable en m�moire.
         * \param pSize Pointeur sur une variable qui contiendra la taille du dump
         * \param oep Param�tre permettant de sp�cifier un changement de point-d'entr�e
         * \return Pointeur sur le dump m�moire
         */
        PUCHAR dump(PULONG pSize, DWORD oep = 0);

        /**
         * \fn void writeDump(const PUCHAR pDump, ULONG sizeDmp, const std::string & filename = "")
         * \brief Permet d'�crire un dump m�moire dans un fichier en dur.
         * \param pDump Pointeur sur le dump m�moire qui va �tre �crit dans le fichier
         * \param sizeDmp Taille du dump m�moire en octet
         * \param filename Nom du fichier qui va �tre cr�er
         */
        void writeDump(const PUCHAR pDump, ULONG sizeDmp, const std::string & filename = "");

        DWORD getRegister(const std::string & reg) const;
        DWORD getImageBase(void) const;
};

#endif
