CREATE SCHEMA `blog` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE `blog`.`user` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `firstName` VARCHAR(50) NULL DEFAULT NULL,
  `middleName` VARCHAR(50) NULL DEFAULT NULL,
  `lastName` VARCHAR(50) NULL DEFAULT NULL,
  `mobile` VARCHAR(15) NULL,
  `email` VARCHAR(50) NULL,
  `tokenId` VARCHAR(32) NULL DEFAULT NULL,
  `registeredAt` DATETIME NOT NULL,
  `lastLogin` DATETIME NULL DEFAULT NULL,
  `intro` TINYTEXT NULL DEFAULT NULL,
  `profile` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `uq_mobile` (`mobile` ASC),
  UNIQUE INDEX `uq_email` (`email` ASC) );
  
  
CREATE TABLE `blog`.`post` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `authorId` BIGINT NOT NULL,
  `parentId` BIGINT NULL DEFAULT NULL,
  `title` VARCHAR(75) NOT NULL,
  `metaTitle` VARCHAR(100) NULL,
  `slug` VARCHAR(100) NOT NULL,
  `summary` TINYTEXT NULL,
  `published` TINYINT(1) NOT NULL DEFAULT 0,
  `createdAt` DATETIME NOT NULL,
  `updatedAt` DATETIME NULL DEFAULT NULL,
  `publishedAt` DATETIME NULL DEFAULT NULL,
  `content` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `uq_slug` (`slug` ASC),
  INDEX `idx_post_user` (`authorId` ASC),
  CONSTRAINT `fk_post_user`
    FOREIGN KEY (`authorId`)
    REFERENCES `blog`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

ALTER TABLE `blog`.`post` 
ADD INDEX `idx_post_parent` (`parentId` ASC);
ALTER TABLE `blog`.`post` 
ADD CONSTRAINT `fk_post_parent`
  FOREIGN KEY (`parentId`)
  REFERENCES `blog`.`post` (`id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;
  
  



CREATE TABLE `blog`.`post_comment` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `postId` BIGINT NOT NULL,
  `parentId` BIGINT NULL DEFAULT NULL,
  `title` VARCHAR(100) NOT NULL,
  `published` TINYINT(1) NOT NULL DEFAULT 0,
  `createdAt` DATETIME NOT NULL,
  `publishedAt` DATETIME NULL DEFAULT NULL,
  `content` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `idx_comment_post` (`postId` ASC),
  CONSTRAINT `fk_comment_post`
    FOREIGN KEY (`postId`)
    REFERENCES `blog`.`post` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

ALTER TABLE `blog`.`post_comment` 
ADD INDEX `idx_comment_parent` (`parentId` ASC);
ALTER TABLE `blog`.`post_comment` 
ADD CONSTRAINT `fk_comment_parent`
  FOREIGN KEY (`parentId`)
  REFERENCES `blog`.`post_comment` (`id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;
  
