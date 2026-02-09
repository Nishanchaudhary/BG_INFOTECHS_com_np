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
-- Table structure for table `bg_app_user_user_permissions`
--

DROP TABLE IF EXISTS `bg_app_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bg_app_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `bg_app_user_user_permissions_user_id_permission_id_0ddae6a4_uniq` (`user_id`,`permission_id`),
  KEY `bg_app_user_user_per_permission_id_b6318419_fk_auth_perm` (`permission_id`),
  CONSTRAINT `bg_app_user_user_per_permission_id_b6318419_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `bg_app_user_user_permissions_user_id_aae9b119_fk_bg_app_user_id` FOREIGN KEY (`user_id`) REFERENCES `bg_app_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=155 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bg_app_user_user_permissions`
--

LOCK TABLES `bg_app_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `bg_app_user_user_permissions` DISABLE KEYS */;
INSERT INTO `bg_app_user_user_permissions` VALUES (50,2,5),(51,2,6),(52,2,7),(53,2,8),(54,2,25),(55,2,26),(56,2,27),(57,2,28),(58,2,29),(1,2,30),(2,2,31),(3,2,32),(4,2,33),(5,2,34),(6,2,35),(7,2,36),(8,2,37),(9,2,38),(10,2,39),(11,2,40),(12,2,41),(13,2,42),(14,2,43),(15,2,44),(16,2,45),(17,2,46),(18,2,47),(19,2,48),(20,2,49),(21,2,50),(22,2,51),(23,2,52),(24,2,53),(59,2,54),(60,2,55),(61,2,56),(62,2,57),(63,2,58),(64,2,59),(65,2,60),(66,2,61),(67,2,62),(68,2,63),(69,2,64),(70,2,65),(71,2,66),(72,2,67),(73,2,68),(74,2,69),(25,2,70),(26,2,71),(27,2,72),(28,2,73),(75,2,74),(76,2,75),(77,2,76),(78,2,77),(79,2,78),(80,2,79),(81,2,80),(82,2,81),(83,2,82),(84,2,83),(85,2,84),(86,2,85),(87,2,86),(88,2,87),(89,2,88),(90,2,89),(29,2,90),(30,2,91),(31,2,92),(32,2,93),(91,2,94),(92,2,95),(93,2,96),(94,2,97),(33,2,98),(34,2,99),(35,2,100),(36,2,101),(37,2,102),(38,2,103),(39,2,104),(40,2,105),(95,2,106),(96,2,107),(97,2,108),(98,2,109),(41,2,110),(42,2,111),(43,2,112),(44,2,113),(45,2,115),(46,2,117),(47,2,118),(48,2,119),(49,2,120),(99,2,121),(100,2,122),(101,2,123),(102,2,124),(103,2,129),(104,2,130),(105,2,131),(106,2,132),(135,2,133),(136,2,134),(137,2,135),(138,2,136),(139,2,137),(140,2,138),(141,2,139),(142,2,140),(115,2,141),(116,2,142),(117,2,143),(118,2,144),(151,2,145),(152,2,146),(153,2,147),(154,2,148),(143,2,149),(144,2,150),(145,2,151),(146,2,152),(147,2,153),(148,2,154),(149,2,155),(150,2,156),(131,2,157),(132,2,158),(133,2,159),(134,2,160);
/*!40000 ALTER TABLE `bg_app_user_user_permissions` ENABLE KEYS */;
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
