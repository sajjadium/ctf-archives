const express = require('express'); 
const path = require('path');
  
const app = express(); 
const PORT = process.env.PORT ?? 3000;

app.use(express.static(path.join(__dirname, 'public')));
  
app.listen(PORT, (err) =>{ 
    if(!err) 
        console.log("mikufanpage running on port "+ PORT) 
    else 
        console.log("Err ", err); 
}); 

app.get("/image", (req, res) => {
    if (req.query.path.split(".")[1] === "png" || req.query.path.split(".")[1] === "jpg") { // only allow images
        res.sendFile(path.resolve('./img/' + req.query.path));
    } else {
        res.status(403).send('Access Denied');
    }
});