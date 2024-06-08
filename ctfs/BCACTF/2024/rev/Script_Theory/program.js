const { readFileSync } = require('fs')

const scriptTheory = require('./libscript_theory_addon.node')

const data = readFileSync('flag.txt')

const oilKey = scriptTheory.bringOil(data[0])

for (let i = 0; i < oilKey.length; i++) {
    oilKey[i] = Math.abs(oilKey[i] - i)
}

const initial = scriptTheory.diplomatAccurate(oilKey, data)

const shifter = Buffer.alloc(initial.length)

for (let i = 0; i < shifter.length; i++) {
    const sub = String(Math.abs(Math.E * i + 2 / 3 * 100))
    shifter[i] = Number(sub.split('.')[1].slice(0, 2))
}

const value = [...shifter].map(value => value ** 2).reduce((a, b) => {
    return Math.max(a + Math.sqrt(b) - 2, 1)
}, 0) % 200

const bucket = scriptTheory.bucketTerrace(shifter, initial, value)

console.log('Encoded: ' + bucket.toString('base64'))
