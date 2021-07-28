-- MySQL dump 10.13  Distrib 5.5.62, for Win64 (AMD64)
--
-- Host: localhost    Database: job_check
-- ------------------------------------------------------
-- Server version	5.5.5-10.5.10-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `cover_letter`
--

DROP TABLE IF EXISTS `cover_letter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cover_letter` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `job_app_id` int(10) unsigned NOT NULL,
  `cover_letter_file` text DEFAULT NULL,
  `created_at` date DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `cover_letter_un` (`user_id`,`job_app_id`),
  UNIQUE KEY `cover_letter_un1` (`cover_letter_file`) USING HASH,
  KEY `cover_letter_FK_1` (`job_app_id`),
  CONSTRAINT `cover_letter_FK` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `cover_letter_FK_1` FOREIGN KEY (`job_app_id`) REFERENCES `job_application` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cover_letter`
--

LOCK TABLES `cover_letter` WRITE;
/*!40000 ALTER TABLE `cover_letter` DISABLE KEYS */;
INSERT INTO `cover_letter` VALUES (5,6,17,'b0e0ead8e5c65392d29a_sample_cover_letter.pdf','2021-07-24'),(8,6,5,'c7460cec1149d21a4174_sample_cover_letter.pdf','2021-07-26');
/*!40000 ALTER TABLE `cover_letter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interview`
--

DROP TABLE IF EXISTS `interview`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `interview` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `job_app_id` int(10) unsigned NOT NULL,
  `interview_date` date NOT NULL,
  `interview_time` time NOT NULL,
  `interview_time_period` varchar(2) NOT NULL,
  `interview_time_zone` varchar(3) NOT NULL,
  `interview_type` varchar(30) DEFAULT '',
  `interview_location` varchar(50) DEFAULT '',
  `notes` varchar(255) DEFAULT '',
  `created_at` date DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `interview_FK` (`user_id`),
  KEY `interview_FK_1` (`job_app_id`),
  CONSTRAINT `interview_FK` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `interview_FK_1` FOREIGN KEY (`job_app_id`) REFERENCES `job_application` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interview`
--

LOCK TABLES `interview` WRITE;
/*!40000 ALTER TABLE `interview` DISABLE KEYS */;
INSERT INTO `interview` VALUES (14,6,17,'2021-09-16','01:00:00','PM','MST','Phone Interview','','','2021-07-23'),(16,6,17,'2021-07-26','11:00:00','AM','MST',NULL,'','','2021-07-24'),(17,6,5,'2021-07-26','11:15:00','AM','EST',NULL,'','','2021-07-24'),(18,6,12,'2021-07-09','04:00:00','PM','PST',NULL,'','','2021-07-24'),(19,6,13,'2021-07-19','06:00:00','PM','MST',NULL,'','','2021-07-24'),(21,6,15,'2021-07-26','10:30:00','AM','MST',NULL,'','','2021-07-24'),(22,6,15,'2021-07-29','01:00:00','PM','MST',NULL,'','','2021-07-24'),(23,6,15,'2021-07-03','08:30:00','AM','MST',NULL,'','','2021-07-24'),(24,6,13,'2021-07-21','01:00:00','PM','EST','','','','2021-07-26'),(25,6,13,'2021-07-30','11:00:00','PM','PST','','','','2021-07-26'),(26,6,13,'2021-07-28','02:30:00','PM','MST','','','','2021-07-27'),(27,6,18,'2021-07-27','01:00:00','PM','MST','In-Person','#5 - 123 Building Address','First Interview - Enter building through the North Entrance','2021-07-27'),(28,6,18,'2021-08-02','10:15:00','AM','MST','Phone','','','2021-07-27'),(29,6,18,'2021-08-09','03:00:00','PM','EST','Video Conference','Zoom Link','','2021-07-27');
/*!40000 ALTER TABLE `interview` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interviewer`
--

DROP TABLE IF EXISTS `interviewer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `interviewer` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `interview_id` int(10) unsigned NOT NULL,
  `job_app_id` int(10) unsigned NOT NULL,
  `name` varchar(50) NOT NULL,
  `job_position` varchar(50) DEFAULT '',
  `email` varchar(50) DEFAULT '',
  `phone_number` varchar(15) DEFAULT '',
  `other_contact_info` varchar(50) DEFAULT '',
  `notes` varchar(255) DEFAULT '',
  `created_at` date DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `interviewer_FK` (`user_id`),
  KEY `interviewer_FK_1` (`interview_id`),
  KEY `interviewer_FK_2` (`job_app_id`),
  CONSTRAINT `interviewer_FK` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `interviewer_FK_1` FOREIGN KEY (`interview_id`) REFERENCES `interview` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `interviewer_FK_2` FOREIGN KEY (`job_app_id`) REFERENCES `job_application` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interviewer`
--

LOCK TABLES `interviewer` WRITE;
/*!40000 ALTER TABLE `interviewer` DISABLE KEYS */;
/*!40000 ALTER TABLE `interviewer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `job_application`
--

DROP TABLE IF EXISTS `job_application`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `job_application` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `company` varchar(50) NOT NULL,
  `job_posting_url` text DEFAULT '',
  `job_position` varchar(50) NOT NULL,
  `job_location` varchar(50) DEFAULT '',
  `employment_type` varchar(30) DEFAULT '',
  `salary_type` varchar(20) DEFAULT '',
  `salary_amount` decimal(7,2) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `due_date` date DEFAULT NULL,
  `status` varchar(15) NOT NULL,
  `applied_date` date DEFAULT NULL,
  `notes` varchar(255) DEFAULT '',
  `created_at` date DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `job_application_FK` (`user_id`),
  CONSTRAINT `job_application_FK` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `job_application`
--

LOCK TABLES `job_application` WRITE;
/*!40000 ALTER TABLE `job_application` DISABLE KEYS */;
INSERT INTO `job_application` VALUES (5,6,'BIS Safety Software','https://ca.indeed.com/jobs?q=ux%20designer&l=Alberta&advn=1506843008921879&vjk=4878512fa8c8fc9f','Product Designer','Sherwood Park, AB','Full-Time','Yearly',50000.00,NULL,'2021-07-27','Applied','2021-07-31','Applied on the BIS Safety Software\'s website.','2021-07-20'),(8,3,'Company ABC',NULL,'Position ABC',NULL,NULL,NULL,NULL,NULL,NULL,'Applied',NULL,NULL,'2021-07-20'),(9,3,'Company XYZ',NULL,'Position XYZ',NULL,NULL,NULL,NULL,NULL,NULL,'Applied',NULL,NULL,'2021-07-20'),(10,3,'Company 123',NULL,'Position 123',NULL,NULL,NULL,NULL,NULL,NULL,'Not Applied',NULL,NULL,'2021-07-20'),(12,6,'Avanciers','https://ca.indeed.com/jobs?q=ux%20designer&l=Alberta&advn=393264691650981&vjk=9b01668f2b1d994c','UX Designer','Calgary, AB','Contract','',NULL,NULL,NULL,'Closed','2021-07-23','','2021-07-20'),(13,6,'Alcanna Inc.','https://ca.indeed.com/jobs?q=ux%20designer&l=Alberta&vjk=3da19e928973835b','Web Designer','Edmonton, AB','Full-Time','Hourly',20.00,'2021-08-16','2021-08-10','Applied','2021-07-26','Submitted application with resume and cover letter by email to hr@alcanna.com.','2021-07-20'),(15,6,'Graphite','https://ca.indeed.com/jobs?q=ux%20designer&l=Alberta&vjk=2b246cd4bf1226c7','Full Stack Engineer','Calgary, AB','Full-Time','Yearly',40000.00,NULL,NULL,'Applied',NULL,'','2021-07-20'),(17,6,'Yodify','https://ca.indeed.com/jobs?q=junior%20developer&l=Alberta&vjk=41700b5c340d2b03','Junior .NET Web Developer','Calgary, AB','Full-Time','Yearly',45000.00,NULL,'2021-07-28','Not Applied',NULL,'','2021-07-22'),(18,6,'Dro','https://ca.indeed.com/jobs?q=junior%20developer&l=Alberta&advn=4819684984092293&vjk=799987114c3d8873','Junior Software Developer','Edmonton, AB','Full-Time','Hourly',20.00,'2021-08-02','2021-07-30','Not Applied',NULL,'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Fusce id velit ut tortor pretium viverra suspendisse potenti. Euismod elementum nisi quis eleifend quam adipiscing vitae. Pharetra.','2021-07-25');
/*!40000 ALTER TABLE `job_application` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `job_reference`
--

DROP TABLE IF EXISTS `job_reference`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `job_reference` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `company_name` varchar(30) DEFAULT '',
  `reference_name` varchar(50) NOT NULL,
  `job_position` varchar(50) NOT NULL,
  `company_address` varchar(50) DEFAULT '',
  `postal_code` varchar(7) DEFAULT '',
  `city` varchar(50) NOT NULL,
  `province` varchar(50) NOT NULL,
  `email` varchar(50) DEFAULT '',
  `phone_number` varchar(15) DEFAULT '',
  `notes` varchar(255) DEFAULT '',
  `created_at` date DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `job_reference_FK` (`user_id`),
  CONSTRAINT `job_reference_FK` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `job_reference`
--

LOCK TABLES `job_reference` WRITE;
/*!40000 ALTER TABLE `job_reference` DISABLE KEYS */;
INSERT INTO `job_reference` VALUES (1,1,NULL,'Michael Hall','Merchandise Manager',NULL,NULL,'Calgary','AB','testemail@gmail.com','403-888-0099',NULL,'2021-07-13'),(3,1,NULL,'Deb Clarke','CEO',NULL,NULL,'Toronto','ON',NULL,NULL,NULL,'2021-07-14'),(4,6,NULL,'Joe Brown','Supervisor','','A1B 2D3','Toronto','ON','joe@company.com','','','2021-07-23'),(9,6,'University of Calgary','Jodi Mccarthy','Professor','',NULL,'Calgary','AB','','','Capstone Supervisor','2021-07-23'),(10,6,NULL,'Boyce Thomas','Reference Job Position','',NULL,'Calgary','AB','','','','2021-07-25'),(11,6,NULL,'Elnora Austin','Reference Job Position #2','',NULL,'Calgary','AB','','','','2021-07-25');
/*!40000 ALTER TABLE `job_reference` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `networking_connection`
--

DROP TABLE IF EXISTS `networking_connection`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `networking_connection` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `networking_event_id` int(10) unsigned NOT NULL,
  `name` varchar(50) NOT NULL,
  `company` varchar(50) DEFAULT '',
  `connection_role` varchar(50) DEFAULT '',
  `email` varchar(50) DEFAULT '',
  `phone_number` varchar(15) DEFAULT '',
  `linkedIn` text DEFAULT '',
  `website` text DEFAULT '',
  `other` varchar(255) DEFAULT '',
  `notes` varchar(255) DEFAULT '',
  `created_at` date DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `connection_FK` (`user_id`),
  KEY `connection_FK_1` (`networking_event_id`),
  CONSTRAINT `connection_FK` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `connection_FK_1` FOREIGN KEY (`networking_event_id`) REFERENCES `networking_event` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `networking_connection`
--

LOCK TABLES `networking_connection` WRITE;
/*!40000 ALTER TABLE `networking_connection` DISABLE KEYS */;
INSERT INTO `networking_connection` VALUES (1,1,1,'Sally Stone',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2021-07-14'),(2,1,1,'Joe Manning','Company ABC','Team Lead','testingemail@gmail.com',NULL,NULL,NULL,NULL,'Met at career fair. Spoke about the culture fit at Company ABC.','2021-07-14'),(11,6,8,'John Doe','Company XYZ','Hiring Manager','joe@company.com','4031234567','https://www.google.ca/','https://www.google.ca/','https://www.google.ca/','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Fusce id velit ut tortor pretium viverra suspendisse potenti. Euismod elementum nisi quis eleifend quam adipiscing vitae. Pharetra.','2021-07-27'),(12,6,8,'Jane Doe','Company XYZ','Supervisor','jane@company.com','4035555555','https://www.linkedin.com/','https://www.google.ca/','Other Contact Information','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Fusce id velit ut tortor pretium viverra suspendisse potenti. Euismod elementum nisi quis eleifend quam adipiscing vitae. Pharetra.','2021-07-27');
/*!40000 ALTER TABLE `networking_connection` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `networking_event`
--

DROP TABLE IF EXISTS `networking_event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `networking_event` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `status` varchar(10) NOT NULL,
  `event_name` varchar(50) NOT NULL,
  `event_date` date NOT NULL,
  `start_time` time NOT NULL,
  `start_time_period` varchar(2) NOT NULL,
  `end_time` time DEFAULT NULL,
  `end_time_period` varchar(2) DEFAULT '',
  `time_zone` varchar(3) NOT NULL,
  `event_type` varchar(30) DEFAULT '',
  `event_location` varchar(50) DEFAULT '',
  `notes` varchar(255) DEFAULT '',
  `created_at` date DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `networking_event_FK` (`user_id`),
  CONSTRAINT `networking_event_FK` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `networking_event`
--

LOCK TABLES `networking_event` WRITE;
/*!40000 ALTER TABLE `networking_event` DISABLE KEYS */;
INSERT INTO `networking_event` VALUES (1,1,'Upcoming','ECO Canada Virtual Career Fair','2021-06-23','12:00:00','PM',NULL,NULL,'MDT',NULL,NULL,NULL,'2021-07-14'),(3,1,'Attended','University of Calgary Winter Career Fair 2021','2020-02-15','10:00:00','AM',NULL,NULL,'MDT',NULL,NULL,NULL,'2021-07-14'),(6,6,'Attended','Meetup Group','2021-07-31','12:00:00','PM','01:00:00','PM','MST','','','','2021-07-23'),(7,6,'Upcoming','Industry Presentation','2021-09-14','04:00:00','PM',NULL,'PM','MST','','','','2021-07-23'),(8,6,'Upcoming','Company XYZ\'s Networking Event','2021-07-12','06:00:00','PM',NULL,'','EST','','','','2021-07-23');
/*!40000 ALTER TABLE `networking_event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `resume`
--

DROP TABLE IF EXISTS `resume`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `resume` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `job_app_id` int(10) unsigned NOT NULL,
  `resume_file` text DEFAULT NULL,
  `created_at` date DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `resume_un` (`user_id`,`job_app_id`),
  UNIQUE KEY `resume_un1` (`resume_file`) USING HASH,
  KEY `resume_FK_1` (`job_app_id`),
  CONSTRAINT `resume_FK` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `resume_FK_1` FOREIGN KEY (`job_app_id`) REFERENCES `job_application` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resume`
--

LOCK TABLES `resume` WRITE;
/*!40000 ALTER TABLE `resume` DISABLE KEYS */;
INSERT INTO `resume` VALUES (39,6,17,'0da711c8a725f9ec2828_sample_resume.pdf','2021-07-24');
/*!40000 ALTER TABLE `resume` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_session`
--

DROP TABLE IF EXISTS `user_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_session` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `token` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_session_un` (`token`),
  KEY `user_session_FK` (`user_id`),
  CONSTRAINT `user_session_FK` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_session`
--

LOCK TABLES `user_session` WRITE;
/*!40000 ALTER TABLE `user_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(150) NOT NULL,
  `salt` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_un` (`email`),
  CONSTRAINT `users_check` CHECK (char_length(`password`) >= 8)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Emily','Grace','emilygrace@gmail.com','95d168c08a234c6f454a38f58962fa1789e2b0490d8b4e91f20c1d905ea3ed96f54dbb7739783d2b90d943986cd9432ebec3f9591f53804e2b8648c00a8e67a0','xG39V7rsIg'),(3,'Rebecca','James','rebeccajames@gmail.com','af6c68eeb35f904e56ecef0f5bd5161e40c3fd980ed174969a40320cb21b06d36020bfbc185b79b2cace47b7ee16d407a379ea114c644c098e45fc8994bf65e4','9ouCXb2qmu'),(4,'Jen','Clarke','jen_clarke@gmail.com','08bdc8f84e6f33e55026a19f265e887365b39647b753fe98668d1df4e70dbada03b8e92804cb3814a71413905a438b53824e9487d9bac5c3d6cf47363566099b','E0XP6dqKSl'),(6,'Sophie','Henderson','sophiehenderson@gmail.com','f31a8422140c189ebdc8e36839b6dbfd5349b17fb56cfa6c285eb1aa6ed882022697ffb66cafc2f312439ba4008ad91ccbb97511e35ca8c2287d5b3c9f3e9b73','A6Rd3QfCct');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'job_check'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-07-27 20:44:33
