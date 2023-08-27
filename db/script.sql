-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema series_schema
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema series_schema
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `series_schema` ;
USE `series_schema` ;

-- -----------------------------------------------------
-- Table `series_schema`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `series_schema`.`users` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(155) NOT NULL,
  `last_name` VARCHAR(155) NOT NULL,
  `email` VARCHAR(155) NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `series_schema`.`series`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `series_schema`.`series` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NOT NULL,
  `network` VARCHAR(155) NOT NULL,
  `release_date` DATE NOT NULL,
  `description` LONGTEXT NOT NULL,
  `user_id` INT UNSIGNED NOT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `fk_series_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_series_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `series_schema`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
