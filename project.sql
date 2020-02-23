/*
 Navicat Premium Data Transfer

 Source Server         : qasys
 Source Server Type    : MySQL
 Source Server Version : 50729
 Source Host           : 106.53.84.119:3306
 Source Schema         : raw_data

 Target Server Type    : MySQL
 Target Server Version : 50729
 File Encoding         : 65001

 Date: 23/02/2020 00:40:57
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for project
-- ----------------------------
DROP TABLE IF EXISTS `project`;
CREATE TABLE `project` (
  `project_name` varchar(100) NOT NULL,
  `degree` varchar(100) DEFAULT NULL,
  `duration` varchar(100) DEFAULT NULL,
  `start` varchar(100) DEFAULT NULL,
  `ucas` varchar(100) NOT NULL,
  `institution_code` varchar(100) DEFAULT NULL,
  `typical_Alevel_offer` text,
  `uk_fees` varchar(100) DEFAULT NULL,
  `international_fees` varchar(100) DEFAULT NULL,
  `entry_requirement` text,
  `cataglory` varchar(100) DEFAULT NULL,
  `school` varchar(200) DEFAULT NULL,
  `program` varchar(200) DEFAULT NULL,
  `courses` text,
  PRIMARY KEY (`ucas`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
