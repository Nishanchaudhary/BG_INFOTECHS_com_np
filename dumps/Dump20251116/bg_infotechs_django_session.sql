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
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('2950m4308danefbnmqkkjytda12vw9b6','.eJxVjEsOwiAUAO_C2hD-tC7d9wzkwXtI1UBS2pXx7oakC93OTObNAhx7CUenLazIrkyyyy-LkJ5Uh8AH1HvjqdV9WyMfCT9t50tDet3O9m9QoJextdYi-Sw0RR9xMiqhzT5h0jhJKwm0ma3JUZNyTszKo9TKG8ogMjjPPl_vtDgF:1vHxzU:kDXO6SYEqTOVnGCwpJUdc27j9zrRaQZFmVcsfQCXPVw','2025-11-23 05:29:28.834408'),('2wg8mqejhwceb3hutk2ygufkp6k3ndjp','.eJxVjEsOwiAUAO_C2hD-tC7d9wzkwXtI1UBS2pXx7oakC93OTObNAhx7CUenLazIrkyyyy-LkJ5Uh8AH1HvjqdV9WyMfCT9t50tDet3O9m9QoJextdYi-Sw0RR9xMiqhzT5h0jhJKwm0ma3JUZNyTszKo9TKG8ogMjjPPl_vtDgF:1vIj32:RZvca8e8o7RRqtlkddRngzP0-l6IYvocLasTsEvk4UM','2025-11-25 07:44:16.760033'),('3ei8yff1g0fkw1og2imhbocv17opa9ty','.eJxVjEsOwiAUAO_C2hD-tC7d9wzkwXtI1UBS2pXx7oakC93OTObNAhx7CUenLazIrkyyyy-LkJ5Uh8AH1HvjqdV9WyMfCT9t50tDet3O9m9QoJextdYi-Sw0RR9xMiqhzT5h0jhJKwm0ma3JUZNyTszKo9TKG8ogMjjPPl_vtDgF:1vJnaC:H9FLAJKZ-XQ7Gd7JRASpKAb3FG_hB21q5deiPyZ5hHM','2025-11-28 06:46:56.689139'),('77olbbb12jl0jklzttd5om2690427ops','.eJxVjEsOwiAUAO_C2hD-tC7d9wzkwXtI1UBS2pXx7oakC93OTObNAhx7CUenLazIrkyyyy-LkJ5Uh8AH1HvjqdV9WyMfCT9t50tDet3O9m9QoJextdYi-Sw0RR9xMiqhzT5h0jhJKwm0ma3JUZNyTszKo9TKG8ogMjjPPl_vtDgF:1vILB4:DObM417Bpqwf8neUg-IO6hmd9BoY4qGG46-2BY2JulM','2025-11-24 06:14:58.134476'),('b324tqfgy2im287tfi5j1p66jywkqg7a','.eJxVjEsOwiAUAO_C2hD-tC7d9wzkwXtI1UBS2pXx7oakC93OTObNAhx7CUenLazIrkyyyy-LkJ5Uh8AH1HvjqdV9WyMfCT9t50tDet3O9m9QoJextdYi-Sw0RR9xMiqhzT5h0jhJKwm0ma3JUZNyTszKo9TKG8ogMjjPPl_vtDgF:1vIk2r:g465CQIoH-3wR_q-rGn3kx2Ex_Z6I-tad59cqh1SlGE','2025-11-25 08:48:09.138577'),('ci4zmuuzsk4rokkm1f6bybujmx3vgo0f','.eJxVjEsOwiAUAO_C2hD-tC7d9wzkwXtI1UBS2pXx7oakC93OTObNAhx7CUenLazIrkyyyy-LkJ5Uh8AH1HvjqdV9WyMfCT9t50tDet3O9m9QoJextdYi-Sw0RR9xMiqhzT5h0jhJKwm0ma3JUZNyTszKo9TKG8ogMjjPPl_vtDgF:1vILB9:Ht9ev7ZO04uNzfmh4OHh2U1pbQaWf_ARAyJ9SjD7mYQ','2025-11-24 06:15:03.934792'),('ixgzai1wiudc1dzkir33w7zap8rn5sbp','.eJxVjEsOwiAUAO_C2hD-tC7d9wzkwXtI1UBS2pXx7oakC93OTObNAhx7CUenLazIrkyyyy-LkJ5Uh8AH1HvjqdV9WyMfCT9t50tDet3O9m9QoJextdYi-Sw0RR9xMiqhzT5h0jhJKwm0ma3JUZNyTszKo9TKG8ogMjjPPl_vtDgF:1vE2Vy:xkJzfLI8TtsQ_CcHfIidkMGb9qqEkaZKk0lDEfgu5oA','2025-11-12 09:30:46.601275'),('ugw3bp7sszba0flu6jh8bw9oiq0kkh1r','.eJxVjEsOwiAUAO_C2hD-tC7d9wzkwXtI1UBS2pXx7oakC93OTObNAhx7CUenLazIrkyyyy-LkJ5Uh8AH1HvjqdV9WyMfCT9t50tDet3O9m9QoJextdYi-Sw0RR9xMiqhzT5h0jhJKwm0ma3JUZNyTszKo9TKG8ogMjjPPl_vtDgF:1vDX45:NwLhcJ4beUA055zV7OJSWIMRYMDOvPyuLqO19uJ54qk','2025-11-10 23:55:53.981927'),('umjjtm4gjtamitwqzuyw81lqydah6u76','.eJxVjEsOwiAUAO_C2hD-tC7d9wzkwXtI1UBS2pXx7oakC93OTObNAhx7CUenLazIrkyyyy-LkJ5Uh8AH1HvjqdV9WyMfCT9t50tDet3O9m9QoJextdYi-Sw0RR9xMiqhzT5h0jhJKwm0ma3JUZNyTszKo9TKG8ogMjjPPl_vtDgF:1vKU8I:NWu93-lrRAjYGgFtmLRUDkDCmoIBFkpEIv4gqnVQQcc','2025-11-30 04:12:58.228965'),('wvycp6k3dos2nlj2lhcgo96lvpunyiyr','.eJxVjEsOwiAUAO_C2hD-tC7d9wzkwXtI1UBS2pXx7oakC93OTObNAhx7CUenLazIrkyyyy-LkJ5Uh8AH1HvjqdV9WyMfCT9t50tDet3O9m9QoJextdYi-Sw0RR9xMiqhzT5h0jhJKwm0ma3JUZNyTszKo9TKG8ogMjjPPl_vtDgF:1vGvQG:yY1MIlzoOpVv9x2U3yt7_tS63dQXHTLP73o2f5xY1_0','2025-11-20 08:32:48.154156');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
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
