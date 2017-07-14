-- MySQL dump 10.13  Distrib 5.6.19, for linux-glibc2.5 (x86_64)
--
-- Host: localhost    Database: pureftpd
-- ------------------------------------------------------
-- Server version	5.6.19-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin` (
  `Username` varchar(35) NOT NULL,
  `Password` char(100) NOT NULL DEFAULT '',
  `Email` varchar(32) DEFAULT '',
  `Add_time` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_admin_Username` (`Username`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES ('admin','7c4a8d09ca3762af61e59520943dc26494f8941b','','2016-06-27 21:50:36',1),('xixi','f7c3bc1d808e04732adf679965ccc34ca7ae3441','','2016-06-28 13:02:38',2);
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `category` (
  `catname` varchar(255) DEFAULT NULL,
  `parentid` int(11) DEFAULT '0',
  `url` varchar(255) DEFAULT NULL,
  `isshow` tinyint(1) NOT NULL DEFAULT '1',
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `catname` (`catname`),
  KEY `ix_category_parentid` (`parentid`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES ('系统管理',0,'',1,1),('导航菜单管理',1,'/menus/list',1,2),('ftp管理',0,'',1,3),('ftp用户管理',3,'/pureftpd/list',1,4),('管理员管理',1,'/admin/list',1,5),('ftp主机管理',3,'/pureftpd/hosts',1,6),('ftp用户组管理',3,'/pureftpd/groups',1,7),('11111',1,'/test',0,8);
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ftphosts`
--

DROP TABLE IF EXISTS `ftphosts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ftphosts` (
  `HostName` varchar(32) NOT NULL,
  `HostIp` varchar(32) NOT NULL,
  `FtpPort` int(11) NOT NULL DEFAULT '22',
  `Comment` text,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_ftphosts_HostName` (`HostName`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ftphosts`
--

LOCK TABLES `ftphosts` WRITE;
/*!40000 ALTER TABLE `ftphosts` DISABLE KEYS */;
INSERT INTO `ftphosts` VALUES ('pureftp1','192.168.4.92',21,'',1),('pureftp2','192.168.4.94',21,'',3),('192.168.4.114','192.168.4.114',21,'',4);
/*!40000 ALTER TABLE `ftphosts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ftphosts_ftpusers_users`
--

DROP TABLE IF EXISTS `ftphosts_ftpusers_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ftphosts_ftpusers_users` (
  `ftphosts_id` int(11) DEFAULT NULL,
  `ftpusers_id` int(11) DEFAULT NULL,
  UNIQUE KEY `ftphosts_ftpusers_Users_mindx` (`ftphosts_id`,`ftpusers_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ftphosts_ftpusers_users`
--

LOCK TABLES `ftphosts_ftpusers_users` WRITE;
/*!40000 ALTER TABLE `ftphosts_ftpusers_users` DISABLE KEYS */;
INSERT INTO `ftphosts_ftpusers_users` VALUES (1,1),(1,7),(1,9),(1,11),(1,15),(1,16),(3,1),(3,5),(3,6),(3,9),(3,11),(4,1),(4,7),(4,9),(4,11),(4,15),(4,16);
/*!40000 ALTER TABLE `ftphosts_ftpusers_users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ftpusergroup`
--

DROP TABLE IF EXISTS `ftpusergroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ftpusergroup` (
  `GroupName` varchar(32) NOT NULL,
  `Comment` text,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_ftpusergroup_GroupName` (`GroupName`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ftpusergroup`
--

LOCK TABLES `ftpusergroup` WRITE;
/*!40000 ALTER TABLE `ftpusergroup` DISABLE KEYS */;
INSERT INTO `ftpusergroup` VALUES ('运维组','这是运维组',1),('测试','',3);
/*!40000 ALTER TABLE `ftpusergroup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ftpusergroup_ftpusers_users`
--

DROP TABLE IF EXISTS `ftpusergroup_ftpusers_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ftpusergroup_ftpusers_users` (
  `ftpusergroup_id` int(11) DEFAULT NULL,
  `ftpusers_id` int(11) DEFAULT NULL,
  UNIQUE KEY `ftpusergroup_ftpusers_Users_mindx` (`ftpusergroup_id`,`ftpusers_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ftpusergroup_ftpusers_users`
--

LOCK TABLES `ftpusergroup_ftpusers_users` WRITE;
/*!40000 ALTER TABLE `ftpusergroup_ftpusers_users` DISABLE KEYS */;
INSERT INTO `ftpusergroup_ftpusers_users` VALUES (1,1),(1,6);
/*!40000 ALTER TABLE `ftpusergroup_ftpusers_users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ftpusers`
--

DROP TABLE IF EXISTS `ftpusers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ftpusers` (
  `User` varchar(16) NOT NULL,
  `Password` varchar(32) DEFAULT '',
  `Uid` int(11) NOT NULL DEFAULT '1000',
  `Gid` int(11) NOT NULL DEFAULT '1000',
  `Dir` varchar(128) NOT NULL DEFAULT '',
  `QuotaFiles` int(11) NOT NULL DEFAULT '0',
  `QuotaSize` int(11) NOT NULL DEFAULT '0',
  `ULBandwidth` int(11) NOT NULL DEFAULT '0',
  `DLBandwidth` int(11) NOT NULL DEFAULT '0',
  `Ipaddress` varchar(15) NOT NULL DEFAULT '*',
  `Status` tinyint(1) NOT NULL DEFAULT '1',
  `RLRatio` smallint(6) NOT NULL DEFAULT '1',
  `DLRatio` smallint(6) NOT NULL DEFAULT '1',
  `Comment` text,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_ftpusers_User` (`User`)
) ENGINE=MyISAM AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ftpusers`
--

LOCK TABLES `ftpusers` WRITE;
/*!40000 ALTER TABLE `ftpusers` DISABLE KEYS */;
INSERT INTO `ftpusers` VALUES ('abcd','25f9e794323b453885f5181f1b624d0b',1000,1000,'/home/abdd',0,0,0,0,'*',1,10,1,'这是测试账号1',1),('test1','25f9e794323b453885f5181f1b624d0b',1000,1000,'',0,0,0,0,'*',1,1,1,'',5),('test2','25f9e794323b453885f5181f1b624d0b',1000,1000,'',0,0,0,0,'*',1,1,1,'',6),('test3','25f9e794323b453885f5181f1b624d0b',1000,1000,'/home/abdd',0,0,0,0,'*',1,1,1,'',7),('test4','25f9e794323b453885f5181f1b624d0b',1000,1000,'',0,0,0,0,'*',1,1,1,'',8),('test5','25f9e794323b453885f5181f1b624d0b',1000,1000,'',0,0,0,0,'*',1,1,1,'',9),('test6','25f9e794323b453885f5181f1b624d0b',1000,1000,'',0,0,0,0,'*',1,1,1,'',10),('test7','25f9e794323b453885f5181f1b624d0b',1000,1000,'',0,0,0,0,'*',1,1,1,'',11),('test8','25f9e794323b453885f5181f1b624d0b',1000,1000,'',0,0,0,0,'*',1,1,1,'',12),('test9','25f9e794323b453885f5181f1b624d0b',1000,1000,'',0,0,0,0,'*',1,1,1,'',13),('test10','25f9e794323b453885f5181f1b624d0b',1000,1000,'',0,0,0,0,'*',1,1,1,'',14),('xixi','e10adc3949ba59abbe56e057f20f883e',1000,1000,'/ftpdata/test',0,0,0,0,'*',1,1,1,'',15),('xixi3','25f9e794323b453885f5181f1b624d0b',1000,1000,'/ftpdata/test',0,0,0,0,'5.45.54.45',1,1,1,'',16);
/*!40000 ALTER TABLE `ftpusers` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-07-14 15:52:57
