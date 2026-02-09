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
-- Table structure for table `vacancy_app_jobapplication`
--

DROP TABLE IF EXISTS `vacancy_app_jobapplication`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vacancy_app_jobapplication` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `full_name` varchar(100) NOT NULL,
  `email` varchar(254) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `cover_letter` longtext NOT NULL,
  `resume` varchar(100) NOT NULL,
  `status` varchar(10) NOT NULL,
  `applied_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `vacancy_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `vacancy_app_jobapplication_vacancy_id_email_dc83125e_uniq` (`vacancy_id`,`email`),
  CONSTRAINT `vacancy_app_jobappli_vacancy_id_ea20d79c_fk_vacancy_a` FOREIGN KEY (`vacancy_id`) REFERENCES `vacancy_app_vacancy` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vacancy_app_jobapplication`
--

LOCK TABLES `vacancy_app_jobapplication` WRITE;
/*!40000 ALTER TABLE `vacancy_app_jobapplication` DISABLE KEYS */;
INSERT INTO `vacancy_app_jobapplication` VALUES (1,'Nishan Chaudhary','chaudharynishan314@gmail.com','9824567890','this is testing','resumes/Nishan_Chaudhary_Btuuecv.pdf','accepted','2025-10-28 01:00:26.217626','2025-11-06 11:02:40.471687',1),(2,'Nishan Chaudhary','chaudharynishan314@gmail.com','9824567890','this is testing message','resumes/Nishan_Chaudhary_UiQkPff.pdf','accepted','2025-11-06 11:47:45.938960','2025-11-10 11:13:14.519583',2),(3,'Babin chaudhary','www.bobeenchy7@gmail.com','9824567890','test','resumes/Nishan_Chaudhary_wrzGRrD.pdf','pending','2025-11-10 11:06:23.769326','2025-11-10 14:35:06.941060',2);
/*!40000 ALTER TABLE `vacancy_app_jobapplication` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-16 11:39:49
