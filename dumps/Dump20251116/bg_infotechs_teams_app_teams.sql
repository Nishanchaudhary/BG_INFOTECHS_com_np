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
-- Table structure for table `teams_app_teams`
--

DROP TABLE IF EXISTS `teams_app_teams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teams_app_teams` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `image` varchar(100) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `email` varchar(254) NOT NULL,
  `facebook` varchar(500) DEFAULT NULL,
  `twitter` varchar(500) DEFAULT NULL,
  `linkedin` varchar(500) DEFAULT NULL,
  `tiktok` varchar(500) DEFAULT NULL,
  `designation` varchar(100) DEFAULT NULL,
  `description` longtext NOT NULL,
  `skills` longtext NOT NULL,
  `status` varchar(10) NOT NULL,
  `display_order` int NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `author_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `teams_app_teams_author_id_396ccbc5_fk_bg_app_user_id` (`author_id`),
  CONSTRAINT `teams_app_teams_author_id_396ccbc5_fk_bg_app_user_id` FOREIGN KEY (`author_id`) REFERENCES `bg_app_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teams_app_teams`
--

LOCK TABLES `teams_app_teams` WRITE;
/*!40000 ALTER TABLE `teams_app_teams` DISABLE KEYS */;
INSERT INTO `teams_app_teams` VALUES (1,'Sunita Bhandari','teams/person-f-6.jpg','9824727890','Sunita@gmail.com','https://facebook.com/','https://x.com','https://linkedin.com','https://tiktok.com','Digital Marketing Head','<p><div aria-hidden=\"true\" data-edge=\"true\" class=\"pointer-events-none h-px w-px\"></div></p><article class=\"text-token-text-primary w-full focus:outline-none [--shadow-height:45px] has-data-writing-block:pointer-events-none has-data-writing-block:-mt-(--shadow-height) has-data-writing-block:pt-(--shadow-height) [&amp;:has([data-writing-block])&gt;*]:pointer-events-auto [content-visibility:auto] supports-[content-visibility:auto]:[contain-intrinsic-size:auto_100lvh] scroll-mt-[calc(var(--header-height)+min(200px,max(70px,20svh)))]\" tabindex=\"-1\" dir=\"auto\" data-turn-id=\"request-WEB:870be9d2-71ac-44cc-96ff-360a98d69335-0\" data-testid=\"conversation-turn-2\" data-scroll-anchor=\"true\" data-turn=\"assistant\"><div class=\"text-base my-auto mx-auto pb-10 [--thread-content-margin:--spacing(4)] thread-sm:[--thread-content-margin:--spacing(6)] thread-lg:[--thread-content-margin:--spacing(16)] px-(--thread-content-margin)\"><div class=\"[--thread-content-max-width:40rem] thread-lg:[--thread-content-max-width:48rem] mx-auto max-w-(--thread-content-max-width) flex-1 group/turn-messages focus-visible:outline-hidden relative flex w-full min-w-0 flex-col agent-turn\" tabindex=\"-1\"><div class=\"flex max-w-full flex-col grow\"><div data-message-author-role=\"assistant\" data-message-id=\"722e8caa-46fc-4fbc-a031-aa7b92e43dbb\" dir=\"auto\" class=\"min-h-8 text-message relative flex w-full flex-col items-end gap-2 text-start break-words whitespace-normal [.text-message+&amp;]:mt-1\" data-message-model-slug=\"gpt-5\"><div class=\"flex w-full flex-col gap-1 empty:hidden first:pt-[1px]\"><div class=\"markdown prose dark:prose-invert w-full break-words dark markdown-new-styling\"><p data-start=\"0\" data-end=\"406\" data-is-last-node=\"\" data-is-only-node=\"\">A <strong data-start=\"2\" data-end=\"28\">Digital Marketing Head</strong> is a senior professional responsible for developing, implementing, and managing a company’s overall digital marketing strategy. They oversee online campaigns, manage digital channels (such as social media, email, SEO, and paid ads), analyze performance data, and lead marketing teams to drive brand awareness, customer engagement, and business growth through digital platforms.</p></div></div></div></div><div class=\"z-0 flex min-h-[46px] justify-start\"></div></div></div></article>','SEO,\r\nSocial Media,\r\nContent Strategy','active',1,'2025-10-28 00:30:55.265955','2025-10-28 00:30:55.265990',1),(2,'Anil Kumar','teams/businessman-isolated-illustratio.jpg','9868567890','anil@gmail.com','https://facebook.com/','https://x.com','https://linkedin.com','https://tiktok.com','UI/UX Designer','<p>A <strong>UI/UX Designer</strong> is a creative professional who focuses on designing user-friendly and visually appealing digital experiences. They combine user research, design principles, and usability testing to create intuitive interfaces and seamless interactions that enhance how users engage with websites, apps, or software.</p>','Design Thinking,\r\nUser Research,\r\nPrototyping','active',2,'2025-10-28 00:33:56.408152','2025-10-28 00:33:56.409809',1),(3,'Rajesh Thapa','teams/pngtree-smiling-man-posing-for-a-portrait-png-image_16420590.png','9824927890','rajesh@gmail.com','https://facebook.com/','https://x.com','https://linkedin.com','https://tiktok.com','Technical Director','<p>A <strong>Technical Director</strong> is a senior expert responsible for overseeing the technical aspects of projects, ensuring that all systems, technologies, and processes run efficiently. They lead technical teams, provide strategic direction, and ensure that technical solutions align with the organization’s goals and quality standards.</p>','Web Development,\r\nMobile Apps,\r\nCloud Solutions','active',3,'2025-10-28 00:37:03.544975','2025-10-28 00:37:03.545012',1);
/*!40000 ALTER TABLE `teams_app_teams` ENABLE KEYS */;
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
