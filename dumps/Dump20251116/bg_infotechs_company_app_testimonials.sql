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
-- Table structure for table `company_app_testimonials`
--

DROP TABLE IF EXISTS `company_app_testimonials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `company_app_testimonials` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `designation` varchar(100) DEFAULT NULL,
  `image` varchar(100) DEFAULT NULL,
  `message` longtext NOT NULL,
  `rating` int unsigned NOT NULL,
  `status` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `company_app_testimonials_chk_1` CHECK ((`rating` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `company_app_testimonials`
--

LOCK TABLES `company_app_testimonials` WRITE;
/*!40000 ALTER TABLE `company_app_testimonials` DISABLE KEYS */;
INSERT INTO `company_app_testimonials` VALUES (1,'Rajesh Chaudhary','Owner, Dhangadhi Fashion Store','testimonial_images/pngtree-smiling-man-posing-for-a-portrait-png-image_16420590.png','BG InfoTechs built our e-commerce website that doubled our sales within 3 months. Their team understood exactly what we needed as a local business and delivered beyond our expectations.',5,1),(2,'Sunita Thapa','Manager, Himalayan Brew Cafe','testimonial_images/portrait-of-beautiful-young-asia.jpg','<p>Our cafe\'s Instagram followers grew from 200 to 5,000+ in just 2 months with BG InfoTechs\' social media strategy. They helped us create content that really connects with local customers.</p>',5,1),(3,'Bikram Rana','Director, Far West Adventures','testimonial_images/businessman-isolated-illustratio.jpg','<p>Thanks to BG InfoTechs\' Google Ads campaigns, our tour company now gets 10+ quality inquiries daily. Their local market knowledge makes all the difference compared to big agencies.</p>',5,1),(4,'Anjali Bhandari','IT Student, Mahendra College','testimonial_images/cHJpdmF0ZS9sci9pbWFnZXMvd2Vic2l0.jpg','<p>After completing BG InfoTechs\' web development course, I landed my first freelance job within a week! The practical training gave me skills I couldn\'t get from college alone.</p>',5,1),(5,'Dr. Arjun Koirala','Medical Director, Seti Hospital','testimonial_images/pngtree-front-view-of-a-smiling.jpg','<p>Our hospital\'s appointment app developed by BG InfoTechs reduced patient wait times by 40%. Their team was always available to make adjustments as we needed.</p>',5,1),(6,'Bipana Rana','Director, Far West Adventures','testimonial_images/profile2.png','<p>Thanks to BG Infotechs’ Google Ads campaigns, our tour company now gets 10+ quality inquiries daily. Their local market knowledge makes all the difference compared to big agencies.</p>',5,1);
/*!40000 ALTER TABLE `company_app_testimonials` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-16 11:39:50
