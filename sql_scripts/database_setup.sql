DROP DATABASE IF EXISTS `remixd`;
CREATE DATABASE `remixd`;
USE `remixd`;

DROP TABLE IF EXISTS `Account`;
CREATE TABLE `Account` (
	ID int NOT NULL AUTO_INCREMENT,
    Name varchar(20) NOT NULL,
    isAdmin boolean NOT NULL default FALSE,
    Email varchar(255) NOT NULL,
    Password varchar(255) NOT NULL,
    Bio varchar(127),
    PFP varchar(255),
    modFlags bit(8) NOT NULL default 0,
    modComment varchar(127),
    PRIMARY KEY (ID)
);

DROP TABLE IF EXISTS `Review`;
CREATE TABLE `Review` (
	AccountID int NOT NULL,
    AlbumID int NOT NULL,
    timestamp timestamp NOT NULL default CURRENT_TIMESTAMP,
    Score tinyint NOT NULL,
    Liked Boolean NOT NULL,
    Content varchar(127),
    FOREIGN KEY (AccountID) REFERENCES Account(ID),
    PRIMARY KEY (AccountID,AlbumID)
);

DROP TABLE IF EXISTS `Tags`;
CREATE TABLE `Tags` (
	AccountID int NOT NULL,
    ReviewAccountID int NOT NULL,
    ReviewAlbumID int NOT NULL,
    info bit(8) NOT NULL,
    FOREIGN KEY (AccountID) REFERENCES Account(ID),
    FOREIGN KEY (ReviewAccountID, ReviewAlbumID) REFERENCES Review(AccountID, AlbumID),
    PRIMARY KEY (AccountID,ReviewAccountID,ReviewAlbumID)
);

DROP TABLE IF EXISTS `Tokens`;
CREATE TABLE `Tokens` (
	SessionID bigint NOT NULL,
    AccountID int NOT NULL,
    timestamp timestamp NOT NULL default CURRENT_TIMESTAMP,
    PRIMARY KEY (SessionID),
    FOREIGN KEY (AccountID) REFERENCES Account(ID)
);