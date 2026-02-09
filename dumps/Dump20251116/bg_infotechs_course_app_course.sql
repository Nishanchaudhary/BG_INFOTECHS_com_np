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
-- Table structure for table `course_app_course`
--

DROP TABLE IF EXISTS `course_app_course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `course_app_course` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `image` varchar(100) NOT NULL,
  `short_description` varchar(500) NOT NULL,
  `description` longtext NOT NULL,
  `duration` bigint NOT NULL,
  `price` int unsigned NOT NULL,
  `offer_price` int unsigned NOT NULL,
  `status` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `author_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `course_app_course_author_id_71083253_fk_bg_app_user_id` (`author_id`),
  CONSTRAINT `course_app_course_author_id_71083253_fk_bg_app_user_id` FOREIGN KEY (`author_id`) REFERENCES `bg_app_user` (`id`),
  CONSTRAINT `course_app_course_chk_1` CHECK ((`price` >= 0)),
  CONSTRAINT `course_app_course_chk_2` CHECK ((`offer_price` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course_app_course`
--

LOCK TABLES `course_app_course` WRITE;
/*!40000 ALTER TABLE `course_app_course` DISABLE KEYS */;
INSERT INTO `course_app_course` VALUES (1,'Front End Web Development','course_img/programming-courses-web-design-c.jpg','Enroll in our  Front End Web Development course to learn how to code with this popular server-side scripting language. Learn Front End Web Development basic concepts like variables, data types, control statements, loops, and functions through hands-on implementations.','<p style=\"margin-right: 0px; margin-bottom: 0px; margin-left: 0px; padding: 0px; font-size: 14.875px; max-inline-size: 118.4rem; color: oklch(0.2974 0.0362 281.74); font-family: &quot;Udemy Sans&quot;, Vazirmatn, &quot;SF Pro Text&quot;, -apple-system, BlinkMacSystemFont, Roboto, &quot;Segoe UI&quot;, Helvetica, Arial, sans-serif, &quot;Apple Color Emoji&quot;, &quot;Segoe UI Emoji&quot;, &quot;Segoe UI Symbol&quot;;\">Learning HTML and CSS doesn’t have to mean sitting through hours of dry theory or building full websites from scratch. In&nbsp;<strong style=\"margin: 0px; padding: 0px;\">Web Project Workshop: HTML &amp; CSS in Action</strong>, you’ll take a hands-on, beginner-friendly journey by creating fun, focused web projects that teach you real skills - fast.</p><p style=\"margin-right: 0px; margin-bottom: 0px; margin-left: 0px; padding: 0px; font-size: 14.875px; max-inline-size: 118.4rem; margin-block-start: 0.8rem; color: oklch(0.2974 0.0362 281.74); font-family: &quot;Udemy Sans&quot;, Vazirmatn, &quot;SF Pro Text&quot;, -apple-system, BlinkMacSystemFont, Roboto, &quot;Segoe UI&quot;, Helvetica, Arial, sans-serif, &quot;Apple Color Emoji&quot;, &quot;Segoe UI Emoji&quot;, &quot;Segoe UI Symbol&quot;;\">This is a creative, project-based course designed to make learning web development both practical and enjoyable. Rather than diving into complex tools or frameworks, you’ll stick to the essentials - HTML5 and CSS3 - while building interactive mini-projects like a digital credit card, blog post card, contact form, FAQ section, recipe layout, login/register form, and more.</p><p style=\"margin-right: 0px; margin-bottom: 0px; margin-left: 0px; padding: 0px; font-size: 14.875px; max-inline-size: 118.4rem; margin-block-start: 0.8rem; color: oklch(0.2974 0.0362 281.74); font-family: &quot;Udemy Sans&quot;, Vazirmatn, &quot;SF Pro Text&quot;, -apple-system, BlinkMacSystemFont, Roboto, &quot;Segoe UI&quot;, Helvetica, Arial, sans-serif, &quot;Apple Color Emoji&quot;, &quot;Segoe UI Emoji&quot;, &quot;Segoe UI Symbol&quot;;\">Each project focuses on a specific concept - from layout and form handling to responsive design, text styling, and animation - giving you the building blocks to create beautiful, functional interfaces. You’ll gain confidence with tools like&nbsp;<strong style=\"margin: 0px; padding: 0px;\">Flexbox</strong>,&nbsp;<strong style=\"margin: 0px; padding: 0px;\">Grid</strong>, custom fonts, icons, and transitions, while building a portfolio of creative, bite-size</p>',13651200000000,30000,25000,1,'2025-10-28 04:58:28.778886','2025-10-31 06:28:32.784671',1),(2,'PHP backend web developments','course_img/back-end-developer-typographic-h.jpg','Enroll in our  PHP course to learn how to code with this popular server-side scripting language. Learn PHP basic concepts like variables, data types, control statements, loops, and functions through hands-on implementations.','<p style=\"margin-right: 0px; margin-bottom: 0px; margin-left: 0px; padding: 0px; border: 0px; vertical-align: baseline; font-family: Poppins, sans-serif; font-size: 16px; -webkit-font-smoothing: antialiased; line-height: 24px; outline: 0px; -webkit-tap-highlight-color: transparent; color: rgb(68, 68, 68);\">If you are a beginner looking to get started with PHP, this course is for you! This comprehensive course will cover the basics of PHP, including installation, comments, variables, operators, and functions.</p><p style=\"margin-right: 0px; margin-bottom: 0px; margin-left: 0px; padding: 0px; border: 0px; vertical-align: baseline; font-family: Poppins, sans-serif; font-size: 16px; -webkit-font-smoothing: antialiased; line-height: 24px; outline: 0px; -webkit-tap-highlight-color: transparent; color: rgb(68, 68, 68);\">&nbsp;</p><p style=\"margin-right: 0px; margin-bottom: 0px; margin-left: 0px; padding: 0px; border: 0px; vertical-align: baseline; font-family: Poppins, sans-serif; font-size: 16px; -webkit-font-smoothing: antialiased; line-height: 1.38; outline: 0px; -webkit-tap-highlight-color: transparent; color: rgb(68, 68, 68);\">PHP is a robust scripting language widely used for developing dynamic web pages, and this PHP online course helps you comprehend its fundamentals. You will first get introduced to PHP and go through the installation. Providing comments is often the best practice. Thus, you will learn about comments in PHP. You will understand the concept of variables, scope variables, echo and print statements, data types, control statements, loops, operators, strings, functions, and arrays in PHP. You will understand them better with the provided hands-on examples. Enroll in this PHP free course and earn a certificate of course completion.</p><p style=\"margin-right: 0px; margin-bottom: 0px; margin-left: 0px; padding: 0px; border: 0px; vertical-align: baseline; font-family: Poppins, sans-serif; font-size: 16px; -webkit-font-smoothing: antialiased; line-height: 24px; outline: 0px; -webkit-tap-highlight-color: transparent; color: rgb(68, 68, 68);\">&nbsp;</p><p style=\"margin-right: 0px; margin-bottom: 0px; margin-left: 0px; padding: 0px; border: 0px; vertical-align: baseline; font-family: Poppins, sans-serif; font-size: 16px; -webkit-font-smoothing: antialiased; line-height: 24px; outline: 0px; -webkit-tap-highlight-color: transparent; color: rgb(68, 68, 68);\">Enhance your software development skills with Great Learning\'s&nbsp;<a href=\"https://www.mygreatlearning.com/software-engineering/courses\" style=\"color: black; text-decoration: none;\">Best Software Engineering Courses</a>. Enroll in the top-rated program of your interest and achieve a certificate that exhibits your skills.</p>',13651200000000,30000,25000,1,'2025-10-28 05:45:43.163293','2025-10-31 06:27:30.261787',1);
/*!40000 ALTER TABLE `course_app_course` ENABLE KEYS */;
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
