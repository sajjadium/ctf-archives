'use strict';
const { Model } = require('sequelize');

module.exports = (sequelize, DataTypes) => {
    class Video extends Model {
        static associate({User, Chat}){
            this.belongsTo(User,{foreignKey: 'userId', as: 'users'})
            this.belongsTo(Chat,{foreignKey: 'chatId', as: 'chats'})
        }
    };

    Video.init({
        id: {
            allowNull: false,
            primaryKey: true,
            type: DataTypes.STRING
        },
        name: {
            allowNull: false,
            type: DataTypes.STRING,
            validate: {
                notNull: {msg: "Name is required"},
                notEmpty: {msg: "Name cannot be empty"}
            }
        },
        userId: {
            allowNull: false,
            type: DataTypes.STRING
        },
        chatId: {
            allowNull: false,
            type: DataTypes.STRING
        },
        isPrivate: {
            allowNull: false,
            type: DataTypes.INTEGER
        },
        pathVideo: {
            allowNull: false,
            type: DataTypes.STRING
        }
    },
    {
        sequelize,
        tableName: 'videos',
        modelName: 'Video',
        timestamps: false
    });
    return Video;
}