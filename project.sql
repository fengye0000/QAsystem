CREATE TABLE `raw_data`.`projects`  (
  `project_name` varchar(100) NOT NULL,
  `degree` varchar(100) NULL,
  `duration` varchar(100) NULL,
  `start` varchar(100) NULL,
  `ucas` varchar(100) Not NULL,
  `institution_code` varchar(100) NULL,
  `typical_Alevel_offer` text NULL,
  `uk_fees` varchar(100) NULL,
  `international_fees` varchar(100) NULL,
  `entry_requirement` text NULL,
  `cataglory` varchar(100) NULL,
  `school` varchar(200) NULL,
	`program` varchar(200) NULL,
  PRIMARY KEY (`ucas`)
);