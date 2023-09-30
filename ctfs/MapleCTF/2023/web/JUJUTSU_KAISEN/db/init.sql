CREATE TABLE IF NOT EXISTS characters(
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    name                    TEXT    NOT NULL UNIQUE,
    occupation              INT     NOT NULL,
    cursed_technique        TEXT,
    img_file                TEXT,
    notes                   TEXT
);



INSERT INTO characters (id, name, occupation, cursed_technique, img_file, notes) VALUES (1, "Itadori Yuji", "Student", "Left-Right-Goodnight", "yuji.png", "why use cursed techniques when you have left fist and right fist");
INSERT INTO characters (id, name, occupation, cursed_technique, img_file, notes) VALUES (2, "Nobara Kugisaki", "Student", "Straw Doll", "nobara.png", "My next tattoo is of her");
INSERT INTO characters (id, name, occupation, cursed_technique, img_file, notes) VALUES (3, "Megumi Fushiguro", "Student", "Ten Shadows", "megumi.png", "Sasuke, is that you?");
INSERT INTO characters (id, name, occupation, cursed_technique, img_file, notes) VALUES (4, "Satoru Gojo", "Teacher", "Limitless", "gojo.png", "the strongest");
INSERT INTO characters (id, name, occupation, cursed_technique, img_file, notes) VALUES (5, "Choso", "Death Painting", "Blood Manipulation", "choso.png", "maple{fake}");
INSERT INTO characters (id, name, occupation, cursed_technique, img_file, notes) VALUES (6, "Suguru Geto", "Exile", "Cursed Spirit Manipulation", "geto.png", "wish i had his hair");
INSERT INTO characters (id, name, occupation, cursed_technique, img_file, notes) VALUES (7, "Hajime Kashimo", "Culling Game Participant", "Electricity", "hajime.png", "really wish i had his hair");
INSERT INTO characters (id, name, occupation, cursed_technique, img_file, notes) VALUES (8, "Toji Fushiguro", "Menace", null, "toji.png", "why use cursed techniques when you have a GLOCK");
INSERT INTO characters (id, name, occupation, cursed_technique, img_file, notes) VALUES (9, "Kento Nanami", "Jujutsu Sorcerer", "Seven-Three", "nanami.png", "Yuji's dad");
INSERT INTO characters (id, name, occupation, cursed_technique, img_file, notes) VALUES (10, "Maki Zenin", "Itachi Cosplayer", null, "maki.png", "The best character design I've seen");
INSERT INTO characters (id, name, occupation, cursed_technique, img_file, notes) VALUES (11, "Noritoshi Kamo", "Student", "Blood Manipulation", "noritoshi.png", "I like your cousin more sorry");
INSERT INTO characters (id, name, occupation, cursed_technique, img_file, notes) VALUES (12, "Toge Inumaki", "Student", "Cursed Speech", "inumaki.png", "salmon");
INSERT INTO characters (id, name, occupation, cursed_technique, img_file, notes) VALUES (13, "Aoi Todo", "Student", "Boogie Woogie", "todo.png", "I like tall girls too");
INSERT INTO characters (id, name, occupation, cursed_technique, img_file, notes) VALUES (15, "Ryoumen Sukuna", "King of Curses", "Cleave", "sukuna.png", "I love his design. He'd kill me, but i love his design");
