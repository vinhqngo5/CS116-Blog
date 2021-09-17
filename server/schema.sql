CREATE SCHEMA `blog` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE `blog`.`user` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `firstName` VARCHAR(50) NULL DEFAULT NULL,
  `lastName` VARCHAR(50) NULL DEFAULT NULL,
  `email` VARCHAR(50) NOT NULL,
  `slug` VARCHAR(50) NOT NULL,
  `registeredAt` DATETIME NOT NULL,
  `lastLogin` DATETIME NULL DEFAULT NULL,
  `avatarLink` VARCHAR(100) NULL DEFAULT NULL,
  `intro` TINYTEXT NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `uq_email` (`email` ASC) );
  
  
CREATE TABLE `blog`.`post` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `authorId` BIGINT NOT NULL,
  `title` VARCHAR(75) NOT NULL,
  `subtitle` VARCHAR(75) NOT NULL,
  `bannerLink` VARCHAR(100) NULL DEFAULT NULL,
  `slug` VARCHAR(100) NOT NULL,
  `summary` TINYTEXT NOT NULL,
  `published` TINYINT(1) NOT NULL DEFAULT 0,
  `createdAt` DATETIME NOT NULL,
  `updatedAt` DATETIME NULL DEFAULT NULL,
  `publishedAt` DATETIME NULL DEFAULT NULL,
  `content` TEXT NULL DEFAULT NULL,
  `like` INT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `uq_slug` (`slug` ASC),
  INDEX `idx_post_user` (`authorId` ASC),
  CONSTRAINT `fk_post_user`
    FOREIGN KEY (`authorId`)
    REFERENCES `blog`.`user` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION);

CREATE TABLE `blog`.`user_like_post` (
  `userId` BIGINT NOT NULL,
  `postId` BIGINT NOT NULL,
  PRIMARY KEY (`userId`, `postId`),
  CONSTRAINT `fk_user_like_post_user`
    FOREIGN KEY (`userId`)
    REFERENCES `blog`.`user` (`id`)
    ON DELETE CASCADE 
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_user_like_post_post`
    FOREIGN KEY (`postId`)
    REFERENCES `blog`.`post` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION);

CREATE TABLE `blog`.`post_comment` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `postId` BIGINT NOT NULL,
  `parentId` BIGINT NULL DEFAULT NULL,
  `authorId` BIGINT NOT NULL,
  `title` VARCHAR(100) NOT NULL,
  `createdAt` DATETIME NOT NULL,
  `content` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `idx_comment_post` (`postId` ASC),
  CONSTRAINT `fk_comment_post`
    FOREIGN KEY (`postId`)
    REFERENCES `blog`.`post` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  INDEX `idx_comment_author` (`authorId` ASC),
  CONSTRAINT `fk_comment_author`
    FOREIGN KEY (`authorId`)
    REFERENCES `blog`.`user` (`id`)
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION);

ALTER TABLE `blog`.`post_comment` 
ADD INDEX `idx_comment_parent` (`parentId` ASC);
ALTER TABLE `blog`.`post_comment` 
ADD CONSTRAINT `fk_comment_parent`
  FOREIGN KEY (`parentId`)
  REFERENCES `blog`.`post_comment` (`id`)
  ON DELETE CASCADE
  ON UPDATE NO ACTION;
  
