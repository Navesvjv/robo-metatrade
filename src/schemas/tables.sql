CREATE TABLE `ticks_win_1min` (
  `id` int NOT NULL AUTO_INCREMENT,
  `symbol` varchar(10) NOT NULL,
  `time` datetime NOT NULL,
  `volume` int NOT NULL,
  `bid` decimal(10,5) NOT NULL,
  `ask` decimal(10,5) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `ticks_win_1min` (
  `id` int NOT NULL AUTO_INCREMENT,
  `symbol` varchar(10) NOT NULL,
  `time` varchar(30) NOT NULL,
  `volume` int NOT NULL,
  `bid` decimal(15,5) NOT NULL,
  `ask` decimal(15,5) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
