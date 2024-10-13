export function f(code) {
    return new Promise((resolve, reject) => {
        const worker = new Worker(new URL("./worker.js", import.meta.url).href, {
            type: "module",
            deno: {
                permissions: {
                    read: true
                }
            }
        });
        worker.onmessage = (ev) => {
            if (ev.data.message){
                resolve(ev.data.message)
            }else {
                reject(ev.data.error)
            }
        }
        worker.postMessage(code)
    })
}
