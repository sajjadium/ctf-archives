const { Sequelize, DataTypes } = require('sequelize');
const fsp = require("fs/promises");
const bcrypt = require("bcrypt");
const path = require("path");

const sequelize = new Sequelize({
  dialect: 'sqlite',
  storage: 'blogme.db',
  logging: false
});

const User = sequelize.define('User', {
    user: {
        type: DataTypes.STRING,
        primaryKey: true,
        allowNull: false,
        unique: true,
        validate: {
            len: [3, 16]
        }
    },
    pass: {
        type: DataTypes.STRING,
        allowNull: false
    },
    profilePic: {
        type: DataTypes.STRING
    }
}, {
    hooks: {
        beforeCreate(s) {
            if(!s.profilePic) {
                s.profilePic = "https://ui-avatars.com/api/?name=" + encodeURIComponent(s.user);
            }
        }
    }
});

const Post = sequelize.define('Post', {
    id: {
        type: DataTypes.UUID,
        primaryKey: true,
        unique: true,
        defaultValue: Sequelize.UUIDV4,
    },
    title: {
        type: DataTypes.STRING,
        allowNull: false,
        validate: {
            len: [3, 30]
        }
    },
    text: {
        type: DataTypes.STRING,
        allowNull: false,
        validate: {
            len: [1, 300]
        }
    },
});

const File = sequelize.define('File', {
    id: {
        type: DataTypes.UUID,
        primaryKey: true,
        unique: true,
        defaultValue: Sequelize.UUIDV4,
    },
    mimeType: {
        type: DataTypes.STRING,
        allowNull: false
    },
});

const Comment = sequelize.define('Comment', {
    id: {
        type: DataTypes.UUID,
        primaryKey: true,
        unique: true,
        defaultValue: Sequelize.UUIDV4,
    },
    text: {
        type: DataTypes.STRING,
        allowNull: false,
        validate: {
            len: [1, 150]
        }
    }
});

const addFile = (user, buffer, type) => {
    return new Promise(async (resolve, reject) => {
        if(user.user !== "admin") {
            if(!["image/jpeg", "image/png"].includes(type)) {
                return reject("Invalid image type, only image/jpeg or image/png are allowed");
            }
            let files = await user.getFiles();
            if(files.length >= 5) {
                return reject("You cannot upload any more images. Please delete some");
            }
        }

        if(buffer.length > 100000) { // 100000 bytes = 100 KB
            return reject("File exceeds max size of 100 KB");
        }

        let file = await File.create({ mimeType: type });
        user.addFile(file);
        file.setUser(user);

        fsp.writeFile(path.resolve("uploads", file.id), buffer)
        .then(() => resolve(file.id))
        .catch(err => {
            console.log(err);
            reject(err.message);
        });
    });
};

User.hasMany(Post);
User.hasMany(File);
Post.belongsTo(User);
File.belongsTo(User);
Post.hasMany(Comment);
Comment.belongsTo(User);
Comment.belongsTo(Post);

sequelize.sync();

module.exports = { sequelize, User, Post, Comment, File, addFile };