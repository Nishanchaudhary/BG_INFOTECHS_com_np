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
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-10-27 02:54:04.865706'),(2,'contenttypes','0002_remove_content_type_name','2025-10-27 02:54:05.403455'),(3,'auth','0001_initial','2025-10-27 02:54:06.298766'),(4,'auth','0002_alter_permission_name_max_length','2025-10-27 02:54:06.428941'),(5,'auth','0003_alter_user_email_max_length','2025-10-27 02:54:06.439850'),(6,'auth','0004_alter_user_username_opts','2025-10-27 02:54:06.452545'),(7,'auth','0005_alter_user_last_login_null','2025-10-27 02:54:06.464815'),(8,'auth','0006_require_contenttypes_0002','2025-10-27 02:54:06.471160'),(9,'auth','0007_alter_validators_add_error_messages','2025-10-27 02:54:06.484917'),(10,'auth','0008_alter_user_username_max_length','2025-10-27 02:54:06.496756'),(11,'auth','0009_alter_user_last_name_max_length','2025-10-27 02:54:06.510165'),(12,'auth','0010_alter_group_name_max_length','2025-10-27 02:54:06.540387'),(13,'auth','0011_update_proxy_permissions','2025-10-27 02:54:06.553359'),(14,'auth','0012_alter_user_first_name_max_length','2025-10-27 02:54:06.562853'),(15,'bg_app','0001_initial','2025-10-27 02:54:08.859285'),(16,'admin','0001_initial','2025-10-27 02:54:09.221594'),(17,'admin','0002_logentry_remove_auto_add','2025-10-27 02:54:09.250499'),(18,'admin','0003_logentry_add_action_flag_choices','2025-10-27 02:54:09.271986'),(19,'blog_app','0001_initial','2025-10-27 02:54:10.266883'),(20,'company_app','0001_initial','2025-10-27 02:54:10.592623'),(21,'company_app','0002_alter_company_profile_options','2025-10-27 02:54:10.602324'),(22,'company_app','0003_services_testimonial','2025-10-27 02:54:10.857530'),(23,'company_app','0004_services_faq','2025-10-27 02:54:11.071071'),(24,'company_app','0005_catagory','2025-10-27 02:54:11.123762'),(25,'company_app','0006_category_delete_catagory','2025-10-27 02:54:11.235546'),(26,'company_app','0007_project_done_category','2025-10-27 02:54:11.377427'),(27,'contact_app','0001_initial','2025-10-27 02:54:11.429713'),(28,'course_app','0001_initial','2025-10-27 02:54:11.795086'),(29,'django_summernote','0001_initial','2025-10-27 02:54:11.844376'),(30,'django_summernote','0002_update-help_text','2025-10-27 02:54:11.853301'),(31,'django_summernote','0003_alter_attachment_id','2025-10-27 02:54:11.956364'),(32,'faq_app','0001_initial','2025-10-27 02:54:12.177809'),(33,'faq_app','0002_slider','2025-10-27 02:54:12.459659'),(34,'faq_app','0003_rename_sliders_status_ecbd5a_idx_slider_status_20198b_idx_and_more','2025-10-27 02:54:12.595245'),(35,'package_app','0001_initial','2025-10-27 02:54:12.651375'),(36,'sessions','0001_initial','2025-10-27 02:54:12.733474'),(37,'teams_app','0001_initial','2025-10-27 02:54:12.924133'),(38,'trainings_app','0001_initial','2025-10-27 02:54:13.129489'),(39,'vacancy_app','0001_initial','2025-10-27 02:54:13.317604'),(40,'vacancy_app','0002_jobapplication','2025-10-27 02:54:13.522797'),(41,'vacancy_app','0003_alter_vacancy_salary','2025-10-28 00:44:12.948660'),(42,'course_app','0002_courseenrollment','2025-10-28 07:32:24.095333'),(43,'blog_app','0002_remove_blogcomment_user_blogcomment_email_and_more','2025-10-29 06:02:41.306468'),(44,'course_app','0003_alter_courseenrollment_unique_together','2025-10-29 06:02:41.456207'),(45,'package_app','0002_custompackage','2025-11-02 04:23:47.542678'),(46,'package_app','0003_plansubscriber','2025-11-02 10:45:55.292345'),(47,'package_app','0004_rename_package_plansubscriber_package','2025-11-02 14:07:51.406292'),(48,'package_app','0005_custompackage_created_at_plansubscriber_created_at','2025-11-02 15:40:19.609985'),(49,'contact_app','0002_branch_facebook_branch_instagram_branch_linkedin_and_more','2025-11-03 06:41:53.462424'),(50,'contact_app','0003_contact','2025-11-03 08:28:58.555076'),(51,'contact_app','0004_alter_contact_phone_number','2025-11-03 10:29:17.221758'),(52,'company_app','0008_services_success','2025-11-05 11:35:54.994367'),(53,'package_app','0006_alter_custompackage_created_at_alter_package_image_and_more','2025-11-07 03:56:54.434024'),(54,'package_app','0007_alter_package_image','2025-11-07 04:00:38.983525'),(55,'package_app','0008_alter_package_tags','2025-11-14 06:34:57.952574');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-16 11:39:48
