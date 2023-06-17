<script>
function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
                
}
window.onhashchange = async ()=>{
    let code = atob(location.hash.slice(1));
    window.isDebug =  (await fetch("/api/debug.php").then((response)=>{
        return response.json();
    }).then((data)=>{
        return Number(data.isDebug);
    }));
    if(window.isDebug) {
        let result = eval(atob(location.hash.slice(1)));
        window.parent.postMessage({result: result, hacker: 0},"*");
    } else if(localStorage.getItem(code)) {
        let result = localStorage.getItem(code);
        window.parent.postMessage({result: result, hacker: 0},"*");
        localStorage.removeItem(code);
    } else {
        if(/!|@|#|\$|\^|&|_|;|\"|\'|\[|\]|\{|\}|[g-w]|[y-z]/.test(code)){
            alert("Are you hacker??");
            window.parent.postMessage({result: null, hacker: 1},"*");
            return;
        } else {
            let result = eval(atob(location.hash.slice(1)))
            localStorage.setItem(code, result);
            window.parent.postMessage({result: result, hacker: 0},"*");
        }
    }
}

</script>