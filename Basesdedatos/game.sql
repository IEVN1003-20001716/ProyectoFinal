-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost:3306
-- Tiempo de generación: 07-12-2024 a las 19:47:23
-- Versión del servidor: 8.0.30
-- Versión de PHP: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `game`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuariosr`
--

CREATE TABLE `usuariosr` (
  `userName` varchar(50) COLLATE utf8mb3_spanish_ci NOT NULL,
  `email` varchar(50) COLLATE utf8mb3_spanish_ci NOT NULL,
  `password` varchar(50) COLLATE utf8mb3_spanish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

--
-- Volcado de datos para la tabla `usuariosr`
--

INSERT INTO `usuariosr` (`userName`, `email`, `password`) VALUES
('Luis', 'luis@gmail.com', '123345'),
('Lalo', 'lalo@gmail.com', 'lalo123'),
('jugador3', 'usuario3@example.com', 'password3'),
('jugador2', 'jugador2@gmail.com', 'jugador123');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
