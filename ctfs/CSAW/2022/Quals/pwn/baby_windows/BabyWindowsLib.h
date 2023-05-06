
#ifdef CSAW_EXPORTS
#define CSAWAPI __declspec(dllexport)
#else
#define CSAWAPI __declspec(dllimport)
#endif

CSAWAPI void PrintCSAWBanner();
CSAWAPI void PrintOS();
CSAWAPI void Pontificate();
CSAWAPI void Pwn();