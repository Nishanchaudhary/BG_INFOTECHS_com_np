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
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=161 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add attachment',6,'add_attachment'),(22,'Can change attachment',6,'change_attachment'),(23,'Can delete attachment',6,'delete_attachment'),(24,'Can view attachment',6,'view_attachment'),(25,'Can add company_profile',7,'add_company_profile'),(26,'Can change company_profile',7,'change_company_profile'),(27,'Can delete company_profile',7,'delete_company_profile'),(28,'Can view company_profile',7,'view_company_profile'),(29,'Can manage company profile',7,'manage_company_profile'),(30,'Can add features',8,'add_features'),(31,'Can change features',8,'change_features'),(32,'Can delete features',8,'delete_features'),(33,'Can view features',8,'view_features'),(34,'Can add Service',9,'add_services'),(35,'Can change Service',9,'change_services'),(36,'Can delete Service',9,'delete_services'),(37,'Can view Service',9,'view_services'),(38,'Can add testimonials',10,'add_testimonials'),(39,'Can change testimonials',10,'change_testimonials'),(40,'Can delete testimonials',10,'delete_testimonials'),(41,'Can view testimonials',10,'view_testimonials'),(42,'Can add Project Done',11,'add_project_done'),(43,'Can change Project Done',11,'change_project_done'),(44,'Can delete Project Done',11,'delete_project_done'),(45,'Can view Project Done',11,'view_project_done'),(46,'Can add Service Testimonial',12,'add_services_testimonial'),(47,'Can change Service Testimonial',12,'change_services_testimonial'),(48,'Can delete Service Testimonial',12,'delete_services_testimonial'),(49,'Can view Service Testimonial',12,'view_services_testimonial'),(50,'Can add Service FAQ',13,'add_services_faq'),(51,'Can change Service FAQ',13,'change_services_faq'),(52,'Can delete Service FAQ',13,'delete_services_faq'),(53,'Can view Service FAQ',13,'view_services_faq'),(54,'Can add Category',14,'add_category'),(55,'Can change Category',14,'change_category'),(56,'Can delete Category',14,'delete_category'),(57,'Can view Category',14,'view_category'),(58,'Can add training',15,'add_training'),(59,'Can change training',15,'change_training'),(60,'Can delete training',15,'delete_training'),(61,'Can view training',15,'view_training'),(62,'Can add training image',16,'add_trainingimage'),(63,'Can change training image',16,'change_trainingimage'),(64,'Can delete training image',16,'delete_trainingimage'),(65,'Can view training image',16,'view_trainingimage'),(66,'Can add category',17,'add_category'),(67,'Can change category',17,'change_category'),(68,'Can delete category',17,'delete_category'),(69,'Can view category',17,'view_category'),(70,'Can add Blog Post',18,'add_blog'),(71,'Can change Blog Post',18,'change_blog'),(72,'Can delete Blog Post',18,'delete_blog'),(73,'Can view Blog Post',18,'view_blog'),(74,'Can add Blog Comment',19,'add_blogcomment'),(75,'Can change Blog Comment',19,'change_blogcomment'),(76,'Can delete Blog Comment',19,'delete_blogcomment'),(77,'Can view Blog Comment',19,'view_blogcomment'),(78,'Can add Vacancy',20,'add_vacancy'),(79,'Can change Vacancy',20,'change_vacancy'),(80,'Can delete Vacancy',20,'delete_vacancy'),(81,'Can view Vacancy',20,'view_vacancy'),(82,'Can add Job Application',21,'add_jobapplication'),(83,'Can change Job Application',21,'change_jobapplication'),(84,'Can delete Job Application',21,'delete_jobapplication'),(85,'Can view Job Application',21,'view_jobapplication'),(86,'Can add Team Member',22,'add_teams'),(87,'Can change Team Member',22,'change_teams'),(88,'Can delete Team Member',22,'delete_teams'),(89,'Can view Team Member',22,'view_teams'),(90,'Can add FAQ',23,'add_faq'),(91,'Can change FAQ',23,'change_faq'),(92,'Can delete FAQ',23,'delete_faq'),(93,'Can view FAQ',23,'view_faq'),(94,'Can add Slider',24,'add_slider'),(95,'Can change Slider',24,'change_slider'),(96,'Can delete Slider',24,'delete_slider'),(97,'Can view Slider',24,'view_slider'),(98,'Can add Course',25,'add_course'),(99,'Can change Course',25,'change_course'),(100,'Can delete Course',25,'delete_course'),(101,'Can view Course',25,'view_course'),(102,'Can add Media',26,'add_media'),(103,'Can change Media',26,'change_media'),(104,'Can delete Media',26,'delete_media'),(105,'Can view Media',26,'view_media'),(106,'Can add Role',27,'add_role'),(107,'Can change Role',27,'change_role'),(108,'Can delete Role',27,'delete_role'),(109,'Can view Role',27,'view_role'),(110,'Can add User',28,'add_user'),(111,'Can change User',28,'change_user'),(112,'Can delete User',28,'delete_user'),(113,'Can view User',28,'view_user'),(114,'Can view admin dashboard',28,'view_admin_dashboard'),(115,'Can view staff dashboard',28,'view_staff_dashboard'),(116,'Can view student dashboard',28,'view_student_dashboard'),(117,'Can manage staff',28,'manage_staff'),(118,'Can manage students',28,'manage_students'),(119,'Can manage financial data',28,'manage_financial'),(120,'Can manage roles',28,'manage_roles'),(121,'Can add Staff',29,'add_staff'),(122,'Can change Staff',29,'change_staff'),(123,'Can delete Staff',29,'delete_staff'),(124,'Can view Staff',29,'view_staff'),(125,'Can add Staff Permission',30,'add_staffpermission'),(126,'Can change Staff Permission',30,'change_staffpermission'),(127,'Can delete Staff Permission',30,'delete_staffpermission'),(128,'Can view Staff Permission',30,'view_staffpermission'),(129,'Can add Student',31,'add_student'),(130,'Can change Student',31,'change_student'),(131,'Can delete Student',31,'delete_student'),(132,'Can view Student',31,'view_student'),(133,'Can add Package',32,'add_package'),(134,'Can change Package',32,'change_package'),(135,'Can delete Package',32,'delete_package'),(136,'Can view Package',32,'view_package'),(137,'Can add branch',33,'add_branch'),(138,'Can change branch',33,'change_branch'),(139,'Can delete branch',33,'delete_branch'),(140,'Can view branch',33,'view_branch'),(141,'Can add Course Enrollment',34,'add_courseenrollment'),(142,'Can change Course Enrollment',34,'change_courseenrollment'),(143,'Can delete Course Enrollment',34,'delete_courseenrollment'),(144,'Can view Course Enrollment',34,'view_courseenrollment'),(145,'Can add Custom Package',35,'add_custompackage'),(146,'Can change Custom Package',35,'change_custompackage'),(147,'Can delete Custom Package',35,'delete_custompackage'),(148,'Can view Custom Package',35,'view_custompackage'),(149,'Can add Plan Subscriber',36,'add_plansubscriber'),(150,'Can change Plan Subscriber',36,'change_plansubscriber'),(151,'Can delete Plan Subscriber',36,'delete_plansubscriber'),(152,'Can view Plan Subscriber',36,'view_plansubscriber'),(153,'Can add Contact',37,'add_contact'),(154,'Can change Contact',37,'change_contact'),(155,'Can delete Contact',37,'delete_contact'),(156,'Can view Contact',37,'view_contact'),(157,'Can add services_success',38,'add_services_success'),(158,'Can change services_success',38,'change_services_success'),(159,'Can delete services_success',38,'delete_services_success'),(160,'Can view services_success',38,'view_services_success');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
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
