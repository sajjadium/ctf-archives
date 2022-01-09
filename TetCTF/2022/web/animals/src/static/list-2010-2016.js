class animals1{
    constructor(){
    }

    all(){
        return {
            "2010":"tiger 🐯",
            "2011":"cat 🐱",
            "2012": "dragon 🐲",
            "2013": "snake 🐍",
            "2014": "horse 🐴",
            "2015":"goat 🐐",
            "2016":"monkey 🐵"
        }
    }

}

let instance = new animals1()

exports.default = instance;
module.exports = exports['default'];
