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
-- Table structure for table `company_app_features`
--

DROP TABLE IF EXISTS `company_app_features`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `company_app_features` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  `tags` varchar(200) NOT NULL,
  `icon` varchar(100) NOT NULL,
  `status` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `company_app_features`
--

LOCK TABLES `company_app_features` WRITE;
/*!40000 ALTER TABLE `company_app_features` DISABLE KEYS */;
INSERT INTO `company_app_features` VALUES (1,'Lightning Fast Performance','<p><span style=\"color: rgb(68, 67, 67); font-family: &quot;Segoe UI&quot;, Tahoma, Geneva, Verdana, sans-serif; font-size: 15px; text-align: center;\">Optimized software and websites that load faster and work smarter, keeping your customers engaged.</span></p>','Speed,Optimization','fa-solid fa-bolt',1),(2,'Enterprise-Grade Security','<p><span style=\"color: rgb(68, 67, 67); font-family: &quot;Segoe UI&quot;, Tahoma, Geneva, Verdana, sans-serif; font-size: 15px; text-align: center;\">Your data is safe with us — with best practices and modern encryption keeping your systems secure.</span></p>','Secure,Protected','fa-solid fa-shield-halved',1),(3,'Seamless Collaboration','<p><span style=\"color: rgb(68, 67, 67); font-family: &quot;Segoe UI&quot;, Tahoma, Geneva, Verdana, sans-serif; font-size: 15px; text-align: center;\">Work better together with integrated tools for team management, communication, and workflow alignment.</span></p>','Teamwork,Collaboration','fa-solid fa-users',1),(4,'Advanced Analytics','<p><span style=\"color: rgb(68, 67, 67); font-family: &quot;Segoe UI&quot;, Tahoma, Geneva, Verdana, sans-serif; font-size: 15px; text-align: center;\">Turn data into actionable insights with powerful analytics that drive smarter business decisions.</span></p>','Data,Insights','fa-solid fa-chart-line',1),(5,'Smart Automation','<p><span style=\"color: rgb(68, 67, 67); font-family: &quot;Segoe UI&quot;, Tahoma, Geneva, Verdana, sans-serif; font-size: 15px; text-align: center;\">Automate routine tasks and focus on what matters most with intelligent, customized workflows.</span></p>','Automation,Workflow','fa-solid fa-robot',1),(6,'Cloud Integration','<p><span style=\"color: rgb(68, 67, 67); font-family: &quot;Segoe UI&quot;, Tahoma, Geneva, Verdana, sans-serif; font-size: 15px; text-align: center;\">Effortlessly connect with cloud platforms for flexible, reliable, and scalable solutions wherever you are.</span></p>','Cloud,Scalable','fa-solid fa-cloud-arrow-up',1);
/*!40000 ALTER TABLE `company_app_features` ENABLE KEYS */;
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
