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
-- Table structure for table `bg_app_user`
--

DROP TABLE IF EXISTS `bg_app_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bg_app_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `profile_picture` varchar(100) DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `address` longtext,
  `last_login_ip` char(39) DEFAULT NULL,
  `login_count` int unsigned NOT NULL,
  `role_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `bg_app_user_role_id_423ec085_fk_bg_app_role_id` (`role_id`),
  CONSTRAINT `bg_app_user_role_id_423ec085_fk_bg_app_role_id` FOREIGN KEY (`role_id`) REFERENCES `bg_app_role` (`id`),
  CONSTRAINT `bg_app_user_chk_1` CHECK ((`login_count` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bg_app_user`
--

LOCK TABLES `bg_app_user` WRITE;
/*!40000 ALTER TABLE `bg_app_user` DISABLE KEYS */;
INSERT INTO `bg_app_user` VALUES (1,'pbkdf2_sha256$1000000$vk2UV7Yl1XccH56a0PEKpU$cfYQq6djet2+nq3m5/lEe9savnrDaGEEBfcXLPe/S7Q=','2025-11-16 04:12:58.204813',1,'nishan','Nishan','Chaudhary','chaudharynishan314@gmail.com',1,1,'2025-10-27 02:55:52.000000','profiles/profile.png',1,'9824567890','dhangadgi',NULL,21,2),(2,'pbkdf2_sha256$1000000$aR0ZA5s30tVuauEwhX5nii$zbQtx2JHGtmfwKVWQfq2lPN8Yj0fNTwh3O5GZT9afy0=','2025-11-14 06:46:18.551642',0,'ram','Ram','Rana','ram@gmail.com',0,1,'2025-10-27 03:03:12.496229','profiles/profile_pic_j0TbtxB.png',1,'9812345678','Dhangadhi',NULL,7,1),(3,'pbkdf2_sha256$1000000$SUITWHEf0gkdhj9guTFBAo$Nx/07S069GM4BnJjnJ++Csxiyl52MBlG6qU9Q5NI6Ws=',NULL,0,'binod','Binod','Joshi','binod@gmail.com',0,1,'2025-10-27 03:08:14.693015','profiles/cat_eYMbgsx.jpg',1,'9812345678','Dhangadhi',NULL,0,3);
/*!40000 ALTER TABLE `bg_app_user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-16 11:39:48
