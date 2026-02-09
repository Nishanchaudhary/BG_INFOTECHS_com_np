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
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `slug` varchar(255) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `description` longtext,
  `status` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `ordering` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`),
  UNIQUE KEY `slug` (`slug`),
  CONSTRAINT `categories_chk_1` CHECK ((`ordering` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (1,'Full Stack Web Development','full-stack-web-development','category/images/2025/10/29/course_1728383943.jpg','<p>Full Stack Web Development refers to the process of designing, building, and maintaining both the front-end (client side) and back-end (server side) of a web application.</p><p><br></p><p>The front-end involves everything users see and interact with, built using technologies like HTML, CSS, and JavaScript along with frameworks such as React, Angular, or Vue.js.</p><p><br></p><p>The back-end handles server logic, databases, and application architecture, using languages and frameworks like Node.js, Express, Python (Django/Flask), Java (Spring Boot), or PHP (Laravel).</p><p><br></p><p>Databases (SQL or NoSQL) like MySQL, MongoDB, or PostgreSQL store and manage data.</p><p><br></p><p>A Full Stack Developer is skilled in both areas, capable of creating complete, functional web applications from start to finish.</p>',1,'2025-10-29 10:29:24.405710','2025-10-29 10:29:24.405923',1),(2,'Branding','branding','category/images/2025/10/30/branding-word-concepts-banner-ad.jpg','<p>Branding is the process of creating a unique identity for a business or product through elements like name, logo, design, and messaging. It shapes how people perceive and connect with the brand, building recognition, trust, and loyalty over time.</p>',1,'2025-10-30 04:19:53.717860','2025-10-30 04:32:51.498492',2),(3,'Packaging','packaging','category/images/2025/10/30/p_images.jpg','<p>Packaging is the design and production of containers or wrappers for products. It protects the item, provides important information, and plays a key role in attracting customers and communicating the brand’s identity.</p>',1,'2025-10-30 04:24:49.868973','2025-10-30 04:24:49.869008',3),(4,'Web Design','web-design','category/images/2025/10/30/landing-page-template-with-isome.jpg','<p>Web Design is the process of creating and organizing the visual layout, content, and functionality of websites. It focuses on user experience, aesthetics, and usability to ensure sites are both attractive and easy to navigate</p>',1,'2025-10-30 04:29:02.516273','2025-10-30 04:29:02.516303',4),(5,'Social Media','social-media','category/images/2025/10/30/social-media-marketing-concept-f.jpg','<p>Social Media refers to online platforms and apps that allow people and businesses to create, share, and interact with content, building connections and engaging with audiences worldwide.</p>',1,'2025-10-30 04:32:24.195775','2025-10-30 04:32:24.195807',5),(6,'Print Design','print-design','category/images/2025/10/30/printing-vector-banner-design-co.jpg','<p>Print Design is the creation of visual materials for printed media, such as brochures, posters, business cards, and packaging. It combines layout, typography, and imagery to communicate messages effectively in physical form.</p>',1,'2025-10-30 04:37:56.041561','2025-10-30 04:37:56.041595',6),(7,'SEO','seo','category/images/2025/11/02/SEO-services-in-Fayetteville-NC.jpg','<p>SEO (Search Engine Optimization) is the practice of optimizing a website or online content to rank higher in search engine results pages (SERPs). By improving factors like keyword usage, content quality, site structure, and backlinks, SEO helps increase visibility, drive organic traffic, and enhance user experience. The goal is to make a website more accessible and relevant to both search engines and users.</p>',1,'2025-11-02 05:44:53.926356','2025-11-02 05:44:53.926395',7),(8,'Android Apps','android-app','category/images/2025/11/04/android-app-development-mobile.jpg','<p>Android App — A mobile application designed for Android devices, offering seamless performance, user-friendly interfaces, and access to powerful features through the Android ecosystem.</p>',1,'2025-11-04 10:37:25.159167','2025-11-04 10:42:48.713631',8),(9,'iOS Apps','ios-apps','category/images/2025/11/04/ios.jpg','<p>iOS Apps — Mobile applications built for Apple devices, delivering smooth performance, intuitive design, and a secure user experience within the iOS ecosystem.</p>',1,'2025-11-04 10:42:31.934596','2025-11-04 10:42:31.934639',9),(10,'React Native Apps','react-native-apps','category/images/2025/11/04/react-native-mobile-apps-develop.jpg','<p>React Native — A cross-platform framework for building mobile apps using JavaScript and React, enabling fast development for both Android and iOS from a single codebase.</p>',1,'2025-11-04 10:46:40.737357','2025-11-04 10:46:40.737401',10),(11,'Flutter App','flutter-app','category/images/2025/11/04/Applications-Built-with-Flutter.jpg','<p>Flutter — An open-source UI toolkit by Google for building fast, beautiful, and natively compiled applications for mobile, web, and desktop from a single codebase.</p>',1,'2025-11-04 10:49:31.670158','2025-11-04 10:49:31.670191',12);
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
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
