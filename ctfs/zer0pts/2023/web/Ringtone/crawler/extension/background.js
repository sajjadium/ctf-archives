chrome.runtime.onMessageExternal.addListener(
        function(request, sender, sendResponse) {
            if (request) {
                if (request.message) {
                    if (request.message == "hello") {
                        sendResponse({reply: "Konnichiwa"});
                    }
                }
            }
            return true;
        });
const sleep = ms => new Promise(r => setTimeout(r, ms));
    
chrome.runtime.onMessage.addListener(
        function(request, sender, sendResponse) {
                if(request.play=="play"){
                        chrome.tabs.create({url:"audio.html"},async (tab)=>{
                                await sleep(5000);
                                chrome.tabs.remove(tab.id)
                        })
                        sendResponse({text:"played successfully"})
                }
        }
)
const prefix = location.origin + '/?code=';
self.onfetch= e => {
  if (e.clientId && e.request.url.startsWith(prefix)) {
    e.respondWith(new Response(e.request.url.slice(prefix.length), {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8' },
    }));
  }
};




