import ExtendedMath from "./extendedMath.js"
function mathEval(code) {
    return new Promise((resolve, reject) => {
        try {
            const f = Function("return " + code)
            resolve(f.apply({ Math: (new ExtendedMath()).newMath }))
        } catch (error) {
            reject(error)
        }
    })

}
self.onmessage = (ev) => {
    mathEval(ev.data)
        .then(message => self.postMessage({ message }))
        .catch(error => self.postMessage({ error }))
}
