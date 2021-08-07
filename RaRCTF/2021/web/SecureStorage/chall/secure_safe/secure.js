/* hey... what are you doing here??? 😡 */

console.log("secure js loaded...");

const z=(s,i,t=window,y='.')=>s.includes(y)?z(s.substring(s.indexOf(y)+1),i,t[s.split(y).shift()]):t[s]=i;

var user = "";
const render = () => {
    document.getElementById("user").innerText = user;
    document.getElementById("message").innerText = localStorage.message || "None set";
    document.getElementById("message").style.color = localStorage.color || "black";
};

window.onmessage = (e) => {
    let { origin, data } = e;
    if(origin !== document.getElementById("site").innerText || !Array.isArray(data)) return;
    z(...data.map(d => `${d}`));
    render();
};