-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema rasdb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema rasdb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `rasdb` DEFAULT CHARACTER SET utf8 ;
USE `rasdb` ;

-- -----------------------------------------------------
-- Table `rasdb`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `rasdb`.`user` (
  `email` VARCHAR(45) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  `IBAN` VARCHAR(45) NOT NULL,
  `aniversario` DATE NOT NULL,
  `cc` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`email`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `rasdb`.`jogo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `rasdb`.`jogo` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `desporto` VARCHAR(45) NOT NULL,
  `odd_vitoriaCasa` FLOAT NOT NULL,
  `odd_empate` FLOAT NULL,
  `odd_vitoriaVisitante` FLOAT NOT NULL,
  `equipaCasa` VARCHAR(45) NOT NULL,
  `equipaVisitante` VARCHAR(45) NOT NULL,
  `horario` DATETIME NOT NULL,
  `estado_apostavel` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `rasdb`.`bet`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `rasdb`.`bet` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `jogo_id` INT NOT NULL,
  `odd` FLOAT NOT NULL,
  `equipaEscolhida` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`, `jogo_id`),
  INDEX `fk_bet_jogo_idx` (`jogo_id` ASC) VISIBLE,
  CONSTRAINT `fk_bet_jogo`
    FOREIGN KEY (`jogo_id`)
    REFERENCES `rasdb`.`jogo` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `rasdb`.`Boletim`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `rasdb`.`Boletim` (
  `user_email` VARCHAR(45) NOT NULL,
  `bet_id` INT NOT NULL,
  `id` INT NOT NULL,
  `valor` FLOAT NOT NULL,
  `total_odd` FLOAT NOT NULL,
  `estado` VARCHAR(45) NOT NULL,
  `moeda` VARCHAR(45) NOT NULL,
  INDEX `fk_Boletim_user1_idx` (`user_email` ASC) VISIBLE,
  INDEX `fk_Boletim_bet1_idx` (`bet_id` ASC) VISIBLE,
  CONSTRAINT `fk_Boletim_user1`
    FOREIGN KEY (`user_email`)
    REFERENCES `rasdb`.`user` (`email`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Boletim_bet1`
    FOREIGN KEY (`bet_id`)
    REFERENCES `rasdb`.`bet` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `rasdb`.`moeda`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `rasdb`.`moeda` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `tipo` VARCHAR(45) NOT NULL,
  `montante` FLOAT NOT NULL,
  `user_email` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_moeda_user1_idx` (`user_email` ASC) VISIBLE,
  CONSTRAINT `fk_moeda_user1`
    FOREIGN KEY (`user_email`)
    REFERENCES `rasdb`.`user` (`email`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
