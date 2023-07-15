window.onload=()=> {
    var hasExtension = false;
    var extensionId="pifcfidoojbiodholilemccdnkcibghf"
    if(chrome.runtime == undefined){
        document.getElementById("msg").textContent="You have to install the Chrome extension to get the most of our web app"
        return
    }
    chrome.runtime.sendMessage(extensionId, { message: "hello" },
        function (answer) {
            if (answer) {
                if (answer.reply==="Konnichiwa") {
                        hasExtension = true;
                        console.log("Extension installed :-)")
                }
            }
            else {
              hasExtension = false;
            }
            console.log(hasExtension)
            if(!hasExtension){
                document.getElementById("msg").textContent="You have to install the Chrome extension to get the most of our web app"
            }
        
        });
        var url = new URL(location.href);
        var inp = url.searchParams.get("message");
        options={FORBID_TAGS:["meta"]}
        if(inp){
        document.getElementById("msg").innerHTML=DOMPurify.sanitize(inp,options)
}

    };

    