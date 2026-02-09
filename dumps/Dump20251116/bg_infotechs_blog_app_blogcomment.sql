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
-- Table structure for table `blog_app_blogcomment`
--

DROP TABLE IF EXISTS `blog_app_blogcomment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `blog_app_blogcomment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `comment` longtext NOT NULL,
  `status` varchar(10) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `blog_id` bigint NOT NULL,
  `email` varchar(254) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `blog_app_bl_blog_id_eb17e0_idx` (`blog_id`,`status`,`created_at`),
  CONSTRAINT `blog_app_blogcomment_blog_id_9d3d8cbe_fk_blog_app_blog_id` FOREIGN KEY (`blog_id`) REFERENCES `blog_app_blog` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blog_app_blogcomment`
--

LOCK TABLES `blog_app_blogcomment` WRITE;
/*!40000 ALTER TABLE `blog_app_blogcomment` DISABLE KEYS */;
INSERT INTO `blog_app_blogcomment` VALUES (2,'wow very nice blog','approved','2025-10-29 06:56:26.061043','2025-10-29 06:57:13.512304',2,'chaudharynishan314@gmail.com','nishan'),(3,'very nice article','approved','2025-10-29 09:30:12.949157','2025-10-29 09:31:08.339538',2,'nishan@gmail.com','Nishan Chaudhary'),(5,'very nice article','approved','2025-10-29 10:08:13.382543','2025-10-29 10:09:36.700106',1,'chaudharynishan314@gmail.com','nishan'),(6,'very nice blog','rejected','2025-10-29 10:22:58.185274','2025-10-29 10:23:25.030039',1,'chaudharynishan314@gmail.com','nishan'),(7,'my favorite article site','pending','2025-10-31 00:04:09.328912','2025-10-31 00:04:09.328932',1,'chaudharynishan314@gmail.com','nishan'),(8,'wow?very nice blog.....','approved','2025-11-09 05:28:46.937091','2025-11-10 07:54:07.097784',3,'ram@gmail.com','Ram');
/*!40000 ALTER TABLE `blog_app_blogcomment` ENABLE KEYS */;
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
