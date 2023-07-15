import { Sequelize, Model, DataTypes } from "sequelize";
const sequelize = new Sequelize(process.env.DATABASE || "postgres://service:s3cur1ty_by_netw0rk_is0lation_m0m3nt@database/lahoot");
// bare boilerplate sequelize for now
class Player extends Model {}
Player.init({
    id: {
        type: DataTypes.STRING,
        primaryKey: true
    },
    lastSubmitIndex: {
        type: DataTypes.INTEGER,
        defaultValue: 0
    }
}, { sequelize, modelName: "player" });

export async function init(){
    await sequelize.authenticate();
    // tbf I don't care about the db persistence!
    await sequelize.sync({
        alter: true,
        force: true
    });
}

export default Player;

export {Player};