onmessage = (e) => {
    const { platesToIgnore } = e.data
    postMessage(generatePlatePossibilitySpace(platesToIgnore))
}

function generatePlatePossibilitySpace (platesToIgnore) {
    const arr = Array.from({ length: 10 ** 3 * 26 ** 3 }, (_, i) => i)
    for (let i = 0; i < platesToIgnore.length; i++) {
        arr[platesToIgnore[i]] = -1
    }
    return arr.filter((x) => x !== -1)
}
