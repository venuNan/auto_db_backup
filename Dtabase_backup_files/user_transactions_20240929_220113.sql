-- Table structure for `transactions`
CREATE TABLE `transactions` (
  `transaction_id` int NOT NULL AUTO_INCREMENT,
  `amount` decimal(10,2) DEFAULT NULL,
  `customer_id` int DEFAULT NULL,
  PRIMARY KEY (`transaction_id`),
  KEY `customer_id` (`customer_id`),
  CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `transactions`
INSERT INTO `transactions` (`transaction_id`, `amount`, `customer_id`) VALUES
('2', '250.75', '2'),
('3', '300.00', '3'),
('4', '150.20', '4'),
('5', '450.65', '5'),
('7', '200.80', '2'),
('8', '750.00', '6'),
('9', '320.10', '7'),
('10', '1000.00', '3');
