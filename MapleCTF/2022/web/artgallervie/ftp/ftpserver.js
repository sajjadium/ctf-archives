var ftpd = require('ftpd');
var fs = require('fs');
var path = require('path');
var keyFile;
var certFile;
var server;
var options = {
    host: process.env.IP || '127.0.0.1',
    port: process.env.FTP_PORT || 8021,
    tls: null,
};

server = new ftpd.FtpServer(options.host, {
    getInitialCwd: function() {
        return '/';
    },
    getRoot: function() {
        return process.cwd()+"/files";
    },
    pasvPortRangeStart: 1025,
    pasvPortRangeEnd: 1050,
    tlsOptions: options.tls,
    allowUnauthorizedTls: true,
    useWriteFile: false,
    useReadFile: false,
    uploadMaxSlurpSize: 7000, // N/A unless 'useWriteFile' is true.
});

server.on('error', function(error) {
    console.log('FTP Server error:', error);
});

server.on('client:connected', function(connection) {
    console.log('client connected: ' + connection.remoteAddress);
    connection.on('command:user', function(user, success, failure) {
        success();
    });

    connection.respond = function(message, callback){if(callback)callback()};

    connection.on('command:pass', function(pass, success, failure) {
        success('ppp');
    });

    let original_ondata = connection._onData;

    connection._onData = function swag(data){
        // there are no intended vulnerabilities within this function, it is not in the scope of the challenge
        let start = 0;
        for(let i = 0; i < data.length; ++i){
            if(data[i] == 10){
                original_ondata.call(connection, data.slice(start, i));
                start = i+1;
            }
        }
    }

});

server.debugging = 4;
server.listen(options.port);
console.log('Listening on port ' + options.port);
