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
-- Table structure for table `company_app_company_profile`
--

DROP TABLE IF EXISTS `company_app_company_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `company_app_company_profile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `company_name` varchar(100) NOT NULL,
  `company_email` varchar(254) NOT NULL,
  `company_phone` varchar(15) DEFAULT NULL,
  `company_address` varchar(100) DEFAULT NULL,
  `company_logo` varchar(100) DEFAULT NULL,
  `company_footer_logo` varchar(100) DEFAULT NULL,
  `company_favicon` varchar(100) DEFAULT NULL,
  `company_image` varchar(100) DEFAULT NULL,
  `company_intro` longtext,
  `company_mission` longtext,
  `company_vision` longtext,
  `company_footer` longtext,
  `map_iframe` longtext,
  `facebook_link` varchar(200) DEFAULT NULL,
  `instagram_link` varchar(200) DEFAULT NULL,
  `twitter_link` varchar(200) DEFAULT NULL,
  `youtube_link` varchar(200) DEFAULT NULL,
  `meta_title` varchar(100) DEFAULT NULL,
  `meta_description` longtext,
  `meta_keywords` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `company_app_company_profile`
--

LOCK TABLES `company_app_company_profile` WRITE;
/*!40000 ALTER TABLE `company_app_company_profile` DISABLE KEYS */;
INSERT INTO `company_app_company_profile` VALUES (1,'BG INFOTECHS','bginfotechs@gmail.com','9812345678','Dhangadhi','company_logos/Logo_a3JqJQ3.png','company_footer_logos/Logo.png','company_favicons/Logo1.png','company_images/collaborative-workspaces_U2tQA1g.jpg','None','None','None','At BG INFOTECHS, we specialize in crafting cutting-edge IT solutions tailored to meet the evolving needs of businesses. With a commitment to innovation and excellence, we empower organizations to thrive in the digital age.','None','https://facebook.com','https://instagram.com','https://x.com','https://youtube.com','bg infotechs','At BG INFOTECHS, we specialize in crafting cutting-edge IT solutions tailored to meet the evolving needs of businesses. With a commitment to innovation and excellence, we empower organizations to thrive in the digital age.','None');
/*!40000 ALTER TABLE `company_app_company_profile` ENABLE KEYS */;
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
