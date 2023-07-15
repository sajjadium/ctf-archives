var form=document.getElementById("ring-form");
form.addEventListener("submit",
async (evt)=>{
    evt.preventDefault();
    var val=form.elements["message"].value;
    console.log(val)
    const response = await chrome.runtime.sendMessage({play:"play"})
    if(response.text=="played successfully"){
        console.log("yattaa")
    }
}
)

chrome.runtime.onMessage.addListener(function (msg, sender, sendResponse) {
    if (msg.text === 'report_back') {
        console.log("msg received")
        if(users.privileged.dataset.admin){
            sendResponse(users.privileged.dataset.admin)
        }
    }
});
