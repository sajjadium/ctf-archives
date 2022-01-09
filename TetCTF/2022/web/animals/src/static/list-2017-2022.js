class animal2{
    constructor(){
    }

    all(){
        return {
            "2017": "chicken 🐔",
            "2018": "dog 🐶",
            "2019": "pig 🐷",
            "2020": "mouse 🐭",
            "2021": "buffalo 🐃",
            "2022": "tiger 🐯",
        }
    }

}

let instance = new animal2()
exports.default = instance;
module.exports = exports['default'];