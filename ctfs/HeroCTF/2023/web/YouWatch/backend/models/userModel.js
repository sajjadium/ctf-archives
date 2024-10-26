'use strict';
const { Model } = require('sequelize');

module.exports = (sequelize, DataTypes) => {
    class User extends Model {
        static associate({Video, Message}) {
            this.hasMany(Video, {foreignKey: 'userId', as: 'videos'})
            this.hasMany(Message, {foreignKey: 'id', as: 'messages'})
        }
    };

    User.init({
        id: {
            allowNull: false,
            primaryKey: true,
            autoIncrement: true,
            type: DataTypes.INTEGER
        },
        pseudo: {
            allowNull: false,
            type: DataTypes.STRING,
            unique: true,
            validate: {
                notNull: {msg: "Pseudo is required"},
                notEmpty: {msg: "Pseudo cannot be empty"}
            }
        },
        email: {
            allowNull: false,
            type: DataTypes.STRING,
            unique: true,
            validate: {
                isEmail: {msg: "Email must be valid or not be used by another user"}
            }
        },
        password: {
            allowNull: false,
            type: DataTypes.STRING
        }
    },
    {
        sequelize,
        tableName: 'users',
        modelName: 'User',
        timestamps: false
    });
    return User;
}