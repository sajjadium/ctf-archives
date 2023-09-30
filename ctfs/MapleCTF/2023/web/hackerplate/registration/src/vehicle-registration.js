import DBFactory from "./db.js";

export default class VehicleRegistration {
    createdAt; // date of creation
    pid; // password ID
    name; // name of vehicle owner
    birthdate; // birthdate of vehicle owner
    vin; // vehicle identification number
    uid; // user ID, if exists
    attempting;
    constructor(name, pid, birthdate, vin) {
        this.name = name;
        this.pid = pid;
        this.birthdate = birthdate;
        this.vin = vin;
        this.createdAt = new Date();
        this.attempting = false;
    }

    async addUser() {
        const db = await DBFactory.getDB();
        const uid = await db.createUser(this.name, this.pid, this.birthdate);
        this.uid = uid;
    }

    async addVehicle(plate) {
        const db = await DBFactory.getDB();
        await db.createVehicle(this.vin, this.uid, plate);
    }

    isAttempting () {
        return this.attempting;
    }

    attempt() {
        this.attempting = true;
    }

    cancelAttempt() {
        this.attempting = false;
    }

    async finalize(plate) {
        // await this.addVehicle(plate); // storage is expensive :)
        return true;
    }

    expired() {
        // remove in-flight requests after 15 minutes
        return this.createdAt.getTime() + (1000 * 60 * 15) < new Date().getTime();
    }

    async rollback() {
        const db = await DBFactory.getDB();
        await db.deleteVehicle(this.vin);
        const vehicles = await db.getVehicles(this.uid);
        if (vehicles.length === 0) {
            await db.deleteUser(this.uid);
        }
    }
}