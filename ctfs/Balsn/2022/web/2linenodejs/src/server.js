#!/usr/local/bin/node
process.stdin.setEncoding('utf-8');
process.stdin.on('readable', () => {
  try{
    console.log('HTTP/1.1 200 OK\nContent-Type: text/html\nConnection: Close\n');
    const json = process.stdin.read().match(/\?(.*?)\ /)?.[1],
    obj = JSON.parse(json);
    console.log(`JSON: ${json}, Object:`, require('./index')(obj, {}));
  }catch{
    require('./usage')
  }finally{
    process.exit();
  }
});
