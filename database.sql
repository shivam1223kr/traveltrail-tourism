CREATE DATABASE IF NOT EXISTS tourist_manager;
USE tourist_manager;

CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(120) NOT NULL UNIQUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE destinations (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  state VARCHAR(100) NOT NULL,
  category VARCHAR(100),
  budget_level ENUM('low','medium','high') NOT NULL,
  rating DECIMAL(2,1) DEFAULT 0
);

CREATE TABLE hotels (
  id INT AUTO_INCREMENT PRIMARY KEY,
  destination_id INT NOT NULL,
  name VARCHAR(120) NOT NULL,
  provider VARCHAR(80) NOT NULL,
  price_per_night DECIMAL(10,2) NOT NULL,
  rating DECIMAL(2,1),
  amenities TEXT,
  FOREIGN KEY (destination_id) REFERENCES destinations(id)
);

CREATE TABLE bookings (
  id INT AUTO_INCREMENT PRIMARY KEY,
  booking_code VARCHAR(30) NOT NULL UNIQUE,
  user_id INT NULL,
  destination_id INT NOT NULL,
  checkin DATE NOT NULL,
  guests INT NOT NULL,
  status ENUM('pending','confirmed','cancelled') DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (destination_id) REFERENCES destinations(id)
);
