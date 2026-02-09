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
-- Table structure for table `company_app_services_testimonial`
--

DROP TABLE IF EXISTS `company_app_services_testimonial`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `company_app_services_testimonial` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `designation` varchar(100) DEFAULT NULL,
  `image` varchar(100) DEFAULT NULL,
  `message` longtext NOT NULL,
  `rating` int unsigned NOT NULL,
  `status` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `service_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `company_app_service_56df01_idx` (`service_id`,`status`),
  KEY `company_app_rating_2408ed_idx` (`rating`),
  CONSTRAINT `company_app_services_service_id_b8c6c6f7_fk_company_a` FOREIGN KEY (`service_id`) REFERENCES `company_app_services` (`id`),
  CONSTRAINT `company_app_services_testimonial_chk_1` CHECK ((`rating` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `company_app_services_testimonial`
--

LOCK TABLES `company_app_services_testimonial` WRITE;
/*!40000 ALTER TABLE `company_app_services_testimonial` DISABLE KEYS */;
INSERT INTO `company_app_services_testimonial` VALUES (1,'Sarah Johnson','CEO, Bloom Cosmetics','services_testimonials/2025/10/30/32.jpg','The branding package BG Designs created for us perfectly captured our company\'s essence. Our sales increased by 40% after the rebrand!',4,1,'2025-10-30 06:53:14.587870','2025-10-30 06:53:41.988193',1),(2,'Michael Chen','Founder, TechNova','services_testimonials/2025/10/30/45.jpg','Their UI/UX design transformed our app\'s user engagement. The attention to detail and user-centric approach was exceptional',5,1,'2025-10-30 06:56:25.491580','2025-10-30 06:56:25.491640',1),(3,'Sarah Johnson...','CEO, TechStart','services_testimonials/2025/11/04/images1.png','BuzzPulse took our Instagram from 500 to 50,000 followers in just 6 months. The engagement is through the roof and we\'re closing deals directly from DMs!',5,1,'2025-11-04 04:38:29.489532','2025-11-04 05:10:23.489527',2),(6,'Michael Chen','Marketing Director, StyleHub','services_testimonials/2025/11/04/portrait-confident-young-busines_CZG9oGP.jpg','Our TikTok went viral with over 2 million views on a single video. BuzzPulse understands the algorithm better than anyone we\'ve worked with before.',5,1,'2025-11-04 05:06:53.229295','2025-11-04 05:06:53.229327',2),(7,'David Rodriguez','Founder, FitnessFuel','services_testimonials/2025/11/04/young-man-very-smiley-during-260.jpg','The Facebook ad strategy BuzzPulse implemented dropped our cost per acquisition by 68%. They\'ve become an extension of our marketing team.',5,1,'2025-11-04 05:09:50.019481','2025-11-04 05:09:50.019510',2),(8,'Sarah Johnson','CEO, TechStart','services_testimonials/2025/11/04/images1_tuL1W37.png','BuzzPulse took our Instagram from 500 to 50,000 followers in just 6 months. The engagement is through the roof and we\'re closing deals directly from DMs!',5,1,'2025-11-04 07:02:43.131707','2025-11-04 07:02:43.131733',5),(9,'Michael Chen','Marketing Director, StyleHub','services_testimonials/2025/11/04/portrait-confident-young-busines.jpg','Our TikTok went viral with over 2 million views on a single video. BuzzPulse understands the algorithm better than anyone we\'ve worked with before.',5,1,'2025-11-04 07:13:48.510929','2025-11-04 07:13:48.510958',5),(10,'David Rodriguez','Founder, FitnessFuel','services_testimonials/2025/11/04/young-man-very-smiley-during-260_YsvA7gf.jpg','The Facebook ad strategy BuzzPulse implemented dropped our cost per acquisition by 68%. They\'ve become an extension of our marketing team.',5,1,'2025-11-04 07:16:12.899812','2025-11-04 07:16:12.899841',5),(11,'Sarah Johnson','Technical Director','services_testimonials/2025/11/05/images1.png','Everything seems to be working good. Of course, I want to get everything moved as far back as possible on the internet. I have had several people go out and search for negative information, and they couldn’t pull up anything. Thanks again!',5,1,'2025-11-05 05:47:22.670631','2025-11-05 05:47:22.670674',6),(12,'Aarav Sharma','CEO, BrightTech Solutions','services_testimonials/2025/11/13/profile1.png','The team delivered our website exactly how we envisioned it. Their attention to detail, responsiveness, and technical expertise made the whole process smooth. Highly recommend their web development services!',5,1,'2025-11-13 06:08:38.377972','2025-11-13 06:08:38.378054',3),(13,'Priya Singh','Founder, UrbanStyle Boutique','services_testimonials/2025/11/13/profile2.png','I was amazed by how quickly they understood my business needs and turned them into a modern, user-friendly website. Excellent design sense and top-notch coding skills!',5,1,'2025-11-13 06:10:04.848267','2025-11-13 06:10:04.848325',3),(14,'Sneha Koirala','Marketing Head, Vision Plus Media','services_testimonials/2025/11/13/profile3.png','Working with them was effortless. They communicated clearly, delivered on time, and provided valuable suggestions to improve our website.',5,1,'2025-11-13 06:13:31.826724','2025-11-13 06:13:31.826768',3),(15,'Sanjay Thapa','Founder, RideNow App','services_testimonials/2025/11/13/profile1_udCbWdX.png','BG-Infotechs built our mobile app exactly the way we wanted. The design is clean, the performance is fast, and the user experience is outstanding. Their team was supportive from day one.',5,1,'2025-11-13 06:55:03.734692','2025-11-13 06:55:03.734792',4),(16,'Anita Sharma','CEO, Foodiez Nepal','services_testimonials/2025/11/13/profile2_zdoemkt.png','We had a great experience with BG-Infotechs. They handled everything — from planning to publishing our app on the Play Store and App Store. The communication was clear and the delivery was on time.',5,1,'2025-11-13 06:57:28.330059','2025-11-13 06:57:28.330114',4),(17,'Divyanshi','Founder, Ecom Fashion','services_testimonials/2025/11/14/profile3.png','As a small business, we were struggling to stand out online. Their data-driven SEO strategy and attention to detail were game-changers. Not only did our site traffic increase significantly, but conversion rates also improved substantially.',5,1,'2025-11-14 05:06:16.541342','2025-11-14 05:06:16.541366',6);
/*!40000 ALTER TABLE `company_app_services_testimonial` ENABLE KEYS */;
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
