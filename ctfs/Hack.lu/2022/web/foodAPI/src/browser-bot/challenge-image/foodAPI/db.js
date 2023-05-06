import { DataTypes, Database, Model, SQLite3Connector} from "https://deno.land/x/denodb@v1.0.40/mod.ts";

// Load env
const conf = Deno.env.toObject();

if (!conf.DBDEBUG || !conf.DBFILEPATH || !conf.FLAG) {
    console.log('.env missing')
    conf.DBDEBUG = '0';
    conf.DBFILEPATH = '/tmp/db.sqlite';
    conf.FLAG = 'flag{fake_fl4g}';
}

// we use sqlite ight
const connector = new SQLite3Connector({
    filepath: conf.DBFILEPATH,
});


const db = new Database({connector, debug: conf.DBDEBUG === '1'});


class Food extends Model {
    static table = 'food';
    static fields = {
    "id": {
        primaryKey: true,
        autoIncrement: true,
    },
    name: DataTypes.STRING,
    difficulty: DataTypes.STRING,
    ingredients: DataTypes.STRING,
    };
}


class Flag extends Model {
    static table = 'flag';
    static fields = {
        flag: DataTypes.STRING,
    };
}

// add them
db.link([Food, Flag]);
await db.sync({ drop: true });

// add data
await Food.create({
    name: 'Pancakes',
    difficulty: 'easy',
    ingredients: 'flour, eggs, milk, butter, apples, cinnamon, sugar',
})
await Food.create({
    name: 'WURST',
    difficulty: 'WURST',
    ingredients: 'WURST and other stuff',
})
await Food.create({
    name: 'Rouladen',
    difficulty: 'hard',
    ingredients: 'bacon, onions, mustard, pickles, thinly sliced beef',
})
await Flag.create({ 
    flag: conf.FLAG 
});

export default Food
