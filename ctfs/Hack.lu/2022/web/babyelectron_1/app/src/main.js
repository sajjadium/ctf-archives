// Modules to control application life and create native browser window
const {app, BrowserWindow, ipcMain, session} = require('electron')
const path = require('path')

function createWindow (session) {
  // Create the browser window.
  const mainWindow = new BrowserWindow({
    title: "Real Estate Luxembourg",
    width: 860,
    height: 600,
    minWidth: 860,
    minHeight: 600,
    resizable: false,
    icon: '/images/fav.ico',
    webPreferences: {
      preload: path.join(app.getAppPath(), "./src/preload.js"), // eng-disable PRELOAD_JS_CHECK
      // SECURITY: use a custom session without a cache
      // https://github.com/1password/electron-secure-defaults/#disable-session-cache
      session,
      // SECURITY: disable node integration for remote content
      // https://github.com/1password/electron-secure-defaults/#rule-2
      nodeIntegration: false,
      // SECURITY: enable context isolation for remote content
      // https://github.com/1password/electron-secure-defaults/#rule-3
      contextIsolation: true,
      // SECURITY: disable the remote module
      // https://github.com/1password/electron-secure-defaults/#remote-module
      enableRemoteModule: false,
      // SECURITY: sanitize JS values that cross the contextBridge
      // https://github.com/1password/electron-secure-defaults/#rule-3
      worldSafeExecuteJavaScript: true,
      // SECURITY: restrict dev tools access in the packaged app
      // https://github.com/1password/electron-secure-defaults/#restrict-dev-tools
      devTools: !app.isPackaged,
      // SECURITY: disable navigation via middle-click
      // https://github.com/1password/electron-secure-defaults/#disable-new-window
      disableBlinkFeatures: "Auxclick",
      // SECURITY: sandbox renderer content
      // https://github.com/1password/electron-secure-defaults/#sandbox
      sandbox: true,

    }
  })
  mainWindow.setMenuBarVisibility(false)
  // and load the ~~index.html~~ login of the app.
  mainWindow.loadFile(path.join(app.getAppPath(), process.env.BOT ? "src/views/support.html" : "src/views/login.html"));

  // Open the DevTools.
  // mainWindow.webContents.openDevTools()
}


// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on("ready", () => {
  // SECURITY: use a custom persistent session without a cache
  // https://github.com/1password/electron-secure-defaults/#disable-session-cache
  const secureSession = session.fromPartition("persist:app", {
    cache: false,
  });

  createWindow(secureSession);

  app.on("activate", function () {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (BrowserWindow.getAllWindows().length === 0) createWindow(secureSession);
  });

  // SECURITY: deny permission requests from renderer
  // https://github.com/1password/electron-secure-defaults/#rule-4
  secureSession.setPermissionRequestHandler(
    (_webContents, _permission, callback) => {
      callback(false);
    }
  );

  // SECURITY: define a strict CSP
  // https://github.com/1password/electron-secure-defaults/#rule-6
  secureSession.webRequest.onHeadersReceived((details, callback) => {
    callback({
      responseHeaders: /* eng-disable CSP_GLOBAL_CHECK */ {
        ...details.responseHeaders,
        "Content-Security-Policy": ["default-src: 'self'; object-src: 'none'; style-src: 'inline'"],
      },
    });
  });
});



// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit()
})

app.on("web-contents-created", (_ev, contents) => {
  // SECURITY: verify webview options before creation
  // https://github.com/1password/electron-secure-defaults/#rule-11
  const preventDefault = (ev) => {
    ev.preventDefault();
  };
  contents.on("will-attach-webview", preventDefault);

  // SECURITY: disable or limit navigation
  // https://github.com/1password/electron-secure-defaults/#rule-12
  contents.on("will-navigate", () => {}); // eng-disable LIMIT_NAVIGATION_GLOBAL_CHECK

  // SECURITY: disable or limit creation of new windows
  // https://github.com/1password/electron-secure-defaults/#rule-13
  contents.on("new-window", preventDefault); // eng-disable LIMIT_NAVIGATION_GLOBAL_CHECK

  // SECURITY: further prevent new window creation
  // https://github.com/1password/electron-secure-defaults/#prevent-new-window
  contents.setWindowOpenHandler(() => {
    return { action: "deny" };
  });
});





// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.

app.RELbuy = function(listingId){
  return
}

app.RELsell = function(houseId, price, duration){
  return
}

app.RELinfo = function(houseId){
  return
}

app.RElist = function(listingId){
  return
}

app.RELsummary = function(userId){
 return 
}

ipcMain.on("RELaction", (_e, action, args)=>{
  //if(["RELbuy", "RELsell", "RELinfo"].includes(action)){
  if(/^REL/i.test(action)){
    app[action](...args)  
  }else{
    // ?? 
  }
})