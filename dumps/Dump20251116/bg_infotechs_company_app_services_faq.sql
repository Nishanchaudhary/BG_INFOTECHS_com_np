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
-- Table structure for table `company_app_services_faq`
--

DROP TABLE IF EXISTS `company_app_services_faq`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `company_app_services_faq` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `question` varchar(255) NOT NULL,
  `answer` longtext NOT NULL,
  `status` varchar(20) NOT NULL,
  `slug` varchar(255) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `service_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`),
  KEY `company_app_services_service_id_35c0741d_fk_company_a` (`service_id`),
  CONSTRAINT `company_app_services_service_id_35c0741d_fk_company_a` FOREIGN KEY (`service_id`) REFERENCES `company_app_services` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `company_app_services_faq`
--

LOCK TABLES `company_app_services_faq` WRITE;
/*!40000 ALTER TABLE `company_app_services_faq` DISABLE KEYS */;
INSERT INTO `company_app_services_faq` VALUES (1,'How long does it take to create a design?','The timeline for creating a design depends on the complexity and scope of the project. Simple designs can take anywhere from 1–3 business days, while more detailed or customized projects may take up to 1–2 weeks. We’ll provide you with an estimated delivery time after discussing your requirements and project details.','published','how-long-does-it-take-to-develop-a-website','2025-10-30 08:26:55.530208','2025-10-30 08:26:55.530246',1),(2,'What information do you need to start the design?','We’ll need details such as your project goals, target audience, preferred style or theme, and any specific colors, images, or text you’d like included. The more information you provide, the better we can capture your vision.','published','what-information-do-you-need-to-start-the-design','2025-10-30 08:35:47.061895','2025-10-30 08:35:47.061915',1),(3,'Can I request revisions to my design?','Yes! We offer a set number of revisions depending on your package. Our goal is to make sure you’re completely satisfied with the final result, so we’ll work with your feedback to refine the design.','published','can-i-request-revisions-to-my-design','2025-10-30 08:39:15.567181','2025-10-30 08:45:05.929560',1),(4,'Do you offer rush or urgent design services?','Yes, we can accommodate tight deadlines for an additional fee. Please let us know your timeline in advance so we can prioritize your project accordingly.','published','do-you-offer-rush-or-urgent-design-services','2025-10-30 08:46:24.789037','2025-10-30 08:50:52.677957',1),(5,'What if I don’t know exactly what I want?','No problem! Our team can help you develop ideas and provide design concepts based on your brand identity, industry, and preferences. We’ll guide you through each step to create something you love.','published','what-if-i-dont-know-exactly-what-i-want','2025-10-30 09:08:19.706593','2025-10-30 09:08:31.355973',1),(6,'What\'s included in your social media handling packages?','Our packages include creative graphic design, page management, content creation, festival/birthday posts, profile/cover images, monthly reporting, and 24/7 support. Higher-tier packages include additional features like ads videos and ad boosting.','published','whats-included-in-your-social-media-handling-packa','2025-11-02 08:28:20.467779','2025-11-02 08:28:20.467801',2),(7,'Can I customize my social media package?','Yes, we offer customizable solutions. You can start with one of our standard packages (Silver, Gold, Platinum, or Diamond) and add specific services as needed. Fill out our custom package form to discuss your requirements.','published','can-i-customize-my-social-media-package','2025-11-02 08:29:08.018422','2025-11-02 08:29:08.018453',2),(8,'What\'s the difference between the Silver and Diamond packages?','The Silver package includes 14 creative designs and basic management, while the Diamond package offers 30 designs, monthly calendars, 4 Reels/GIFs per month, 2 ads videos, and $10 ad boosting. The Diamond package provides comprehensive services for businesses needing full-scale social media management.','published','whats-the-difference-between-the-silver-and-diamon','2025-11-02 08:29:47.109786','2025-11-02 08:29:47.109817',2),(9,'Do you offer ad boosting services?','Yes, we offer ad boosting services. Our Platinum package includes $5 boosting and Diamond includes $10 boosting. Additional boosting services are available separately - please contact us for details.','published','do-you-offer-ad-boosting-services','2025-11-02 08:30:31.501277','2025-11-02 08:30:31.501298',2),(10,'How do I choose the right package for my business?','Consider your business size, social media goals, and budget. Small businesses may start with Silver or Gold, while established brands typically benefit from Platinum or Diamond. Our team can help assess your needs and recommend the best package during a free consultation.','published','how-do-i-choose-the-right-package-for-my-business','2025-11-02 08:31:16.792911','2025-11-02 08:31:16.792936',2),(11,'How do I choose the right package for my business?','Consider your business size, social media goals, and budget. Small businesses may start with Silver or Gold, while established brands typically benefit from Platinum or Diamond. Our team can help assess your needs and recommend the best package during a free consultation.','published','how-do-my-business','2025-11-05 07:43:18.066188','2025-11-05 07:43:18.066211',6),(12,'What types of websites do you develop?','We build all kinds of websites — from simple portfolio or business sites to advanced e-commerce platforms, booking systems, and custom web applications. Each project is tailored to fit your goals and budget.','published','what-types-of-websites-do-you-develop','2025-11-13 06:15:58.220482','2025-11-13 06:15:58.220553',3),(13,'How much does a new website cost?','Website pricing varies depending on features, design complexity, and content. We offer custom packages to match your needs and budget. Contact us for a free quote.','published','how-much-does-a-new-website-cost','2025-11-13 06:19:09.308275','2025-11-13 06:19:09.308318',3),(14,'Do you offer website maintenance and support?','Yes, we offer ongoing maintenance plans to keep your site secure, up-to-date, and running smoothly. We also provide technical support whenever you need it.','published','do-you-offer-website-maintenance-and-support','2025-11-13 06:19:54.446908','2025-11-13 06:20:50.144513',3),(15,'Will my website be optimized for search engines (SEO)?','Yes. All our websites are built with SEO best practices, including fast load times, clean code, and optimized structure to help your site rank better on Google.','published','will-my-website-be-optimized-for-search-engines-se','2025-11-13 06:20:40.146224','2025-11-13 06:20:40.146279',3),(16,'What types of mobile apps do you develop?','At BG-Infotechs, we develop all kinds of mobile applications — including Android, iOS, and cross-platform apps using technologies like Flutter and React Native. Whether you need a business app, e-commerce solution, or custom platform, we’ve got you covered.','published','what-types-of-mobile-apps-do-you-develop','2025-11-13 06:50:16.931523','2025-11-13 06:50:16.931559',4),(17,'How long does it take to build a mobile app?','Development time depends on the app’s complexity and features. A simple app may take 4–6 weeks, while a more advanced one with custom APIs or integrations could take 2–3 months. We’ll share a detailed timeline after analyzing your project.','published','how-long-does-it-take-to-build-a-mobile-app','2025-11-13 06:50:52.640160','2025-11-13 06:50:52.640195',4),(18,'How much does mobile app development cost?','Costs vary based on design, functionality, and platform. BG-Infotechs offers custom and affordable packages tailored to your business goals. Contact us for a free project quote.','published','how-much-does-mobile-app-development-cost','2025-11-13 06:51:22.927747','2025-11-13 06:52:52.499684',4),(19,'Do you develop apps for both Android and iOS?','Yes. We build native apps for both Android and iOS as well as cross-platform solutions that work seamlessly across all devices.','published','do-you-develop-apps-for-both-android-and-ios','2025-11-13 06:51:55.283116','2025-11-13 06:51:55.283151',4),(20,'Will my app have a modern and user-friendly design?','Absolutely! Our design team focuses on UI/UX excellence — ensuring your app is visually appealing, intuitive, and easy to use.','published','will-my-app-have-a-modern-and-user-friendly-design','2025-11-13 06:52:43.567332','2025-11-13 06:52:43.567365',4),(21,'What is Social Media Marketing (SMM)?','Social Media Marketing (SMM) is the process of using platforms like Facebook, Instagram, Twitter, LinkedIn, and TikTok to promote your brand, increase awareness, and drive traffic or sales.','published','what-is-social-media-marketing-smm','2025-11-13 09:27:53.747695','2025-11-13 09:27:53.747730',5),(22,'Why is social media marketing important for my business?','Social media marketing helps you connect directly with your audience, increase brand visibility, build trust, and generate leads. It’s one of the most cost-effective ways to grow your business online.','published','why-is-social-media-marketing-important-for-my-bus','2025-11-13 09:28:47.121640','2025-11-13 09:28:47.121695',5),(23,'What services are included in your social media marketing packages?','Our SMM packages include content creation, page management, paid ad campaigns, audience engagement, analytics tracking, and monthly performance reports.','published','what-services-are-included-in-your-social-media-ma','2025-11-13 09:29:34.355489','2025-11-13 09:29:34.355528',5),(24,'How often will you post on our social media pages?','The posting frequency depends on your plan and strategy — typically 3 to 7 times per week to maintain consistent engagement and visibility.','published','how-often-will-you-post-on-our-social-media-pages','2025-11-13 09:30:28.382179','2025-11-13 09:30:28.382227',5);
/*!40000 ALTER TABLE `company_app_services_faq` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-16 11:39:51
