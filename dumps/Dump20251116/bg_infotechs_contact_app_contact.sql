-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: bg_infotechs
-- ------------------------------------------------------
-- Server version	8.0.43

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
-- Table structure for table `contact_app_contact`
--

DROP TABLE IF EXISTS `contact_app_contact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contact_app_contact` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `full_name` varchar(100) NOT NULL,
  `email` varchar(254) NOT NULL,
  `phone_number` varchar(20) NOT NULL,
  `message` longtext NOT NULL,
  `status` tinyint(1) NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `service_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `contact_app_contact_service_id_69b33cd0_fk_company_a` (`service_id`),
  KEY `contact_app_status_04e919_idx` (`status`),
  KEY `contact_app_is_read_16d71b_idx` (`is_read`),
  KEY `contact_app_created_2e698f_idx` (`created_at`),
  CONSTRAINT `contact_app_contact_service_id_69b33cd0_fk_company_a` FOREIGN KEY (`service_id`) REFERENCES `company_app_services` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contact_app_contact`
--

LOCK TABLES `contact_app_contact` WRITE;
/*!40000 ALTER TABLE `contact_app_contact` DISABLE KEYS */;
INSERT INTO `contact_app_contact` VALUES (1,'Nishan Chaudhary','chaudharynishan314@gmail.com','9824567890','this is testing message',1,0,'2025-11-03 10:29:59.348796','2025-11-03 10:29:59.348842',3),(2,'Nishan Chaudhary','chaudharynishan314@gmail.com','9824567890','this is testing message',1,1,'2025-11-03 10:32:59.384273','2025-11-03 10:32:59.384305',3),(3,'Nishan Chaudhary','chaudharynishan314@gmail.com','+9779824567890','this is testing messages......',1,1,'2025-11-03 10:47:20.136773','2025-11-03 10:47:20.136802',3);
/*!40000 ALTER TABLE `contact_app_contact` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-16 11:39:46
