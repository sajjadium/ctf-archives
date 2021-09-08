#include <sourcemod>
#include <sdktools>
native void call(char[] url, int length);
forward void OnDownloaded(const char[] sFile);
forward void notify(const char[] msg);

public Plugin:info = {
    name = "SQ",
    author = "localo",
    description = "Download and execute squirrel scripts",
    url = ""
};

public void OnPluginStart() {
    RegConsoleCmd("sm_sq", OnCommand);
}


public Action OnCommand(int client, int args) {
    if (args != 1) {
        ReplyToCommand(client, "Usage: sq <URL>");
        return Plugin_Handled;
    }

    char url[256];
    GetCmdArg(1, url, sizeof(url));
	call(url,sizeof(url));
    return Plugin_Handled;
}

public void notify(const char[] msg){
    for (int i = 1; i <= MaxClients; i++)
    {
        if (!IsClientInGame(i))
            continue;
        PrintToChat(i, msg);
    } 
}

public void OnDownloaded(const char[] sFile){
  int entity = CreateEntityByName("logic_script");
  if( entity != -1 )
  {
    DispatchSpawn(entity);
    SetVariantString(sFile);
    AcceptEntityInput(entity, "RunScriptFile");
    RemoveEdict(entity);
  }
}