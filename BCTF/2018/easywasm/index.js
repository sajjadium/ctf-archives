const Module = require('./easywasm.js');

util=require('util')
const wasm = Module({wasmBinaryFile: 'easywasm.wasm'});
function to_cstr(str){
    var ptr = wasm.allocate(wasm.intArrayFromString(str),'i8',wasm.ALLOC_NORMAL);
    return ptr;
}


wasm.onRuntimeInitialized = function(){
  var express = require("express");
  var bodyParser = require("body-parser"); 
  var app = express(); 
  app.use(bodyParser.urlencoded({ extended: false }));  
  var hostName = '0.0.0.0';
  var port = 23333;

  app.all('*', function(req, res, next) {  
      res.header("Access-Control-Allow-Origin", "*");  
      res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");  
      res.header("Access-Control-Allow-Methods","PUT,POST,GET,DELETE,OPTIONS");  
      res.header("X-Powered-By",' 3.2.1')  
      res.header("Content-Type", "application/json;charset=utf-8");  
      next();  
  });

  app.get("/add_person",function(req,res){
      var name="";
      var is_tutor=-1;
      for(var key in req.query){
        if(key=='name')
          name=req.query[key];
        if(key=='is_tutor')
          is_tutor=req.query[key];
          
      }
      if (name!=""){
        try{
          result = wasm._add_person(to_cstr(name),is_tutor);
        }
        catch(e) {
          res.send("internal error");
          return;
        }
        if (result!=-1)
          res.send(util.format("create person done, person id = %d",result));
        else
          res.send("too much person");
      }
      else
        res.send("name required");
  })

  app.get("/change_name",function(req,res){
    var name="";
    var id="";
    for(var key in req.query){
      if(key=='name')
        name=req.query[key];
      if(key=='id')
        id=req.query[key];
        
    }
    if (name==""){
      res.send("name required");
      return;
    }
    if (id==""){
      res.send("id required");
      return;
    }
    try{
      result = wasm._change_name(id,to_cstr(name));
    }
    catch(e) {
      res.send("internal error");
      return;
    }
    if (result!=-1)
        res.send(util.format("done"));
    else
        res.send("invalid id");
    

  })

  app.get("/init",function(req,res){
    var admin_key="THIS_IS_A_FAKE_KEY";
    var input_key="";
    for(var key in req.query){
      if(key=='admin_key')
        input_key=req.query[key];
      
    }
    if (input_key==admin_key){
      wasm._init();
      res.send("init done");
    }
    else
      res.send("wrong key");
  })
  app.get("/intro",function(req,res){
    var id="";
    for(var key in req.query){
      if(key=='id')
        id=req.query[key];
    }
    if (id==""){
      res.send("invalid id");
      return;
    }
    try {
      wasm._intro(id);
      res.send("intro sent to log window")
    }
    catch(e) {
      res.send("internal error");
      return;
    }
  })
  app.listen(port,hostName,function(){

    console.log(`server run at http://${hostName}:${port}`);

  });

}
