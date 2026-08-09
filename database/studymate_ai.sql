CREATE DATABASE  IF NOT EXISTS `studymate_ai` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `studymate_ai`;
-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: studymate_ai
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `documents`
--

DROP TABLE IF EXISTS `documents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `documents` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `file_name` varchar(255) NOT NULL,
  `file_type` varchar(20) NOT NULL,
  `summary` longtext,
  `upload_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `documents_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `documents`
--

LOCK TABLES `documents` WRITE;
/*!40000 ALTER TABLE `documents` DISABLE KEYS */;
INSERT INTO `documents` VALUES (1,1,'python_notes.pdf','pdf','Introduction to Python','2026-08-01 10:37:23'),(2,1,'python_notes.pdf','pdf','Introduction to Python programming.','2026-08-01 10:52:16'),(3,1,'python_notes.pdf','pdf','Introduction to Python programming.','2026-08-01 11:18:02');
/*!40000 ALTER TABLE `documents` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exam_questions`
--

DROP TABLE IF EXISTS `exam_questions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `exam_questions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `document_id` int NOT NULL,
  `question` text NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `document_id` (`document_id`),
  CONSTRAINT `exam_questions_ibfk_1` FOREIGN KEY (`document_id`) REFERENCES `documents` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exam_questions`
--

LOCK TABLES `exam_questions` WRITE;
/*!40000 ALTER TABLE `exam_questions` DISABLE KEYS */;
/*!40000 ALTER TABLE `exam_questions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `study_notes`
--

DROP TABLE IF EXISTS `study_notes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `study_notes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `document_id` int NOT NULL,
  `notes` longtext,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `document_id` (`document_id`),
  CONSTRAINT `study_notes_ibfk_1` FOREIGN KEY (`document_id`) REFERENCES `documents` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `study_notes`
--

LOCK TABLES `study_notes` WRITE;
/*!40000 ALTER TABLE `study_notes` DISABLE KEYS */;
INSERT INTO `study_notes` VALUES (2,1,'This is my first study note.','2026-08-01 10:39:43');
/*!40000 ALTER TABLE `study_notes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `full_name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Srushti patel','srushti@gmail.com','12345','2026-08-01 10:13:12'),(2,'srushti patel','srushtikpatel812@gmail.com','1234567890','2026-08-04 15:40:27'),(3,'pinal thakor','pinalt@gmail.com','280604','2026-08-04 15:56:00'),(4,'hency patel','hency06@gmail.com','hency0610','2026-08-05 07:03:49'),(5,'Prachi Sangdot','prachi@gmail.com','scrypt:32768:8:1$rGJCTauUDN2JW2Jp$3f20a3311e8d405d3e74e90ecfa00d16476803a4ca6ba9918dfd6e71665316ac79cf1fe2575320ab7abbba720b4a02ce99933bb58117641de073f8df5b7c7311','2026-08-06 15:03:43'),(6,'Kiyan patel','kiyan@gmail.com','scrypt:32768:8:1$ttnSHIIMze4RBLGQ$77edb99fb4522906cc4833059ab1b0ffb0c120a4ba0b8d4809a4e836df9393333aa5ddcf8a80aac3dbc81005b7335e7e26257c2f82eb167559991aff41c8f44f','2026-08-06 16:32:04'),(7,'Meghana Patel','meghana@gmail.com','scrypt:32768:8:1$zdrjTXyqcJIVEUJr$7133eb37b306791beb84f1cbb0b5adbefeb99d9f44e90166299bd77bff2216a7ce79fba544f621ac09eb5dc541fb24d91ee6063fadc38cc90c9d9a621f282e7c','2026-08-07 13:43:44'),(8,'Dhruvi Patel','dhruvi@gmail.com','scrypt:32768:8:1$1IxyhmwmRahosrl5$d0de55a05c3d0f0e4bd0d02a3555e9a9e9547be963f06bbb5a9c8fe72a685a49a3bf7bb2cee50693899c9c544f0e8dfe9c22ffb5d2de4a336a5f2f7e34786a09','2026-08-08 08:24:50');
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

-- Dump completed on 2026-08-08 22:04:29
