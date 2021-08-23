const { Sequelize, Model, DataTypes } = require('sequelize');
const crypto = require("crypto");

const sequelize = new Sequelize({
    dialect: 'sqlite',
    storage: 'styleme.sqlite3'
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
    }
});

const Style = sequelize.define('Style', {
    id: {
        type: DataTypes.STRING,
        primaryKey: true,
        unique: true
    },
    title: {
        type: DataTypes.STRING,
        allowNull: false,
        validate: {
            len: [3, 128]
        }
    },
    url: {
        type: DataTypes.STRING
    },
    global: {
        type: DataTypes.BOOLEAN,
        defaultValue: false
    },
    css: {
        type: DataTypes.STRING,
        allowNull: false
    },
    hidden: {
        type: DataTypes.BOOLEAN,
        allowNull: false,
        defaultValue: true
    }
}, {
    hooks: {
        beforeCreate(s) {
            s.css = s.css.trim();
            s.id = crypto.randomBytes(6).toString("hex");
        }
    }
});

User.hasMany(Style)
Style.belongsTo(User);

sequelize.sync();

User.count().then(async c => {
    if(c !== 0) return;
    console.log('initialing db with default data...');

    let adminUser = await User.create({ user: "admin", pass: "this is the actual admin password :O" });
    let defaultUser = await User.create({ user: "default", pass: "password for default templates :^)" });

    // add some default color styles :D
    for(let color of ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]) {
        let style = await Style.create({ title: `${color} background`, hidden: false, url: "http://example.com", css: `
* {
    background-color: ${color} !important;
}` 
});
        style.setUser(defaultUser);
        defaultUser.addStyle(style);
    }

    let flagStyle = await Style.create({ title: "super secret admin only flag style", global: true, css: `
/* flag: ${process.env.FLAG} */

h1,h2,h3,h4,h5,h6,a,p,span {
    background: linear-gradient(45deg,#FF0000,#FF7F00,#FFFF00,#00FF00,#0000FF,#4B0082,#8B00FF);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-size: 400% 400% !important;

    -webkit-animation: rainbow 5s ease infinite !important;
       -moz-animation: rainbow 5s ease infinite !important;
            animation: rainbow 5s ease infinite !important;
}

@-webkit-keyframes rainbow {
    0%{background-position:0% 50%}
    50%{background-position:100% 50%}
    100%{background-position:0% 50%}
}
@-moz-keyframes rainbow {
    0%{background-position:0% 50%}
    50%{background-position:100% 50%}
    100%{background-position:0% 50%}
}
@keyframes rainbow { 
    0%{background-position:0% 50%}
    50%{background-position:100% 50%}
    100%{background-position:0% 50%}
}`, hidden: true });

    flagStyle.setUser(adminUser);
    adminUser.addStyle(flagStyle);
});

const requiresLogin = (req, res, next) => {
    if(!req.user) {
        req.session.error = "You must be logged in to access this page.";
        return res.redirect("/");
    }
    next();
};

module.exports = { User, Style, requiresLogin };