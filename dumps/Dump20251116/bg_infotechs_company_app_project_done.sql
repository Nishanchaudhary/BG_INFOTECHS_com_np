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
-- Table structure for table `company_app_project_done`
--

DROP TABLE IF EXISTS `company_app_project_done`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `company_app_project_done` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(50) NOT NULL,
  `image` varchar(100) NOT NULL,
  `company` varchar(50) NOT NULL,
  `logo` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  `live_link` varchar(200) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `service_id` bigint NOT NULL,
  `category_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `company_app_project__service_id_ef8642a7_fk_company_a` (`service_id`),
  KEY `company_app_project_done_category_id_57262f6b_fk_categories_id` (`category_id`),
  CONSTRAINT `company_app_project__service_id_ef8642a7_fk_company_a` FOREIGN KEY (`service_id`) REFERENCES `company_app_services` (`id`),
  CONSTRAINT `company_app_project_done_category_id_57262f6b_fk_categories_id` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `company_app_project_done`
--

LOCK TABLES `company_app_project_done` WRITE;
/*!40000 ALTER TABLE `company_app_project_done` DISABLE KEYS */;
INSERT INTO `company_app_project_done` VALUES (1,'BG infotechs','project_done/Screenshot_95.png','BG infotechs','company_logo/Logo1_jo9Xz4O.png','BG Infotechs is a Nepal-based software and digital solutions company, with its head office located in Dhangadhi and a branch in Kathmandu.','https://bginfotechs.com.np/','2025-10-29 11:04:09.019966','2025-10-29 11:04:09.020038',1,3,1),(2,'Python Django BG project','project_done/Screenshot_95_rJvKhl0.png','BG infotechs','company_logo/Logo.png','BG Infotechs is a Nepal-based software and digital solutions company, with its head office located in Dhangadhi and a branch in Kathmandu.','https://bginfotechs.com/','2025-10-29 11:24:22.454331','2025-10-31 10:28:16.867081',1,3,1),(3,'EV Fast Charging','project_done/electric-car_23-2148004726.jpg','EV Fast','company_logo/evfast_logo.jpg','**EV Fast** refers to **Electric Vehicle Fast Charging**, a technology that rapidly recharges electric car batteries using high-power chargers—typically delivering 50 kW to 350 kW or more.','','2025-10-30 05:13:19.218141','2025-11-01 04:53:19.751801',1,1,5),(4,'UI /UX Design','project_done/5809245.jpg','BG infotechs','company_logo/Logo1_LrjkAnd.png','At GB Infotechs, we create intuitive, engaging, and visually stunning digital experiences that connect businesses with their audiences. Our UI/UX Design services focus on understanding your users’ needs and translating them into seamless, easy-to-navigate interfaces.','','2025-10-30 09:44:31.333009','2025-10-30 13:53:54.851443',1,1,4),(5,'social media marketing','project_done/Real-Estate-Social-Network-e1646.jpg','ABCD info tech','company_logo/abc-logo-abc-letter-abc-letter-l.png','Social Media Marketing is the use of social media platforms—such as Facebook, Instagram, X (Twitter), LinkedIn, and TikTok—to promote products, services, or brands. It involves creating and sharing content, engaging with audiences, running paid ads, and analyzing performance to build brand awareness, drive traffic, and increase sales.','https://abcd.com/','2025-11-02 05:32:10.403118','2025-11-02 05:56:10.900628',1,2,5),(6,'Search engine optimization','project_done/digital_marketing.jpg','XYZ infotech','company_logo/xyz_logo.png','SEO in Digital Marketing refers to the strategies and techniques used to improve a website’s visibility in search engine results as part of a broader digital marketing plan. It focuses on optimizing website content, structure, and performance to attract organic (non-paid) traffic. Effective SEO helps businesses reach target audiences, build credibility, and increase conversions by ensuring their online presence ranks high for relevant keywords and search queries.','https://xyz.com/','2025-11-02 05:53:08.263426','2025-11-02 05:53:08.263450',1,2,7),(7,'Employee management app','project_done/Employee_management_app.jpg','Employee management app','company_logo/logo.jpg','**Employee Management App** — A digital solution to manage employee data, attendance, payroll, and performance efficiently from one centralized platform.','https://bginfotechs.com.np/','2025-11-04 11:00:01.583667','2025-11-04 11:00:01.583702',1,4,8),(8,'Hospital Management App','project_done/medical-booking-app-concept_23-2.jpg','ABCD Hospital PVT LTD','company_logo/hospital-logo-design-vector-medi.png','Hospital Management App — A comprehensive system for managing patients, staff, appointments, billing, and medical records efficiently in one platform.','https://abcd.com/','2025-11-04 11:08:56.068342','2025-11-04 11:08:56.070324',1,4,9),(9,'School Management App','project_done/school_management_app.jpg','XYZ secondary school','company_logo/School_Management_App.png','School Management App — A digital platform to manage students, teachers, classes, attendance, exams, and communication efficiently in one place.','https://xyz.com/','2025-11-04 11:24:40.905515','2025-11-04 11:24:40.905537',1,4,11),(10,'SEO project','project_done/seo_images.jpg','NGO Company','company_logo/company-logo-png_seeklogo-389186.png','Improve website visibility and ranking on search engines through optimized SEO strategies and analytics.','https://ngo.com/','2025-11-05 05:19:51.674920','2025-11-05 05:19:51.674957',1,6,7),(11,'Facebook Page Boost','project_done/facebook_page_like_boost.png','A2Z','company_logo/facebook_page_boost.png','Enhance your brand visibility and reach more audiences with targeted Facebook Page Boost campaigns.','http://AtoZ.com','2025-11-13 09:23:13.678567','2025-11-13 09:23:13.678630',1,5,7);
/*!40000 ALTER TABLE `company_app_project_done` ENABLE KEYS */;
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
