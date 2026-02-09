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
-- Table structure for table `faq`
--

DROP TABLE IF EXISTS `faq`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `faq` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `question` varchar(255) NOT NULL,
  `answer` longtext NOT NULL,
  `status` varchar(20) NOT NULL,
  `slug` varchar(255) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `published_at` datetime(6) DEFAULT NULL,
  `meta_title` varchar(255) NOT NULL,
  `meta_description` longtext NOT NULL,
  `display_order` int unsigned NOT NULL,
  `author_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`),
  KEY `faq_author_id_a6b8ef18_fk_bg_app_user_id` (`author_id`),
  CONSTRAINT `faq_author_id_a6b8ef18_fk_bg_app_user_id` FOREIGN KEY (`author_id`) REFERENCES `bg_app_user` (`id`),
  CONSTRAINT `faq_chk_1` CHECK ((`display_order` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faq`
--

LOCK TABLES `faq` WRITE;
/*!40000 ALTER TABLE `faq` DISABLE KEYS */;
INSERT INTO `faq` VALUES (1,'What areas in Dhangadhi do you serve?','<p><span style=\"color: rgb(108, 117, 125); font-family: &quot;Segoe UI&quot;, Tahoma, Geneva, Verdana, sans-serif; font-size: 14px;\">We provide IT services throughout Dhangadhi and surrounding areas in Sudurpaschim Province. Our team is available for on-site visits across the city and remote support for all locations.</span></p>','published','what-areas-in-dhangadhi-do-you-serve','2025-11-10 15:00:59.224405','2025-11-10 15:00:59.224486','2025-11-10 15:00:59.222958','What areas in Dhangadhi do you serve?','We provide IT services throughout Dhangadhi and surrounding areas in Sudurpaschim Province. Our team is available for on-site visits across the city and remote ...',1,1),(2,'What types of businesses do you work with?','<p><span style=\"color: rgb(108, 117, 125); font-family: &quot;Segoe UI&quot;, Tahoma, Geneva, Verdana, sans-serif; font-size: 14px;\">We serve businesses of all sizes across various sectors in Dhangadhi - from small local shops to educational institutions, healthcare facilities, and government offices. Our solutions are tailored to meet each client\'s specific needs.</span></p>','published','what-types-of-businesses-do-you-work-with','2025-11-10 15:01:29.177448','2025-11-10 15:01:29.177465','2025-11-10 15:01:29.177273','What types of businesses do you work with?','We serve businesses of all sizes across various sectors in Dhangadhi - from small local shops to educational institutions, healthcare facilities, and government...',2,1),(3,'Do you provide emergency IT support?','<p><span style=\"color: rgb(108, 117, 125); font-family: &quot;Segoe UI&quot;, Tahoma, Geneva, Verdana, sans-serif; font-size: 14px;\">Yes, we offer 24/7 emergency IT support for critical issues. Our local team in Dhangadhi can respond quickly to urgent situations to minimize downtime for your business.</span></p>','published','do-you-provide-emergency-it-support','2025-11-10 15:13:24.178592','2025-11-10 15:13:24.178608','2025-11-10 15:13:24.178420','Do you provide emergency IT support?','Yes, we offer 24/7 emergency IT support for critical issues. Our local team in Dhangadhi can respond quickly to urgent situations to minimize downtime for your ...',3,1),(4,'How can I get started with your services?','<p><span style=\"color: rgb(108, 117, 125); font-family: &quot;Segoe UI&quot;, Tahoma, Geneva, Verdana, sans-serif; font-size: 14px;\">Getting started is easy! Simply contact us via phone, email, or visit our office in Dhangadhi. We\'ll schedule a free consultation to understand your requirements and propose the best IT solutions for your business.</span></p>','published','how-can-i-get-started-with-your-services','2025-11-10 15:14:12.634865','2025-11-10 15:14:12.634883','2025-11-10 15:14:12.634645','How can I get started with your services?','Getting started is easy! Simply contact us via phone, email, or visit our office in Dhangadhi. We\'ll schedule a free consultation to understand your requirement...',4,1);
/*!40000 ALTER TABLE `faq` ENABLE KEYS */;
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
