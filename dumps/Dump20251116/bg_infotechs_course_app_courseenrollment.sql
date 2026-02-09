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
-- Table structure for table `course_app_courseenrollment`
--

DROP TABLE IF EXISTS `course_app_courseenrollment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `course_app_courseenrollment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `address` longtext NOT NULL,
  `contact_number` varchar(20) NOT NULL,
  `education` varchar(20) DEFAULT NULL,
  `experience` varchar(20) DEFAULT NULL,
  `source` varchar(20) DEFAULT NULL,
  `enrolled_at` datetime(6) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `course_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `course_app_courseenrollment_course_id_b3ae9c00` (`course_id`),
  CONSTRAINT `course_app_courseenr_course_id_b3ae9c00_fk_course_ap` FOREIGN KEY (`course_id`) REFERENCES `course_app_course` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course_app_courseenrollment`
--

LOCK TABLES `course_app_courseenrollment` WRITE;
/*!40000 ALTER TABLE `course_app_courseenrollment` DISABLE KEYS */;
INSERT INTO `course_app_courseenrollment` VALUES (1,'Nishan','Chaudhary','chaudharynishan314@gmail.com','ghodaghodi-2\r\n','9824567890','high_school','none','friend','2025-10-28 09:39:35.551148',1,2),(5,'Aasth','Chaudhary','castha213@gmail.com','dhangadgi','9812345678','high_school','none','social_media','2025-10-31 16:03:55.244936',1,2);
/*!40000 ALTER TABLE `course_app_courseenrollment` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-16 11:39:47
