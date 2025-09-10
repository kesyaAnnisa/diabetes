-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 10, 2025 at 05:09 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `diabetes_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `patients`
--

CREATE TABLE `patients` (
  `id` int(11) NOT NULL,
  `Pregnancies` int(11) NOT NULL,
  `Glucose` int(11) NOT NULL,
  `BloodPressure` int(11) NOT NULL,
  `SkinThickness` int(11) NOT NULL,
  `Insulin` int(11) NOT NULL,
  `BMI` float NOT NULL,
  `DiabetesPedigreeFunction` float NOT NULL,
  `Age` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `patients`
--

INSERT INTO `patients` (`id`, `Pregnancies`, `Glucose`, `BloodPressure`, `SkinThickness`, `Insulin`, `BMI`, `DiabetesPedigreeFunction`, `Age`) VALUES
(1, 2, 120, 70, 25, 100, 24.5, 0.672, 35),
(2, 1, 150, 80, 30, 150, 28.7, 1.233, 41),
(3, 4, 95, 65, 20, 85, 22.1, 0.451, 29),
(4, 0, 130, 75, 28, 120, 30.4, 0.987, 50),
(5, 3, 180, 90, 40, 200, 35.6, 2.012, 55),
(6, 5, 110, 60, 22, 95, 23.9, 0.341, 27),
(7, 6, 140, 85, 32, 180, 33.2, 1.753, 45),
(8, 1, 160, 78, 29, 130, 26.8, 0.912, 39),
(9, 2, 170, 88, 35, 250, 37.5, 1.456, 60),
(10, 0, 100, 55, 18, 70, 21.4, 0.215, 22);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `patients`
--
ALTER TABLE `patients`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `patients`
--
ALTER TABLE `patients`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
