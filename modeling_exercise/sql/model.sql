-- MySQL Script generated by MySQL Workbench
-- Mon Aug  1 03:52:09 2022
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`Member`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Member` (
  `member_id` INT NOT NULL,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `phone_number` VARCHAR(45) NULL,
  `is_email_confirmed` TINYINT NOT NULL DEFAULT 0,
  `is_phone_confirmed` TINYINT NOT NULL DEFAULT 0,
  PRIMARY KEY (`member_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`City`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`City` (
  `city_id` INT NOT NULL,
  `city_name` VARCHAR(45) NOT NULL,
  `region` VARCHAR(45) NOT NULL,
  `country` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`city_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Stops`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Stops` (
  `stop_id` INT NOT NULL,
  `city_id` INT NOT NULL,
  `address` VARCHAR(150) NOT NULL,
  `latitude` DECIMAL NOT NULL,
  `longitude` DECIMAL NOT NULL,
  `is_origin` TINYINT NOT NULL,
  `is_destination` TINYINT NOT NULL,
  PRIMARY KEY (`stop_id`),
  INDEX `fk_Route_has_City_City1_idx` (`city_id` ASC) VISIBLE,
  CONSTRAINT `fk_city_id`
    FOREIGN KEY (`city_id`)
    REFERENCES `mydb`.`City` (`city_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Trip`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Trip` (
  `trip_id` INT auto_increment NOT NULL,
  `trip_owner_id` INT NOT NULL,
  `origin` INT NOT NULL,
  `destination` INT NOT NULL,
  `trip_date` DATE NOT NULL,
  `trip_time` TIME NOT NULL,
  `nb_seats_offered` SMALLINT NOT NULL,
  `nb_seats_available` SMALLINT NOT NULL,
  `price_per_seat` DECIMAL NULL,
  `is_published` TINYINT NOT NULL DEFAULT 0,
  `date_published` DATETIME NULL,
  `trip_duration_minutes` INT NULL,
  `distance_km` DECIMAL NULL,
  `main_road` VARCHAR(50) NULL,
  `date_created` DATETIME NOT NULL,
  `date_updated` DATETIME NULL,
  PRIMARY KEY (`trip_id`),
  INDEX `fk_Trip_member1_idx` (`trip_owner_id` ASC) VISIBLE,
  INDEX `fk_Trip_Stops1_idx` (`origin` ASC) VISIBLE,
  INDEX `fk_Trip_Stops2_idx` (`destination` ASC) VISIBLE,
  CONSTRAINT `fk_trip_owner_id`
    FOREIGN KEY (`trip_owner_id`)
    REFERENCES `mydb`.`Member` (`member_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_origin`
    FOREIGN KEY (`origin`)
    REFERENCES `mydb`.`Stops` (`stop_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_destination`
    FOREIGN KEY (`destination`)
    REFERENCES `mydb`.`Stops` (`stop_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`member_request`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`member_request` (
  `request_id` INT auto_increment NOT NULL,
  `member_id` INT NOT NULL,
  `trip_id` INT NOT NULL,
  `from_stop_id` INT NOT NULL,
  `to_stop_id` INT NOT NULL,
  `prorated_price` DECIMAL NULL,
  `request_status` TINYINT NULL,
  `request_reason` VARCHAR(200) NULL,
  `trip_duration_minutes` INT NULL,
  `distance_km` DECIMAL NULL,
  INDEX `fk_Member_has_Trip_Offer_Member1_idx` (`member_id` ASC) VISIBLE,
  INDEX `fk_Member_request_Trip_Offer_Stops1_idx` (`from_stop_id` ASC) VISIBLE,
  INDEX `fk_Member_request_Trip_Offer_Stops2_idx` (`to_stop_id` ASC) VISIBLE,
  PRIMARY KEY (`request_id`),
  INDEX `fk_member_request_trip_idx` (`trip_id` ASC) VISIBLE,
  CONSTRAINT `fk_requester_id`
    FOREIGN KEY (`member_id`)
    REFERENCES `mydb`.`Member` (`member_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_from_stop_id`
    FOREIGN KEY (`from_stop_id`)
    REFERENCES `mydb`.`Stops` (`stop_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_to_stop_id`
    FOREIGN KEY (`to_stop_id`)
    REFERENCES `mydb`.`Stops` (`stop_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_trip_id`
    FOREIGN KEY (`trip_id`)
    REFERENCES `mydb`.`Trip` (`trip_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`additional_stops`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`additional_stops` (
  `id` INT auto_increment NOT NULL,
  `trip_id` INT NOT NULL,
  `stop_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_Trip_has_Stops_Stops1_idx` (`stop_id` ASC) VISIBLE,
  INDEX `fk_Trip_has_Stops_Trip1_idx` (`trip_id` ASC) VISIBLE,
  CONSTRAINT `fk_trip_id2`
    FOREIGN KEY (`trip_id`)
    REFERENCES `mydb`.`Trip` (`trip_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_stop_id`
    FOREIGN KEY (`stop_id`)
    REFERENCES `mydb`.`Stops` (`stop_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
