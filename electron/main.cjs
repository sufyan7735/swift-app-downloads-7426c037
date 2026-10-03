// نقطة تشغيل نسخة سطح المكتب (ويندوز): تشغّل خادم التطبيق محلياً داخل الجهاز
// ثم تفتح نافذة التطبيق عليه — بلا أي اعتماد على الإنترنت.
const { app, BrowserWindow, shell, Menu } = require("electron");
const path = require("node:path");
const net = require("node:net");

const isDev = !app.isPackaged;
const appRoot = isDev ? path.join(__dirname, "..") : process.resourcesPath;
const serverDir = path.join(appRoot, "dist-electron");

let win = null;
let port = 0;

function freePort() {
  return new Promise((resolve, reject) => {
    const srv = net.createServer();
    srv.once("error", reject);
    srv.listen(0, "127.0.0.1", () => {
      const p = srv.address().port;
      srv.close(() => resolve(p));
    });
  });
}

function waitForServer() {
  return new Promise((resolve, reject) => {
    const deadline = Date.now() + 30000;
    const tick = () => {
      const sock = net.connect(port, "127.0.0.1");
      sock.once("connect", () => {
        sock.destroy();
        resolve();
      });
      sock.once("error", () => {
        sock.destroy();
        if (Date.now() > deadline) reject(new Error("server timeout"));
        else setTimeout(tick, 250);
      });
    };
    tick();
  });
}

async function startServer() {
  port = await freePort();
  process.env.PORT = String(port);
  process.env.HOST = "127.0.0.1";
  process.env.NITRO_PORT = String(port);
  process.env.NITRO_HOST = "127.0.0.1";
  process.chdir(serverDir);
  await import(require("node:url").pathToFileURL(path.join(serverDir, "server", "index.mjs")).href);
  await waitForServer();
}

function createWindow() {
  win = new BrowserWindow({
    width: 1440,
    height: 900,
    minWidth: 1024,
    minHeight: 700,
    show: false,
    backgroundColor: "#0b1220",
    autoHideMenuBar: true,
    icon: path.join(appRoot, "build", "icon.png"),
    webPreferences: { contextIsolation: true, nodeIntegration: false },
  });
  win.once("ready-to-show", () => {
    win.show();
    win.maximize();
  });
  win.webContents.setWindowOpenHandler(({ url }) => {
    void shell.openExternal(url);
    return { action: "deny" };
  });
  void win.loadURL(`http://127.0.0.1:${port}/`);
}

Menu.setApplicationMenu(null);

app.whenReady().then(async () => {
  try {
    await startServer();
  } catch (err) {
    console.error("failed to start local server", err);
  }
  createWindow();
  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on("window-all-closed", () => {
  app.quit();
});
