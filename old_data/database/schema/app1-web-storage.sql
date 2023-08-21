-- Adminer 4.8.1 MySQL 8.0.34 dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

DROP TABLE IF EXISTS `app1-web-storage`;
CREATE TABLE `app1-web-storage` (
  `_id` int NOT NULL AUTO_INCREMENT,
  `file_name` varchar(255) NOT NULL,
  `file_url` varchar(255) NOT NULL,
  PRIMARY KEY (`_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- 2023-08-16 09:06:17
