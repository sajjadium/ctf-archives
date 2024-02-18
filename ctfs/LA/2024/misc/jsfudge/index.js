#!/usr/local/bin/node
const runCode=(code)=>{const allowed=new Set('()+[]!');for(const char of code){if(!allowed.has(char)){console.log('Oops, make sure to only use characters "()+[]!"');return;}}
const oldProto=[].__proto__.toString;[].__proto__.toString=()=>'^w^';try{const codeRes=eval(code);console.log(codeRes.toString());}
catch(e){console.log('oopsie woopsie stinki poopie',e);}
finally{[].__proto__.toString=oldProto;}}
const rl=require('readline').createInterface({input:process.stdin,terminal:false});(async()=>{console.log('Gimme some js code to run');for await(const line of rl){runCode(line.trim());rl.close();return;}})();