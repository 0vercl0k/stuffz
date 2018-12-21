#include "classDebug.hpp"
#include "classExcptDbg.hpp"
#define BP   0x00461010 //00461010    FFE0            JMP EAX

int main()
{
    PUCHAR pDump;
    DWORD sizeBin = 0;

    try
    {
        DebugUrProcess dbg("UnpackMe.exe");
        dbg.goTo(BP, DebugUrProcess::HardwareBreakpoint);
        dbg.writeDump(dbg.dump(&sizeBin, dbg.getRegister("eax")-dbg.getImageBase()), sizeBin);
    }
    catch(ExcptDbg & a)
    {
        std::cerr << a.what() << " -> " << DebugUrProcess::errorDescription(a.getErrorNumber()) << std::endl;
        return 0;
    }

    return 1;
}
