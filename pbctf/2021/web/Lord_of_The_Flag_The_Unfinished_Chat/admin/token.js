const { createAdminUser } = require('./utils.js');

const teamHash = "cccccccccccccccccccccccccccccccd"
createAdminUser(teamHash).then(token => {
    console.log("ADMIN_ROOM=" + teamHash)
    console.log("ADMIN_TOKEN=" + token)
});

