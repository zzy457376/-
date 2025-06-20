-- MySQL dump 10.13  Distrib 9.3.0, for Win64 (x86_64)
--
-- Host: localhost    Database: movie_industry
-- ------------------------------------------------------
-- Server version	9.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `actor`
--

DROP TABLE IF EXISTS `actor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `actor` (
  `actor_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `dob` date DEFAULT NULL,
  PRIMARY KEY (`actor_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `actor`
--

LOCK TABLES `actor` WRITE;
/*!40000 ALTER TABLE `actor` DISABLE KEYS */;
INSERT INTO `actor` VALUES (1,'鏌婄憼缇?,'1987-06-01'),(2,'閲戝煄姝?,'1973-10-11'),(3,'鍒樺痉鍗?,'1961-09-27'),(4,'Tim Robbins','1958-10-16'),(5,'Morgan Freeman','1937-06-01');
/*!40000 ALTER TABLE `actor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `director`
--

DROP TABLE IF EXISTS `director`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `director` (
  `director_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `dob` date DEFAULT NULL,
  PRIMARY KEY (`director_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `director`
--

LOCK TABLES `director` WRITE;
/*!40000 ALTER TABLE `director` DISABLE KEYS */;
INSERT INTO `director` VALUES (1,'瀹磶楠?,'1941-01-05'),(2,'寮犺壓璋?,'1950-11-14'),(3,'Frank Darabont','1959-01-28');
/*!40000 ALTER TABLE `director` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `genre`
--

DROP TABLE IF EXISTS `genre`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `genre` (
  `genre_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`genre_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `genre`
--

LOCK TABLES `genre` WRITE;
/*!40000 ALTER TABLE `genre` DISABLE KEYS */;
INSERT INTO `genre` VALUES (1,'鍔ㄧ敾'),(2,'鍓ф儏'),(3,'鐘姜'),(4,'姝︿緺');
/*!40000 ALTER TABLE `genre` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `movie`
--

DROP TABLE IF EXISTS `movie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movie` (
  `movie_id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `release_year` int DEFAULT NULL,
  `duration` int DEFAULT NULL,
  `synopsis` text,
  `production_company_id` int DEFAULT NULL,
  PRIMARY KEY (`movie_id`),
  KEY `production_company_id` (`production_company_id`),
  CONSTRAINT `movie_ibfk_1` FOREIGN KEY (`production_company_id`) REFERENCES `production_company` (`production_company_id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movie`
--

LOCK TABLES `movie` WRITE;
/*!40000 ALTER TABLE `movie` DISABLE KEYS */;
INSERT INTO `movie` VALUES (1,'鍗冧笌鍗冨',2001,125,'灏戝コ鍗冨璇叆绁炵伒涓栫晫锛屼负鏁戠埗姣嶈€屽睍寮€鍐掗櫓銆?,1),(2,'鍗侀潰鍩嬩紡',2004,119,'姹熸箹涔夊啗涓庢湞寤峰娍鍔涢棿鐨勭埍鎭ㄧ籂钁涖€?,2),(3,'鑲栫敵鍏嬬殑鏁戣祹',1994,142,'閾惰瀹跺畨杩湪鐩戠嫳涓鎵捐嚜鐢变笌甯屾湜銆?,3);
/*!40000 ALTER TABLE `movie` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `movie_director`
--

DROP TABLE IF EXISTS `movie_director`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movie_director` (
  `movie_id` int NOT NULL,
  `director_id` int NOT NULL,
  PRIMARY KEY (`movie_id`,`director_id`),
  KEY `director_id` (`director_id`),
  CONSTRAINT `movie_director_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movie` (`movie_id`) ON DELETE CASCADE,
  CONSTRAINT `movie_director_ibfk_2` FOREIGN KEY (`director_id`) REFERENCES `director` (`director_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movie_director`
--

LOCK TABLES `movie_director` WRITE;
/*!40000 ALTER TABLE `movie_director` DISABLE KEYS */;
INSERT INTO `movie_director` VALUES (1,1),(2,2),(3,3);
/*!40000 ALTER TABLE `movie_director` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `movie_genre`
--

DROP TABLE IF EXISTS `movie_genre`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movie_genre` (
  `movie_id` int NOT NULL,
  `genre_id` int NOT NULL,
  PRIMARY KEY (`movie_id`,`genre_id`),
  KEY `genre_id` (`genre_id`),
  CONSTRAINT `movie_genre_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movie` (`movie_id`) ON DELETE CASCADE,
  CONSTRAINT `movie_genre_ibfk_2` FOREIGN KEY (`genre_id`) REFERENCES `genre` (`genre_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movie_genre`
--

LOCK TABLES `movie_genre` WRITE;
/*!40000 ALTER TABLE `movie_genre` DISABLE KEYS */;
INSERT INTO `movie_genre` VALUES (1,1),(3,2),(3,3),(2,4);
/*!40000 ALTER TABLE `movie_genre` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `narration`
--

DROP TABLE IF EXISTS `narration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `narration` (
  `narration_id` int NOT NULL AUTO_INCREMENT,
  `content` text NOT NULL,
  `actor_id` int DEFAULT NULL,
  `movie_id` int DEFAULT NULL,
  PRIMARY KEY (`narration_id`),
  KEY `actor_id` (`actor_id`),
  KEY `movie_id` (`movie_id`),
  CONSTRAINT `narration_ibfk_1` FOREIGN KEY (`actor_id`) REFERENCES `actor` (`actor_id`) ON DELETE SET NULL,
  CONSTRAINT `narration_ibfk_2` FOREIGN KEY (`movie_id`) REFERENCES `movie` (`movie_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `narration`
--

LOCK TABLES `narration` WRITE;
/*!40000 ALTER TABLE `narration` DISABLE KEYS */;
INSERT INTO `narration` VALUES (1,'杩欐槸涓€涓濂囩殑涓栫晫銆?,1,1),(2,'姹熸箹鎭╂€ㄥ啀璧枫€?,2,2),(3,'Hope is a good thing, maybe the best of things.',5,3);
/*!40000 ALTER TABLE `narration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `production_company`
--

DROP TABLE IF EXISTS `production_company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `production_company` (
  `production_company_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  PRIMARY KEY (`production_company_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `production_company`
--

LOCK TABLES `production_company` WRITE;
/*!40000 ALTER TABLE `production_company` DISABLE KEYS */;
INSERT INTO `production_company` VALUES (1,'寰烽棿涔﹀簵','涓滀含'),(2,'涓奖闆嗗洟','鍖椾含'),(3,'Columbia Pictures','娲涙潐鐭?);
/*!40000 ALTER TABLE `production_company` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role` (
  `role_id` int NOT NULL AUTO_INCREMENT,
  `role_name` varchar(255) NOT NULL,
  `actor_id` int DEFAULT NULL,
  `movie_id` int DEFAULT NULL,
  PRIMARY KEY (`role_id`),
  KEY `actor_id` (`actor_id`),
  KEY `movie_id` (`movie_id`),
  CONSTRAINT `role_ibfk_1` FOREIGN KEY (`actor_id`) REFERENCES `actor` (`actor_id`) ON DELETE CASCADE,
  CONSTRAINT `role_ibfk_2` FOREIGN KEY (`movie_id`) REFERENCES `movie` (`movie_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (1,'鍗冨',1,1),(2,'鍒樻崟澶?,2,2),(3,'閲戞崟澶?,3,2),(4,'Andy Dufresne',4,3),(5,'Red',5,3);
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-20 21:20:54
