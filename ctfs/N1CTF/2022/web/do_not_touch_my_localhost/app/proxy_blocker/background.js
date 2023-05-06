function checkPermission(){
  return new Promise((resolve, reject) => {
    chrome.permissions.contains(
      {
        permissions: ["proxy"],
      },
      function (result) {
        resolve(result);
      }
    );
  });
}

function resetProxy() {
  console.log('reset proxy');
  chrome.proxy.settings.set({ value: { mode: "direct" }, scope: "regular" });
}

function setProxy(options) {
  const config = {
    mode: "fixed_servers",
    rules: {
      singleProxy: options,
    },
  };
  try{
    console.log(options)
    chrome.proxy.settings.set({ value: config, scope: "regular" });
  }catch{}
}

function getProxyPromise() {
  return new Promise((resolve, reject) => {
    chrome.proxy.settings.get({ incognito: false }, function (config) {
      resolve(config);
    });
  });
}

chrome.runtime.onMessage.addListener(async function (
  request,
  sender,
  sendResponse
) {
  if (request.type == "setProxy") {
    setProxy(request.options);
    sendResponse({});
  } else if (request.type == "resetProxy") {
    resetProxy();
    sendResponse({});
  } else if (request.type == "getProxy") {
    let config = await getProxyPromise();
    sendResponse(config);
  }
});

chrome.runtime.onStartup.addListener(async function () {
  if(await checkPermission()){
    resetProxy()
  }
});
