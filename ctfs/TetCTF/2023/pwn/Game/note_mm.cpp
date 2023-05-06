#include <extdll.h>
#include <meta_api.h>

static META_FUNCTIONS gMetaFunctionTable = {
	.pfnGetEntityAPI = nullptr,
	.pfnGetEntityAPI_Post = nullptr,
	.pfnGetEntityAPI2 = GetEntityAPI2,
	.pfnGetEntityAPI2_Post = nullptr,
	.pfnGetNewDLLFunctions = nullptr,
	.pfnGetNewDLLFunctions_Post = nullptr,
	.pfnGetEngineFunctions = nullptr,
	.pfnGetEngineFunctions_Post = nullptr,
};

plugin_info_t Plugin_info = {
    .ifvers = META_INTERFACE_VERSION,
    .name = "Note",
    .version = "1.0",
    .date = __DATE__,
    .author = "nyancat0131",
    .url = "https://nyancat0131.moe",
    .logtag = "NOTE",
    .loadable = PT_STARTUP,
    .unloadable = PT_NEVER
};

meta_globals_t *gpMetaGlobals;
gamedll_funcs_t *gpGamedllFuncs;
mutil_funcs_t *gpMetaUtilFuncs;
enginefuncs_t g_engfuncs;
globalvars_t  *gpGlobals;

C_DLLEXPORT int Meta_Query(const char *interfaceVersion, plugin_info_t **plinfo, mutil_funcs_t *pMetaUtilFuncs) {
    *plinfo = &Plugin_info;
    gpMetaUtilFuncs = pMetaUtilFuncs;

    return 1;
}

C_DLLEXPORT int Meta_Attach(PLUG_LOADTIME now, META_FUNCTIONS *pFunctionTable, meta_globals_t *pMGlobals, gamedll_funcs_t *pGamedllFuncs) {
    gpMetaGlobals = pMGlobals;
    gpGamedllFuncs = pGamedllFuncs;
    *pFunctionTable = gMetaFunctionTable;

    return 1;
}

C_DLLEXPORT int Meta_Detach(PLUG_LOADTIME now, PL_UNLOAD_REASON reason) {
    return 1;
}

static int ConnectionlessPacket(const struct netadr_s *net_from, const char *args, char *response_buffer, int *response_buffer_size) {
    edict_t *ent = ENT(atoi(++args));
    strcpy(response_buffer, STRING(ent->v.classname));
    *response_buffer_size = strlen(response_buffer);

    RETURN_META_VALUE(MRES_SUPERCEDE, 1);
}

C_DLLEXPORT int GetEntityAPI2(DLL_FUNCTIONS *pFunctionTable, int *interfaceVersion) {
	if (*interfaceVersion != INTERFACE_VERSION) {
		*interfaceVersion = INTERFACE_VERSION;
		return 0;
	}
	
    memset(pFunctionTable, 0, sizeof(*pFunctionTable));
    pFunctionTable->pfnConnectionlessPacket = ConnectionlessPacket;

	return 1;
}

C_DLLEXPORT void WINAPI GiveFnptrsToDll(enginefuncs_t* pengfuncsFromEngine, globalvars_t *pGlobals) {
	memcpy(&g_engfuncs, pengfuncsFromEngine, sizeof(enginefuncs_t));
	gpGlobals = pGlobals;
}

// Avoid linking to libstdc++
#if defined(linux)
extern "C" void __cxa_pure_virtual(void) {
}

void *operator new(size_t size) {
	return malloc(size);
}

void *operator new[](size_t size) {
	return malloc(size);
}

void operator delete(void *ptr) {
	free(ptr);
}

void operator delete[](void * ptr) {
	free(ptr);
}
#endif
