-- Aurum Hotel Management System Database Schema
-- Database: hotel_management

CREATE DATABASE IF NOT EXISTS hotel_management;
USE hotel_management;

-- 1. Admins Table
CREATE TABLE IF NOT EXISTS `admins` (
  `admin_id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(100) NOT NULL UNIQUE,
  `password` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`admin_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 2. Rooms Table
CREATE TABLE IF NOT EXISTS `rooms` (
  `room_id` INT NOT NULL AUTO_INCREMENT,
  `room_number` VARCHAR(20) NOT NULL UNIQUE,
  `room_type` VARCHAR(50) DEFAULT 'Single',
  `room_price` DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  `room_status` VARCHAR(30) DEFAULT 'Available',
  `floor_number` INT DEFAULT 1,
  `room_description` VARCHAR(255) DEFAULT '',
  PRIMARY KEY (`room_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 3. Customers Table
CREATE TABLE IF NOT EXISTS `customers` (
  `customer_id` INT NOT NULL AUTO_INCREMENT,
  `customer_name` VARCHAR(100) NOT NULL,
  `gender` VARCHAR(20) DEFAULT 'Male',
  `mobile` VARCHAR(20) DEFAULT '',
  `email` VARCHAR(100) DEFAULT '',
  `address` VARCHAR(255) DEFAULT '',
  `city` VARCHAR(100) DEFAULT '',
  `check_in_date` DATE DEFAULT NULL,
  PRIMARY KEY (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 4. Bookings Table
CREATE TABLE IF NOT EXISTS `bookings` (
  `booking_id` INT NOT NULL AUTO_INCREMENT,
  `customer_id` INT NOT NULL,
  `room_id` INT NOT NULL,
  `check_in_date` DATE NOT NULL,
  `check_out_date` DATE NOT NULL,
  `total_days` INT DEFAULT 1,
  `total_amount` DECIMAL(10,2) DEFAULT 0.00,
  `booking_status` VARCHAR(30) DEFAULT 'Confirmed',
  PRIMARY KEY (`booking_id`),
  KEY `customer_id` (`customer_id`),
  KEY `room_id` (`room_id`),
  CONSTRAINT `bookings_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`) ON DELETE RESTRICT,
  CONSTRAINT `bookings_ibfk_2` FOREIGN KEY (`room_id`) REFERENCES `rooms` (`room_id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Seed Data: Default Administrator (Username: admin | Password: admin123)
INSERT INTO `admins` (`username`, `password`)
VALUES ('admin', 'scrypt:32768:8:1$W9iSPGh10fAVMn32$4831b6c3bf7bacf10dee6aad4895ed894f8a93f4cf704fe89c6bc00e1e16dc4b454de2f3ef0a69a82be4b820d3bafc95ebb602f7800d3c21a8185af87ea95389')
ON DUPLICATE KEY UPDATE `username`=`username`;

-- Seed Data: Sample Rooms
INSERT INTO `rooms` (`room_number`, `room_type`, `room_price`, `room_status`, `floor_number`, `room_description`)
VALUES 
  ('101', 'Single', 1500.00, 'Available', 1, 'Standard single bed room with AC and WiFi'),
  ('102', 'Double', 2500.00, 'Available', 1, 'Spacious double bed room with city view'),
  ('201', 'Deluxe', 4000.00, 'Available', 2, 'Deluxe room with balcony and king bed'),
  ('202', 'Suite', 6000.00, 'Available', 2, 'Luxury executive suite with living area and mini-bar')
ON DUPLICATE KEY UPDATE `room_number`=`room_number`;

