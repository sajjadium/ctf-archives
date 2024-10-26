'use strict';
const { Model } = require('sequelize');

module.exports = (sequelize, DataTypes) => {
    class Chat extends Model {
        static associate({Video, Message}) {
            this.hasMany(Video, {foreignKey: 'chatId', as: 'videos', onUpdate: 'cascade', hooks: true})
            this.hasMany(Message, {foreignKey: 'id', as: 'messages'})
        }
    };

    Chat.init({
        id: {
            allowNull: false,
            autoIncrement: true,
            primaryKey: true,
            type: DataTypes.INTEGER
        },
        publicId: {
            allowNull: false,
            type: DataTypes.STRING
        },
        nbMessages: {
            allowNull: true,
            type: DataTypes.INTEGER
        }
    },
    {
        sequelize,
        tableName: 'chats',
        modelName: 'Chat',
        timestamps: false,
        initialAutoIncrement: 1
    });
    return Chat;
}