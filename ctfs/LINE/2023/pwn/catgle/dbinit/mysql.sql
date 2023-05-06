
-- MySQL dump 10.13  Distrib 8.0.32, for Linux (x86_64)
--
-- Host: catgle_mysql    Database: catgle
-- ------------------------------------------------------
-- Server version   8.0.32

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `catgle`
--

CREATE DATABASE IF NOT EXISTS `catgle` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `catgle`;

--
-- Table structure for table `answer`
--

DROP TABLE IF EXISTS `answer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `answer` (
  `id` int NOT NULL AUTO_INCREMENT,
  `content` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `create_date` datetime NOT NULL,
  `modify_date` datetime DEFAULT NULL,
  `question_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `is_markdown` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_answer_question_id_question` (`question_id`),
  KEY `fk_answer_user_id_users` (`user_id`),
  CONSTRAINT `fk_answer_question_id_question` FOREIGN KEY (`question_id`) REFERENCES `question` (`id`),
  CONSTRAINT `fk_answer_user_id_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `ck_answer_is_markdown` CHECK ((`is_markdown` in (0,1)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `answer`
--

LOCK TABLES `answer` WRITE;
/*!40000 ALTER TABLE `answer` DISABLE KEYS */;
/*!40000 ALTER TABLE `answer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `answer_voter`
--

DROP TABLE IF EXISTS `answer_voter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `answer_voter` (
  `user_id` int NOT NULL,
  `answer_id` int NOT NULL,
  PRIMARY KEY (`user_id`,`answer_id`),
  KEY `fk_answer_voter_answer_id_answer` (`answer_id`),
  CONSTRAINT `fk_answer_voter_answer_id_answer` FOREIGN KEY (`answer_id`) REFERENCES `answer` (`id`),
  CONSTRAINT `fk_answer_voter_user_id_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `answer_voter`
--

LOCK TABLES `answer_voter` WRITE;
/*!40000 ALTER TABLE `answer_voter` DISABLE KEYS */;
/*!40000 ALTER TABLE `answer_voter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chall`
--

DROP TABLE IF EXISTS `chall`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chall` (
  `id` int NOT NULL AUTO_INCREMENT,
  `source` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `file_name` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `file_size` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `category` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL,
  `submission_date` datetime DEFAULT NULL,
  `failed` tinyint(1) DEFAULT NULL,
  `reason` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_chall_user_id_users` (`user_id`),
  CONSTRAINT `fk_chall_user_id_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `ck_chall_failed` CHECK ((`failed` in (0,1)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chall`
--

LOCK TABLES `chall` WRITE;
/*!40000 ALTER TABLE `chall` DISABLE KEYS */;
/*!40000 ALTER TABLE `chall` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `question`
--

DROP TABLE IF EXISTS `question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `question` (
  `id` int NOT NULL AUTO_INCREMENT,
  `subject` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `create_date` datetime NOT NULL,
  `modify_date` datetime DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `is_markdown` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_question_user_id_users` (`user_id`),
  CONSTRAINT `fk_question_user_id_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `ck_question_is_markdown` CHECK ((`is_markdown` in (0,1)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question`
--

LOCK TABLES `question` WRITE;
/*!40000 ALTER TABLE `question` DISABLE KEYS */;
/*!40000 ALTER TABLE `question` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `question_voter`
--

DROP TABLE IF EXISTS `question_voter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `question_voter` (
  `user_id` int NOT NULL,
  `question_id` int NOT NULL,
  PRIMARY KEY (`user_id`,`question_id`),
  KEY `fk_question_voter_question_id_question` (`question_id`),
  CONSTRAINT `fk_question_voter_question_id_question` FOREIGN KEY (`question_id`) REFERENCES `question` (`id`),
  CONSTRAINT `fk_question_voter_user_id_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question_voter`
--

LOCK TABLES `question_voter` WRITE;
/*!40000 ALTER TABLE `question_voter` DISABLE KEYS */;
/*!40000 ALTER TABLE `question_voter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `uploaded_model` tinyint(1) NOT NULL,
  `registered_ip` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_activity` datetime DEFAULT NULL,
  `participated` int DEFAULT NULL,
  `ranking` int DEFAULT NULL,
  `register_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_users_username` (`username`),
  UNIQUE KEY `uq_users_registered_ip` (`registered_ip`),
  CONSTRAINT `ck_users_uploaded_model` CHECK ((`uploaded_model` in (0,1)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-03-08  5:46:17

REVOKE ALL PRIVILEGES ON catgle.* FROM catgle;
GRANT INSERT, SELECT, UPDATE, DELETE, REFERENCES ON catgle.answer TO catgle;
GRANT INSERT, SELECT, UPDATE, DELETE, REFERENCES ON catgle.answer_voter TO catgle;
GRANT INSERT, SELECT, UPDATE, DELETE, REFERENCES ON catgle.chall TO catgle;
GRANT INSERT, SELECT, UPDATE, DELETE, REFERENCES ON catgle.question TO catgle;
GRANT INSERT, SELECT, UPDATE, DELETE, REFERENCES ON catgle.question_voter TO catgle;
GRANT INSERT, SELECT, UPDATE(participated) ON catgle.users TO catgle;
FLUSH privileges;