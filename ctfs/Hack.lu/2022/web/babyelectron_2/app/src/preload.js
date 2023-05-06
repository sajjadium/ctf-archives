const {ipcRenderer, contextBridge} = require('electron')

const API_URL = process.env.API_URL || "https://relapi.flu.xxx";
localStorage.setItem("api", API_URL)

const REPORT_ID = process.env.REPORT_ID || "fail"
localStorage.setItem("reportId", REPORT_ID) 

const RendererApi = {
  invoke: (action, ...args)  => {
      return ipcRenderer.send("RELaction",action, args);
  },
};

// SECURITY: expose a limted API to the renderer over the context bridge
// https://github.com/1password/electron-secure-defaults/SECURITY.md#rule-3
contextBridge.exposeInMainWorld("api", RendererApi);
