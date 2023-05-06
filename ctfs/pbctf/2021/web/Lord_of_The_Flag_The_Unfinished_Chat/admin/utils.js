const admin = require("firebase-admin");

// Generate in the firebase console -> Project settings -> Service accounts -> Firebase Admin SDK
const serviceAccount = require("./serviceAccountKey.json");

const app = admin.initializeApp({
    credential: admin.credential.cert(serviceAccount)
});


async function createAdminUser(teamHash) {
    return admin
        .auth()
        .createCustomToken(teamHash, { admin: true, room: teamHash});
}

async function deleteTeamRoom(teamHash) {
    const roomRef = admin.firestore(app).doc(`rooms/${teamHash}`);
    await admin.firestore(app).recursiveDelete(roomRef);
}

async function deleteAllRooms() {
    const roomsRef = admin.firestore(app).collection(`rooms`);
    await admin.firestore(app).recursiveDelete(roomsRef);
}

async function deleteAllUsers() {
    const userPages = [];
    let pageToken = undefined;
    do {
        const userPage = await admin.auth().listUsers(1000, pageToken)
        userPages.push(userPage);
        pageToken = userPage.pageToken;
    } while (pageToken);

    for (const userPage of userPages) {
        await admin.auth().deleteUsers(userPage.users.map(u => u.uid));
    }

}

async function deleteEverything() {
   await deleteAllRooms()
   await deleteAllUsers();
}

module.exports = { createAdminUser, deleteTeamRoom, deleteEverything, deleteAllUsers, deleteAllRooms };