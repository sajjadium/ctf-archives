CREATE TABLE `users` (
    `uuid` varchar(36) PRIMARY KEY NOT NULL,
    `username` varchar(32) NOT NULL default '',
    `password` varchar(64) NOT NULL default ''
);
CREATE UNIQUE INDEX `useruuid` ON `users`(`uuid`);

CREATE TABLE `notes` (
    `uuid` varchar(36) PRIMARY KEY NOT NULL,
    `timestamp` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `user` varchar(36) NOT NULL,
    `title` varchar(64) NOT NULL default '',
    `body` TEXT NOT NULL default ''
);

CREATE UNIQUE INDEX `noteuuid` ON `notes`(`uuid`);
CREATE INDEX `noteuser` ON `notes`(`user`);

CREATE TABLE `logs` (
    `id` INTEGER PRIMARY KEY,
    `msg` varchar(512) NOT NULL default '',
    `timestamp` DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE UNIQUE INDEX `logid` ON `logs`(`id`);