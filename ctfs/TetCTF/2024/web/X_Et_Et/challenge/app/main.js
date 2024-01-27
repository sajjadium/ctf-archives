// Modules to control application life and create native browser window
const {
  session,
  app,
  BrowserWindow,
  ipcMain,
  screen,
  shell
} = require('electron')
const path = require('path')
let notificationWindow = null;
let mainWindow = null;

function createWindow() {
  // Create the browser window.
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      sandbox: false,
      contextIsolation: true,
      nodeIntegration: false,
      webgl: true,
      webSecurity: false,
      nodeIntegrationInSubFrames: true,
      
    }
  })

 
  
  mainWindow.loadFile("index.html")
 
}

ipcMain.on('Calculator', (event,num1,num2) => {
  
  return eval(`${num1}+${num2}`)
})
function createNotificationWindow(id) {
  
  child = new BrowserWindow({
    width: 300,
    height: 200,
    webPreferences: {
      //preload: no need preload expose
      sandbox: false,
      contextIsolation: false,
      webgl: true,
      webSecurity: false,
      nodeIntegrationInSubFrames: false, // dont allow call ipc from iframe/child windows
    }
  })

  
  child.loadURL("http://localhost/IsNew?id="+id)
 
}

ipcMain.on('OpenUrlIpc', (event, url) => {
  const { shell } = require('electron');
  shell.openExternal(url)
})

ipcMain.on('CreateViewer', (event,id) => {
  createNotificationWindow(id);
})

// IPC handler in the main window





app.whenReady().then(() => {
  
  createWindow();
  

  app.on('activate', function () {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (BrowserWindow.getAllWindows().length === 0) createWindow()

    
  })
})

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit()
})