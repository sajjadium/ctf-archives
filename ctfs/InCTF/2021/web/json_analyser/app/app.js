const express = require('express');
const fileUpload = require('express-fileupload');
const fs = require("fs");
const sqrl = require('squirrelly');
const app = express();
port = 8088



app.use(express.static('static'));
app.set('view engine', 'squirrelly');
app.set('views', __dirname + '/views')
app.use(fileUpload());

app.get('/waf', function (req, res) {
    res.sendFile(__dirname+'/static/waf.html');
});

app.get('/restart',function(req,res){
    var content='';
    content=fs.readFileSync('package.json','utf-8')
    fs.writeFileSync('package1.json', content)
})

app.get('/', function (req, res) {
    res.sendFile(__dirname+'/static/index.html');
});

app.post('/upload', function(req, res) {
    let uploadFile;
    let uploadPath;
    if(req.body.pin !== "[REDACTED]"){
        return res.send('bad pin')
    }
    if (!req.files || Object.keys(req.files).length === 0) {
      return res.status(400).send('No files were uploaded.');
    }
    uploadFile = req.files.uploadFile;
    uploadPath = __dirname + '/package.json' ;
    uploadFile.mv(uploadPath, function(err) {
        if (err)
            return res.status(500).send(err);
        try{
        	var config = require('config-handler')();
        }
        catch(e){
            const src = "package1.json";
            const dest = "package.json";
            fs.copyFile(src, dest, (error) => {
                if (error) {
                    console.error(error);
                    return;
                }
                console.log("Copied Successfully!");
            });
        	return res.sendFile(__dirname+'/static/error.html')
        }
        var output='\n';
        if(config['name']){
            output=output+'Package name is:'+config['name']+'\n\n';
        }
        if(config['version']){
            output=output+ "version is :"+ config['version']+'\n\n'
        }
        if(config['author']){
            output=output+"Author of package:"+config['author']+'\n\n'
        }
        if(config['license']){
            var link=''
            if(config['license']==='ISC'){
                link='https://opensource.org/licenses/ISC'+'\n\n'
            }
            if(config['license']==='MIT'){
                link='https://www.opensource.org/licenses/mit-license.php'+'\n\n'
            }
            if(config['license']==='Apache-2.0'){
                link='https://opensource.org/licenses/apache2.0.php'+'\n\n'
            }
            if(link==''){
                var link='https://opensource.org/licenses/'+'\n\n'
            }
            output=output+'license :'+config['license']+'\n\n'+'find more details here :'+link;
        }
        if(config['dependencies']){
            output=output+"following dependencies are thier corresponding versions are used:" +'\n\n'+'     '+JSON.stringify(config['dependencies'])+'\n'
        }

        const src = "package1.json";
        const dest = "package.json";
        fs.copyFile(src, dest, (error) => {
            if (error) {
                console.error(error);
                return;
            }
        });
        res.render('index.squirrelly', {'output':output})
    });
});



var server= app.listen(port, () => {
    console.log(`Example app listening at http://localhost:${port}`)
});
server.setTimeout(10000);
