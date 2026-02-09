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
-- Table structure for table `contact_app_branch`
--

DROP TABLE IF EXISTS `contact_app_branch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contact_app_branch` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `maps` varchar(500) NOT NULL,
  `image` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  `address` varchar(500) NOT NULL,
  `phone` varchar(500) NOT NULL,
  `email` varchar(254) NOT NULL,
  `office_open` varchar(255) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `facebook` varchar(200) NOT NULL,
  `instagram` varchar(200) NOT NULL,
  `linkedin` varchar(200) NOT NULL,
  `twitter` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contact_app_branch`
--

LOCK TABLES `contact_app_branch` WRITE;
/*!40000 ALTER TABLE `contact_app_branch` DISABLE KEYS */;
INSERT INTO `contact_app_branch` VALUES (1,'Dhangadhi','https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3499.3332973650918!2d80.5805915740978!3d28.709583780580076!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xa13e527e18e84e77%3A0xb449ff1e9cf625a0!2sBG%20Infotechs!5e0!3m2!1sen!2snp!4v1762150935537!5m2!1sen!2snp','branch_img/collaborative-workspaces.jpg','<p>At BG INFOTECHS, we specialize in crafting cutting-edge IT solutions tailored to meet the evolving needs of businesses. With a commitment to innovation and excellence, we empower organizations to thrive in the digital age.</p>','Taranagar-05, Dhangadhi, Kailali, Nepal','+977 91 55555555','info@bginfotechs.com','Sunday - Friday: 9:00 AM - 6:00 PM',1,'https://www.facebook.com/','https://www.instagram.com/','https://www.linkedin.com/in/nishan-kumar-chaudhary-85428b313/','https://www.x.com/'),(2,'Kathmandu','https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d7064.722009068484!2d85.329979!3d27.706138!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x39eb190a74aa1f23%3A0x74ebef82ad0e5c15!2sSoftwarica%20College%20of%20IT%20and%20E-Commerce!5e0!3m2!1sen!2snp!4v1762151250256!5m2!1sen!2snp','branch_img/diverse-people-working-office_53.jpg','<p>At BG INFOTECHS, we specialize in crafting cutting-edge IT solutions tailored to meet the evolving needs of businesses. With a commitment to innovation and excellence, we empower organizations to thrive in the digital age.</p>','Chabahil, Kathmandu, Nepal','+977 1 4555555','kathmandu@bginfotechs.com','Sunday - Friday: 10:00 AM - 7:00 PM',1,'https://www.facebook.com/','https://www.instagram.com/','https://www.linkedin.com/in/nishan-kumar-chaudhary-85428b313/','https://www.x.com/');
/*!40000 ALTER TABLE `contact_app_branch` ENABLE KEYS */;
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
