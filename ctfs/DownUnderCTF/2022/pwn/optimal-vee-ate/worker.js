console.log('V8 version ' + version());
write('> ');

let realm = Realm.create();
Realm.eval(realm, readline());
