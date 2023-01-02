drop database TetCTFToken;

create database TetCTFToken;
use TetCTFToken;

CREATE TABLE `TetCTFToken`.`TetCTFToken_User` (
  `user_id` BIGINT NOT NULL AUTO_INCREMENT,
  `user_name` VARCHAR(250) NULL,
  `user_email` VARCHAR(250) NULL,
  `user_password` VARCHAR(250) NULL,
  PRIMARY KEY (`user_id`));
insert into TetCTFToken_User (user_id,user_name,user_email,user_password) value (1,"admin","admin@TetCTFToken.1337","#####CENSORED#####"),(2,"ducnt","ducnt@TetCTFToken.1337","#####CENSORED#####"),(3,"khanghh","khanghh@TetCTFToken.1337","#####CENSORED#####");
 
DELIMITER ;


USE `TetCTFToken`;
DROP procedure IF EXISTS `sp_createUser`;

DELIMITER $$
CREATE DEFINER=`TetCTFToken`@`localhost` PROCEDURE `sp_createUser`(
  IN p_name VARCHAR(250),
  IN p_email VARCHAR(250),
  IN p_password VARCHAR(250)

)


BEGIN
    IF ( select exists (select 1 from TetCTFToken_User where user_name = p_name) ) 

    THEN
        select 'User Exists !!!';
     
    ELSE
     
        insert into TetCTFToken_User
        (
            user_name,
            user_email,
            user_password
        )
        values
        (
            p_name,
            p_email,
            p_password
        );

    END IF;

END$$


DELIMITER ;

USE `TetCTFToken`;
DROP procedure IF EXISTS `sp_ResetPasswdUser`;

DELIMITER $$
CREATE DEFINER=`TetCTFToken`@`localhost` PROCEDURE `sp_ResetPasswdUser`(

    IN p_name VARCHAR(250),
    IN p_password VARCHAR(250)

)


BEGIN
    IF ( select not exists (select 1 from TetCTFToken_User where user_name = p_name) ) THEN
     
        select 'User Not Exists !!';
     
    ELSE

        update TetCTFToken_User set user_password = p_password where user_name = p_name;

    END IF;

END$$
DELIMITER ;


USE `TetCTFToken`;
DROP procedure IF EXISTS `sp_validateLogin`;

DELIMITER $$
CREATE DEFINER=`TetCTFToken`@`localhost` PROCEDURE `sp_validateLogin`(
IN p_username VARCHAR(250)
)
BEGIN
    select * from TetCTFToken_User where user_email = p_username;
END$$

DELIMITER ;


USE `TetCTFToken`;
DROP procedure IF EXISTS `sp_getUsername`;

DELIMITER $$
CREATE DEFINER=`TetCTFToken`@`localhost` PROCEDURE `sp_getUsername`(
IN p_id BIGINT
)

BEGIN
    IF ( select not exists (select 1 from TetCTFToken_User where user_id = p_id) ) THEN
     
        select 'User Not Exists !!';
     
    ELSE

        select user_name from TetCTFToken_User where user_id = p_id;

    END IF;

END$$
DELIMITER ;

