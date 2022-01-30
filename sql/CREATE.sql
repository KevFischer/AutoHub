
CREATE TABLE `account` (
  `email` varchar(128) NOT NULL,
  `username` varchar(16) NOT NULL,
  `password` varchar(512) NOT NULL,
  `phone` varchar(32) NOT NULL,
  `member_since` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

ALTER TABLE `autohub`.`account` 
ADD COLUMN `image_url` VARCHAR(512) NULL AFTER `member_since`;
ALTER TABLE `autohub`.`account` 
CHANGE COLUMN `image_url` `image_url` VARCHAR(512) NULL DEFAULT 'https://res.cloudinary.com/autohubstorage/image/upload/v1643560393/blank-profile-picture-973460_960_720_dmzcen.webp' ;


CREATE TABLE `offer` (
  `offerID` int NOT NULL AUTO_INCREMENT,
  `account` varchar(128) NOT NULL,
  `brand` varchar(32) NOT NULL,
  `model` varchar(32) NOT NULL,
  `price` float NOT NULL,
  `dateAdded` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `firstRegistration` datetime DEFAULT NULL,
  `mileage` int NOT NULL,
  `fuelType` varchar(16) NOT NULL,
  `location` varchar(128) NOT NULL,
  `roadworthy` varchar(32) NOT NULL,
  `description` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`offerID`),
  KEY `email_idx` (`account`),
  CONSTRAINT `offer_account` FOREIGN KEY (`account`) REFERENCES `account` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `token` (
  `token` varchar(512) NOT NULL,
  `account` varchar(128) NOT NULL,
  `expire` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`token`),
  KEY `email_idx` (`account`),
  CONSTRAINT `email` FOREIGN KEY (`account`) REFERENCES `account` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `message` (
  `messageID` int NOT NULL AUTO_INCREMENT,
  `sender` varchar(128) NOT NULL,
  `receiver` varchar(128) NOT NULL,
  `offer` int NOT NULL,
  `testDrive` datetime DEFAULT NULL,
  `message` varchar(512) NOT NULL,
  PRIMARY KEY (`messageID`),
  KEY `msg_sender_idx` (`sender`),
  KEY `msg_receiver_idx` (`receiver`),
  KEY `msg_offer_idx` (`offer`),
  CONSTRAINT `msg_offer` FOREIGN KEY (`offer`) REFERENCES `offer` (`offerID`),
  CONSTRAINT `msg_receiver` FOREIGN KEY (`receiver`) REFERENCES `account` (`email`),
  CONSTRAINT `msg_sender` FOREIGN KEY (`sender`) REFERENCES `account` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `event` (
  `eventID` int NOT NULL AUTO_INCREMENT,
  `creator` varchar(128) NOT NULL,
  `eventname` varchar(64) NOT NULL,
  `location` varchar(128) NOT NULL,
  `appointment` datetime DEFAULT NULL,
  `maxAttendants` int DEFAULT NULL,
  PRIMARY KEY (`eventID`),
  KEY `event_account_idx` (`creator`),
  CONSTRAINT `event_account` FOREIGN KEY (`creator`) REFERENCES `account` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

ALTER TABLE `autohub`.`event` 
ADD COLUMN `description` VARCHAR(512) NULL AFTER `maxAttendants`;

CREATE TABLE `account_event` (
  `account` varchar(128) NOT NULL,
  `event` int DEFAULT NULL,
  KEY `participant_event_idx` (`account`),
  KEY `event_participants_idx` (`event`),
  CONSTRAINT `event_participants` FOREIGN KEY (`event`) REFERENCES `event` (`eventID`),
  CONSTRAINT `participant_event` FOREIGN KEY (`account`) REFERENCES `account` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `forumpost` (
  `postID` int NOT NULL AUTO_INCREMENT,
  `account` varchar(128) NOT NULL,
  `postedAt` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `topic` varchar(64) NOT NULL,
  `content` varchar(1024) NOT NULL,
  PRIMARY KEY (`postID`),
  KEY `post_account_idx` (`account`),
  CONSTRAINT `post_account` FOREIGN KEY (`account`) REFERENCES `account` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `forumpostanswer` (
  `answerID` int NOT NULL AUTO_INCREMENT,
  `post` int NOT NULL,
  `account` varchar(128) NOT NULL,
  `postedAt` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `content` varchar(1024) NOT NULL,
  `upvotes` int DEFAULT NULL,
  PRIMARY KEY (`answerID`),
  KEY `ansewer_post_idx` (`post`),
  KEY `answer_account_idx` (`account`),
  CONSTRAINT `ansewer_post` FOREIGN KEY (`post`) REFERENCES `forumpost` (`postID`),
  CONSTRAINT `answer_account` FOREIGN KEY (`account`) REFERENCES `account` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `offer_images` (
  `offer` int NOT NULL,
  `url` varchar(512) NOT NULL,
  KEY `offer_images_offer_idx` (`offer`),
  CONSTRAINT `offer_images_offer` FOREIGN KEY (`offer`) REFERENCES `offer` (`offerID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
