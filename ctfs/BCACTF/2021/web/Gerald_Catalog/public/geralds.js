window.addEventListener("load", _ => {
    document.querySelectorAll(".notification-control").forEach(control => {
        control.addEventListener("change", async _e => {
            control.disabled = true;
            if (!control.checked) {
                await fetch(`/gerald/${control.id}/subscription`, { method: "DELETE" });
            }
            try {
                const reg = await navigator.serviceWorker.ready;
                const subscription = await reg.pushManager.subscribe({
                    applicationServerKey: "BPNgtDf_KDozpPch8_EATRRMArftSDxouZ2TI16Gf4Y8dkEf4Gv0E6KO29HijlWPaTNsq4W6XA7n3pxzgLGSWVk",
                    userVisibleOnly: true
                });
                if (control.checked) {
                    if (await Notification.requestPermission() !== "granted") throw new Error("permission denied");
                    await fetch(`/gerald/${control.id}/subscription`, {
                        method: "PUT",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify(subscription.toJSON())
                    });
                } else {
                    await subscription.unsubscribe();
                }
            } catch (e) {
                control.checked = false;
                console.error(e);
                alert("An error occurred. Ensure you are using Firefox, Chrome, Edge, or Opera and that this site has permission to send notifications.");
            }
            control.disabled = false;
        });
    });

    navigator.serviceWorker.register("/sw.js").then(registration => {
        console.log("Service worker registered! Scope: " + registration.scope);
    }).catch(err => {
        console.error(err);
        alert("Could not register a service worker. Check the console for more information.")
    });
});