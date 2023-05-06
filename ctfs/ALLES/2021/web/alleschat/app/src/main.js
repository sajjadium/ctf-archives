const { app, BrowserWindow, ipcMain, shell } = require("electron");
const path = require("path");
const fs = require("fs");

const createWindow = () => {
  const mainWindow = new BrowserWindow({
    width: 1000,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      sandbox: true,
    },
    icon: path.join(__dirname, "logo.png"),
  });

  mainWindow.webContents.session.on("will-download", downloader);
  mainWindow.webContents.on("will-navigate", openInBrowser);
  mainWindow.webContents.setWindowOpenHandler(() => {
    return { action: "deny" }; // nope. we only need one window
  });
  mainWindow.setMenuBarVisibility(false);
  mainWindow.loadFile(path.join(__dirname, "views/index.html"));

  writeLog("info", "Started application.");
};

app.on("ready", createWindow);

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});

app.on("activate", () => {
  if (BrowserWindow.getAllWindows().length === 0) createWindow();
});

app.on("before-quit", () => {
  writeLog("info", "Quitting Application.");
});

ipcMain.on("logging", (_e, level, msg) => {
  writeLog(level, msg);
});

ipcMain.on("notification", (_e, count) => {
  app.setBadgeCount(count);
});

const downloadDir = process.env.HOME + "/Downloads/";
const logFile = path.join(__dirname, "log.xml");

const openInBrowser = (e, url) => {
  // dont open our html files in the browser
  if (!/file:\/\/.+\.html/.test(url)) {
    e.preventDefault();
    shell.openExternal(url);
  }
};

const downloader = (_e, item) => {
  try {
    if (!fs.existsSync(downloadDir)) {
      fs.mkdirSync(downloadDir);
    }
    item.setSavePath(downloadDir + item.getFilename().replace(/\.\./g, ""));
  } catch (e) {
    console.log(e);
  }
};

const writeLog = (level, msg) => {
  let data;

  try {
    if (fs.existsSync(logFile)) {
      data = fs.readFileSync(logFile, "utf8").split("\n");
      data.splice(
        data.length - 1,
        0,
        `\t<${level}>[${new Date().toISOString()}] ${msg}</${level}>`
      );
    } else {
      data = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        "<logs>",
        `\t<${level}>[${new Date().toISOString()}] ${msg}</${level}>`,
        "</logs>",
      ];
    }
    fs.writeFileSync(logFile, data.join("\n"), {
      flag: "w",
    });
  } catch (e) {
    console.log(e);
  }
};

setInterval(() => {
  try {
    if (fs.existsSync(logFile)) {
      // TODO: send error log to server
      fs.writeFileSync(
        logFile,
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<logs>\n</logs>'
      );
    }
  } catch (e) {
    console.log(e);
  }
}, 150000);
