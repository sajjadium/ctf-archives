self.addEventListener("push", event => {
    let gerald = event.data.json();
    self.registration.showNotification(`Your Gerald named "${gerald.name}" was viewed!`);
});