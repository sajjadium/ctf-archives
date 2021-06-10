if (readline().startsWith('SheeK6ul')) {
console.log('Welcome to krautflare workers, just send us a single line of javascript and we will execute it serverless on our server.');
Realm.create();
Realm.global(0).flag = read('/flag');
Realm.eval(1, readline());
}
