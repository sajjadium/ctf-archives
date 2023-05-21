'use strict';
const { Model } = require('sequelize');

module.exports = (sequelize, DataTypes) => {
    class Message extends Model {
        static associate({User,Chat}){
            this.belongsTo(User,{foreignKey: 'userId', as: 'users'})
            this.belongsTo(Chat,{foreignKey: 'chatId', as: 'chats'})
        }
    };

    Message.init({
        id: {
            allowNull: false,
            primaryKey: true,
            type: DataTypes.STRING
        },
        userId: {
            allowNull: false,
            type: DataTypes.STRING
        },
        content: {
            allowNull: false,
            type: DataTypes.STRING,
            validate: {
                notNull: {msg: "Content of message is required"},
                notEmpty: {msg: "Content of message cannot be empty"}
            }
        },
        chatId: {
            allowNull: false,
            type: DataTypes.STRING
        }
    },
    {
        sequelize,
        tableName: 'messages',
        modelName: 'Message',
        timestamps: false
    });
    return Message;
}