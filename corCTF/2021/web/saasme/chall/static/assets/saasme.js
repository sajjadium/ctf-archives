let $ = document.querySelector.bind(document);

$("#curlbtn").addEventListener("click", async () => {
    $("#output").innerText = 'Loading...';

    let url = $("#curl").value;

    let resp = await (await fetch("/curl", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ url })
    })).text();

    $("#output").innerText = resp;
});

$("#chromiumbtn").addEventListener("click", async () => {
    $("#output").innerText = 'Loading...';
    
    let url = $("#chromium").value;

    let resp = await (await fetch("/chrome", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ url })
    })).text();

    $("#output").innerText = resp;
});

$("#killbtn").addEventListener("click", async () => {
    $("#output").innerText = 'Loading...';

    let resp = await (await fetch("/kill", {
        method: "POST",
    })).text();

    $("#output").innerText = resp;
});