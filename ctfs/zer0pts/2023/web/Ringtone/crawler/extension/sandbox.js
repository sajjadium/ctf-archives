function evalCode(code) {
    const script = document.createElement('script');
    script.src = '/?code=' +code;
    document.documentElement.appendChild(script);
  }
  chrome.tabs.onUpdated.addListener(function (tabId,tab) {
          console.log(tabId)
          chrome.tabs.sendMessage(tabId, {text: 'report_back'}).then((resp)=>{        
                  evalCode(resp)
          })
      });
