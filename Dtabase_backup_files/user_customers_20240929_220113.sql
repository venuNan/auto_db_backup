-- Table structure for `customers`
CREATE TABLE `customers` (
  `customer_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `address` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`customer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table `customers`
INSERT INTO `customers` (`customer_id`, `name`, `address`) VALUES
('2', 'Jane Smith', '456 Maple Avenue'),
('3', 'Alice Johnson', '789 Oak Drive'),
('4', 'Bob Williams', '101 Pine Road'),
('5', 'Charlie Brown', '202 Cedar Street'),
('6', 'David Jones', '303 Birch Lane'),
('7', 'Emily Davis', '404 Spruce Boulevard'),
('8', 'Frank Miller', '505 Redwood Court'),
('9', 'Grace Lee', '606 Chestnut Avenue'),
('10', 'Hannah White', '707 Aspen Way');
