const crypto = require('crypto');
const fs = require('fs');

const getHash = (str, salt)=>{
    let hash = crypto.createHash('sha256');
    hash.update(salt);
    hash.update(str);
    return hash.digest('hex');
};

const generateEndpoint = (str, salt)=>{
    let endpointPath = getHash(str, salt);
    let dir = `./views/sandbox/${endpointPath}`;
    
    if(!fs.existsSync(dir)){
        fs.mkdirSync(dir);
    }

    if(!fs.existsSync(`${dir}/index.ejs`)){
        fs.writeFile(`${dir}/index.ejs`, fs.readFileSync("./views/base.ejs", "utf-8"), (err)=>{
            if(err) {
                console.log(`[!] File write error: ${dir}/index.ejs`);
                return false;
            }
            console.log(`[*] Created ${dir}/index.ejs by ${str} (endpoint: ${endpointPath})`);
        });
    }
    return endpointPath;
};

const checkPermission = (path, str, salt)=>{
    return getHash(str, salt) === path;
};

const sanitize = (body)=>{
    reuslt = true
    tmp = body.toLowerCase()
    if(tmp.includes('<') || tmp.includes('>')) return false
    if(tmp.includes('flag')) return false
    
    return true
}

module.exports = {
    generateEndpoint,
    checkPermission,
    sanitize
};
