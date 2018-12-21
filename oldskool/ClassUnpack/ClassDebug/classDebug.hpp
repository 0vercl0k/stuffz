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
         * \brief Permet de poser un breakpoint-logiciel à une adresse addr et d'exécuter le debugge jusqu'à celle-ci.
         * \param addr Adresse absolue (imgBase+offset) du breakpoint
         */
        void goToI3(DWORD addr);

        /**
         * \fn void goToHW(const DWORD addr)
         * \brief Permet de poser un breakpoint-matériel à une adresse addr et d'exécuter le debugge jusqu'à celle-ci.
         * \param addr Adresse absolue (imgBase+offset) du breakpoint
         */
        void goToHW(DWORD addr);

        /**
         * \fn void getDosAndPeHeaders(void);
         * \brief Récupère et stock les en-têtes DOS et PE
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
         * \brief Constructeur de la classe, exécute le binaire jusqu'à son point d'entrée.
         * \param processName Nom du binaire à debug
         * \param directory Dossier qui contient le binaire
         */
        DebugUrProcess(const std::string& processName, const std::string & directory = "");
       ~DebugUrProcess();

        /**
         * \fn static std::string errorDescription(const DWORD num)
         * \brief Méthode permettant de récuperer des informations sur une erreur survenue dans le programme.
         * \param num Numéro de l'erreur
         * \return Texte descriptif de l'erreur en question
         */
        static std::string errorDescription(DWORD num);

        /**
         * \fn template <typename T> static std::string toString(const T& obj)
         * \brief Permet la conversion d'un type T en une chaine de caractère.
         * \param obj Instance de l'objet à convertir
         * \return Chaine de caractère correspondant à l'objet
         */
        template <typename T> static std::string toString(const T& obj);

        /**
         * \fn void goTo(const DWORD addr, BreakpointType bp = SoftwareBreakpoint)
         * \brief Méthode qui pose un breakpoint de type bp à l'adresse addr, et exécute le debuggé jusqu'à cette adresse.
         * \param addr Adresse absolue (imgBase+offset)
         * \param bp Type du breakpoint qui va être poser
         */
        void goTo(DWORD addr, BreakpointType bp = SoftwareBreakpoint);

        /**
         * \fn PUCHAR dump(PULONG pSize, const DWORD oep = 0)
         * \brief Fonction qui va créer un dump de l'exécutable en mémoire.
         * \param pSize Pointeur sur une variable qui contiendra la taille du dump
         * \param oep Paramètre permettant de spécifier un changement de point-d'entrée
         * \return Pointeur sur le dump mémoire
         */
        PUCHAR dump(PULONG pSize, DWORD oep = 0);

        /**
         * \fn void writeDump(const PUCHAR pDump, ULONG sizeDmp, const std::string & filename = "")
         * \brief Permet d'écrire un dump mémoire dans un fichier en dur.
         * \param pDump Pointeur sur le dump mémoire qui va être écrit dans le fichier
         * \param sizeDmp Taille du dump mémoire en octet
         * \param filename Nom du fichier qui va être créer
         */
        void writeDump(const PUCHAR pDump, ULONG sizeDmp, const std::string & filename = "");

        DWORD getRegister(const std::string & reg) const;
        DWORD getImageBase(void) const;
};

#endif
