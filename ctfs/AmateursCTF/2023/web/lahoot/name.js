import friendlyWords from "friendly-words";

function choice(arr){
    return arr[Math.floor(Math.random() * arr.length)];
}

function generate(){
    let luckyRucky = Math.random();
    let number = Math.floor(Math.random() * 899) + 100;
    let base =  choice(friendlyWords.predicates) + choice(friendlyWords.objects);
    if(luckyRucky < 0.01){
        base = "LuckyBear";
    }else if(luckyRucky > 0.03 && luckyRucky < 0.05){
        base = "AccurateBear"
    }
    return base + number;
}

export default generate;
export {generate};

console.log("Test",generate());