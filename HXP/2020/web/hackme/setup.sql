-- Create user
CREATE USER hackmd@127.0.0.1 IDENTIFIED BY "__DB_PASSWORD__";
GRANT CREATE, SELECT, INSERT, UPDATE ON hackmd.* TO hackmd@127.0.0.1;
FLUSH PRIVILEGES;

-- Insert admin user and flag
USE hackmd;

INSERT INTO `Users` VALUES (
    "__ADMIN_UUID__",
    "admin",
    NULL,
    NULL,
    NOW(),
    NOW(),
    NULL,
    NULL,
    "__ADMIN_EMAIL__",
    "__ADMIN_PASSWORD_HASH__",
    "__ADMIN_DELETE_UUID__"
);
INSERT INTO `Notes` VALUES (
    "__NOTE_UUID__",
    "__ADMIN_UUID__",
    "__FLAG__",
    "flag",
    NOW(),
    NOW(),
    "the-flag",
    'private',
    0,
    "__ADMIN_UUID__",
    NOW(),
    NULL,
    NOW(),
    CONCAT('[["__ADMIN_UUID__", 0, ', LENGTH("__FLAG__"), ", ", UNIX_TIMESTAMP(), ", ", UNIX_TIMESTAMP(), "]]"),
    NULL
);
INSERT INTO `Authors` (`color`, `noteId`, `userId`, `createdAt`, `updatedAt`) VALUES (
    "#ff0000",
    "__NOTE_UUID__",
    "__ADMIN_UUID__",
    NOW(),
    NOW()
);
INSERT INTO `Revisions` VALUES (
    "__REVISION_UUID__",
    "__NOTE_UUID__",
    NULL,
    "",
    NULL,
    0,
    NOW(),
    NOW(),
    NULL
);

-- No deleting either of those
DELIMITER EOT

CREATE TRIGGER user_update BEFORE UPDATE ON `Users`
FOR EACH ROW BEGIN
    IF OLD.id = "__ADMIN_UUID__" THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cannot modify the admin user';
    END IF;
END;
EOT

CREATE TRIGGER note_update BEFORE UPDATE ON `Notes`
FOR EACH ROW BEGIN
    IF OLD.id = "__NOTE_UUID__" AND (OLD.content <> NEW.content OR OLD.title <> NEW.title OR OLD.shortid <> NEW.shortid OR OLD.permission <> NEW.permission OR OLD.alias <> NEW.alias OR NEW.deletedAt <> NULL) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cannot modify the flag note in this way';
    END IF;
END;
EOT

CREATE TRIGGER note_insert BEFORE INSERT ON `Notes`
FOR EACH ROW BEGIN
    IF NEW.ownerId = "__ADMIN_UUID__" THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Admin cannot create notes';
    END IF;
END;
EOT

CREATE TRIGGER revision_update BEFORE UPDATE ON `Revisions`
FOR EACH ROW BEGIN
    IF OLD.noteId = "__NOTE_UUID__" THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cannot modify the flag note revisions';
    END IF;
END;
EOT

CREATE TRIGGER revision_insert BEFORE INSERT ON `Revisions`
FOR EACH ROW BEGIN
    IF NEW.noteId = "__NOTE_UUID__" THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cannot add flag note revisions';
    END IF;
END;
EOT

CREATE TRIGGER user_insert BEFORE INSERT ON `Users`
FOR EACH ROW BEGIN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cannot create users';
END;
EOT

DELIMITER ;
