DROP TABLE IF EXISTS Feedback;
DROP TABLE IF EXISTS Invoice;
DROP TABLE IF EXISTS Payments;
DROP TABLE IF EXISTS Slot_Available;
DROP TABLE IF EXISTS Grounds;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Cities;
DROP TABLE IF EXISTS Edited_Users;

CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone_no VARCHAR(15) NOT NULL,
    role ENUM('user', 'admin') DEFAULT 'user',
    password VARCHAR(255) NOT NULL
);

CREATE TABLE Edited_Users (
    user_id INT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone_no VARCHAR(15) NOT NULL,
    role ENUM('user', 'admin') DEFAULT 'user',
    password VARCHAR(255) NOT NULL,
    action varchar(25)
); 

CREATE TABLE Cities (
    city_id INT AUTO_INCREMENT PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL
);

CREATE TABLE Grounds (
    ground_id INT AUTO_INCREMENT PRIMARY KEY,
    ground_name VARCHAR(100) NOT NULL,
    city_id INT NOT NULL,
    capacity INT,
    price DECIMAL(10, 2),
    status ENUM('available', 'unavailable', 'maintenance') DEFAULT 'available',
    FOREIGN KEY (city_id) REFERENCES Cities(city_id) ON DELETE CASCADE
);

CREATE TABLE Slot_Available (
    slot_id INT AUTO_INCREMENT PRIMARY KEY,
    ground_id INT NOT NULL,
    slot_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    availability ENUM('available', 'booked') DEFAULT 'available',
    FOREIGN KEY (ground_id) REFERENCES Grounds(ground_id) ON DELETE CASCADE,
    UNIQUE (ground_id, slot_date, start_time)
);

CREATE TABLE Payments (
    P_id INT AUTO_INCREMENT PRIMARY KEY,
    slot_id INT NOT NULL,
    P_mode ENUM('Credit Card', 'UPI', 'Net Banking', 'Cash') NOT NULL,
    amount_paid DECIMAL(10, 2) NOT NULL,
    payment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (slot_id) REFERENCES Slot_Available(slot_id) ON DELETE CASCADE
);

CREATE TABLE Invoice (
    invoice_id INT AUTO_INCREMENT PRIMARY KEY,
    P_id INT NOT NULL UNIQUE,
    invoice_date DATE DEFAULT (CURRENT_DATE()),
    FOREIGN KEY (P_id) REFERENCES Payments(P_id)
);

CREATE TABLE Feedback (
    feedback_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    ground_id INT NOT NULL,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    feedback_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (ground_id) REFERENCES Grounds(ground_id) ON DELETE CASCADE
);

DELIMITER //

CREATE TRIGGER after_user_update
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
  INSERT INTO Edited_Users (user_id, name, email, phone_no, role, password, action)
  VALUES (OLD.user_id, OLD.name, OLD.email, OLD.phone_no, OLD.role, OLD.password, 'UPDATE');
END //

DELIMITER ;

DELIMITER //

CREATE TRIGGER after_user_delete
AFTER DELETE ON users
FOR EACH ROW
BEGIN
  INSERT INTO Edited_Users (user_id, name, email, phone_no, role, password, action)
  VALUES (OLD.user_id, OLD.name, OLD.email, OLD.phone_no, OLD.role, OLD.password, 'DELETE');
END //

DELIMITER ;

CREATE OR REPLACE VIEW BookedGroundsDetails AS
SELECT 
    i.invoice_id,
    i.invoice_date,
    p.amount_paid,
    s.slot_id,
    g.ground_name AS ground_name,
    c.city_name AS city_name
FROM Invoice i
JOIN Payments p ON i.P_id = p.P_id
JOIN Slot_Available s ON p.slot_id = s.slot_id
JOIN Grounds g ON s.ground_id = g.ground_id
JOIN Cities c ON g.city_id = c.city_id;