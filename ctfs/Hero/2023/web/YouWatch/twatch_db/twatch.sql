DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS chats;
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS videos;

CREATE TABLE `users` (
    `id` INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `pseudo` varchar(20) NOT NULL UNIQUE,
    `email` varchar(60) NOT NULL UNIQUE,
    `password` varchar(64) NOT NULL
);

CREATE TABLE `chats` (
    `id` INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `publicId` VARCHAR(36) NOT NULL UNIQUE,
    `nbMessages` INT
);

CREATE TABLE `videos`(
    `id` VARCHAR(36) PRIMARY KEY NOT NULL,
    `name` VARCHAR(100) NOT NULL,
    `userId` INT REFERENCES users(`id`),
    `chatId` VARCHAR(36) REFERENCES chats(`publicId`) ON UPDATE CASCADE,
    `isPrivate` INT NOT NULL,
    `pathVideo` VARCHAR(200) NOT NULL UNIQUE
);

CREATE TABLE `messages`(
    `id` VARCHAR(36) PRIMARY KEY NOT NULL,
    `content` VARCHAR(10000) NOT NULL,
    `userId` INT REFERENCES users(`id`),
    `chatId` VARCHAR(36) REFERENCES chats(`publicId`) ON UPDATE CASCADE
);

INSERT INTO users VALUES(1,"admin","admin@youwatch.fr","8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918");
INSERT INTO chats VALUES(1,"2e6e4787-6722-46da-83f9-8d38a4c7a922",0);
INSERT INTO videos VALUES("cb13a41b-04a1-47aa-8687-885fe74a1062","[ADMIN] Very Secret Video",1,"2e6e4787-6722-46da-83f9-8d38a4c7a922",1,"for_players.mp4");