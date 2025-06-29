INSERT INTO Cities (city_name) VALUES
    ('Mumbai'),
    ('Delhi'),
    ('Bengaluru'),
    ('Hyderabad'),
    ('Ahmedabad'),
    ('Chennai'),
    ('Kolkata'),
    ('Surat'),
    ('Pune'),
    ('Jaipur');

INSERT INTO Users (name, email, phone_no, role, password) VALUES
('Danish', 'dinesh@example.com', '9876543210', 'admin', 'A123'),
('Priya Patel', 'priya.patel@example.com', '9876543211', 'user', 'securePass1'),
('Rahul Verma', 'rahul.verma@example.com', '9876543212', 'user', 'myPass@456'),
('Sonia Mehta', 'sonia.mehta@example.com', '9876543213', 'user', 'passWord789'),
('Vikram Singh', 'vikram.singh@example.com', '9876543214', 'user', 'Vikram@123'),
('Neha Kapoor', 'neha.kapoor@example.com', '9876543215', 'user', 'NehaKapoor!1'),
('Arjun Das', 'arjun.das@example.com', '9876543216', 'user', 'ArjunDas@789'),
('Simran Kaur', 'simran.kaur@example.com', '9876543217', 'user', 'SimranKaur#55'),
('Ravi Iyer', 'ravi.iyer@example.com', '9876543218', 'user', 'ravi_iyer@321'),
('Deepak Malhotra', 'deepak.malhotra@example.com', '9876543219', 'user', 'Deepak@Secure');

ALTER TABLE grounds modify column status varchar(50);

INSERT INTO Grounds (ground_name, city_id, capacity, price, status) VALUES
-- Grounds for City 1
('Green Field Stadium', 1, 5000, 2000.00, 'available'),
('Sunrise Sports Arena', 1, 3000, 1500.00, 'available'),
('Metro Cricket Ground', 1, 7000, 2500.00, 'available'),
('National Football Turf', 1, 10000, 3500.00, 'maintenance'),
('Olympic Training Center', 1, 5000, 1800.00, 'available'),

-- Grounds for City 2
('Skyline Sports Complex', 2, 6000, 2200.00, 'available'),
('Riverside Football Ground', 2, 8000, 2800.00, 'booked'),
('Sunset Cricket Stadium', 2, 4500, 1700.00, 'available'),
('Elite Sports Arena', 2, 5500, 2100.00, 'available'),
('Victory Tennis Court', 2, 2000, 1200.00, 'available'),

-- Grounds for City 3
('Evergreen Turf', 3, 7500, 2600.00, 'available'),
('City Football Stadium', 3, 9000, 3100.00, 'available'),
('Grand Sports Hub', 3, 4000, 1900.00, 'maintenance'),
('Rapid Fire Cricket Ground', 3, 6800, 2300.00, 'available'),
('Champion Arena', 3, 5000, 2100.00, 'available'),

-- Grounds for City 4
('Mega Soccer Complex', 4, 9500, 3200.00, 'available'),
('Speedway Sports Park', 4, 3500, 1600.00, 'booked'),
('Metro Arena', 4, 7200, 2700.00, 'available'),
('Sunlit Stadium', 4, 8100, 2900.00, 'available'),
('Thunder Cricket Club', 4, 5300, 2000.00, 'available'),

-- Grounds for City 5
('Royal Turf', 5, 8200, 2800.00, 'available'),
('Highland Sports Complex', 5, 4100, 1750.00, 'available'),
('Golden Era Football Field', 5, 9300, 3300.00, 'booked'),
('Speed Masters Track', 5, 5700, 2250.00, 'available'),
('Dreamland Cricket Ground', 5, 6000, 2500.00, 'available'),

-- Grounds for City 6
('Summit Soccer Arena', 6, 9700, 3400.00, 'available'),
('Valley View Stadium', 6, 4400, 1800.00, 'available'),
('Peak Sports Hub', 6, 6600, 2400.00, 'available'),
('Heritage Cricket Ground', 6, 7700, 2900.00, 'maintenance'),
('Rapid Football Arena', 6, 8800, 3100.00, 'available'),

-- Grounds for City 7
('Ocean Breeze Sports Park', 7, 7200, 2700.00, 'available'),
('Lightning Cricket Field', 7, 5000, 2000.00, 'available'),
('Gladiator Sports Club', 7, 6800, 2300.00, 'available'),
('Sky High Football Ground', 7, 7500, 2600.00, 'available'),
('Ironman Training Center', 7, 4000, 1900.00, 'maintenance'),

-- Grounds for City 8
('Dream Arena', 8, 9000, 3200.00, 'available'),
('Champion Cricket Ground', 8, 6700, 2500.00, 'available'),
('Super Sports Stadium', 8, 7300, 2700.00, 'available'),
('Tiger Turf', 8, 8300, 2900.00, 'booked'),
('Horizon Football Complex', 8, 5100, 2000.00, 'available'),

-- Grounds for City 9
('Knight Sports Arena', 9, 9800, 3500.00, 'available'),
('Rapid Play Soccer Ground', 9, 4900, 1800.00, 'available'),
('Fortress Cricket Stadium', 9, 8700, 3200.00, 'maintenance'),
('Royal Soccer Field', 9, 6600, 2400.00, 'available'),
('Empire Turf', 9, 7000, 2500.00, 'available'),

-- Grounds for City 10
('Storm Stadium', 10, 7200, 2700.00, 'available'),
('Hurricane Football Arena', 10, 8500, 3100.00, 'available'),
('Supernova Sports Club', 10, 6400, 2300.00, 'available'),
('Victory Cricket Ground', 10, 7500, 2600.00, 'available'),
('Mountain Peak Stadium', 10, 5700, 2200.00, 'available');

INSERT INTO Slot_Available (ground_id, slot_date, start_time, end_time, availability) VALUES

(1, '2025-04-05', '08:00:00', '10:00:00', 'available'),
(2, '2025-04-05', '10:00:00', '12:00:00', 'available'),
(3, '2025-04-05', '12:00:00', '14:00:00', 'available'),
(4, '2025-04-05', '14:00:00', '16:00:00', 'booked'),
(5, '2025-04-05', '16:00:00', '18:00:00', 'available'),

(6, '2025-04-06', '08:00:00', '10:00:00', 'available'),
(7, '2025-04-06', '10:00:00', '12:00:00', 'available'),
(8, '2025-04-06', '12:00:00', '14:00:00', 'available'),
(9, '2025-04-06', '14:00:00', '16:00:00', 'booked'),
(10, '2025-04-06', '16:00:00', '18:00:00', 'available'),

(11, '2025-04-07', '08:00:00', '10:00:00', 'available'),
(12, '2025-04-07', '10:00:00', '12:00:00', 'available'),
(13, '2025-04-07', '12:00:00', '14:00:00', 'available'),
(14, '2025-04-07', '14:00:00', '16:00:00', 'booked'),
(15, '2025-04-07', '16:00:00', '18:00:00', 'available'),

(16, '2025-04-08', '08:00:00', '10:00:00', 'available'),
(17, '2025-04-08', '10:00:00', '12:00:00', 'available'),
(18, '2025-04-08', '12:00:00', '14:00:00', 'available'),
(19, '2025-04-08', '14:00:00', '16:00:00', 'booked'),
(20, '2025-04-08', '16:00:00', '18:00:00', 'available'),

(21, '2025-04-09', '08:00:00', '10:00:00', 'available'),
(22, '2025-04-09', '10:00:00', '12:00:00', 'available'),
(23, '2025-04-09', '12:00:00', '14:00:00', 'available'),
(24, '2025-04-09', '14:00:00', '16:00:00', 'booked'),
(25, '2025-04-09', '16:00:00', '18:00:00', 'available'),

(26, '2025-04-10', '08:00:00', '10:00:00', 'available'),
(27, '2025-04-10', '10:00:00', '12:00:00', 'available'),
(28, '2025-04-10', '12:00:00', '14:00:00', 'available'),
(29, '2025-04-10', '14:00:00', '16:00:00', 'booked'),
(30, '2025-04-10', '16:00:00', '18:00:00', 'available'),

(31, '2025-04-11', '08:00:00', '10:00:00', 'available'),
(32, '2025-04-11', '10:00:00', '12:00:00', 'available'),
(33, '2025-04-11', '12:00:00', '14:00:00', 'available'),
(34, '2025-04-11', '14:00:00', '16:00:00', 'booked'),
(35, '2025-04-11', '16:00:00', '18:00:00', 'available'),

(36, '2025-04-12', '08:00:00', '10:00:00', 'available'),
(37, '2025-04-12', '10:00:00', '12:00:00', 'available'),
(38, '2025-04-12', '12:00:00', '14:00:00', 'available'),
(39, '2025-04-12', '14:00:00', '16:00:00', 'booked'),
(40, '2025-04-12', '16:00:00', '18:00:00', 'available'),

(41, '2025-04-13', '08:00:00', '10:00:00', 'available'),
(42, '2025-04-13', '10:00:00', '12:00:00', 'available'),
(43, '2025-04-13', '12:00:00', '14:00:00', 'available'),
(44, '2025-04-13', '14:00:00', '16:00:00', 'booked'),
(45, '2025-04-13', '16:00:00', '18:00:00', 'available'),

(46, '2025-04-14', '08:00:00', '10:00:00', 'available'),
(47, '2025-04-14', '10:00:00', '12:00:00', 'available'),
(48, '2025-04-14', '12:00:00', '14:00:00', 'available'),
(49, '2025-04-14', '14:00:00', '16:00:00', 'booked'),
(50, '2025-04-14', '16:00:00', '18:00:00', 'available');

INSERT INTO Feedback (user_id, ground_id, rating, comment, feedback_date) VALUES
(1, 1, 5, 'Great ground with excellent facilities!', NOW()),
(2, 2, 4, 'Nice experience, but could use some improvements.', NOW()),
(3, 3, 3, 'Decent ground, but needs better maintenance.', NOW()),
(4, 4, 5, 'Loved the ground! Very well-maintained and clean.', NOW()),
(5, 5, 4, 'Good experience overall, but a bit crowded at times.', NOW()),

(6, 6, 5, 'Fantastic ground! Highly recommended.', NOW()),
(7, 7, 4, 'Good ground, but a little expensive for the facilities provided.', NOW()),
(8, 8, 3, 'The ground was okay, but the surface could be improved.', NOW()),
(9, 9, 5, 'Superb! Best ground in the city with great ambiance.', NOW()),
(10, 10, 4, 'Great place to play, but needs better lighting.', NOW()),

(1, 11, 5, 'Excellent facility with good seating arrangements.', NOW()),
(2, 12, 4, 'Nice ground but the management should improve cleanliness.', NOW()),
(3, 13, 3, 'Ground was fine, but it was a bit dirty.', NOW()),
(4, 14, 5, 'Wonderful place for a match! Loved every moment.', NOW()),
(5, 15, 4, 'Good ground, but the turf was a bit too hard.', NOW()),

(6, 16, 5, 'A fantastic experience. Would love to play again!', NOW()),
(7, 17, 4, 'Good ground overall, but some areas could be improved.', NOW()),
(8, 18, 3, 'The ground was fine, but the overall atmosphere was lacking.', NOW()),
(9, 19, 5, 'Amazing place! Great turf and well-maintained.', NOW()),
(10, 20, 4, 'Good experience, but the grass was a little uneven.', NOW()),

(1, 21, 5, 'Top-notch facilities and great ambiance!', NOW()),
(2, 22, 4, 'Nice ground but needs some improvements in seating.', NOW()),
(3, 23, 3, 'The ground was okay, but the maintenance could be better.', NOW()),
(4, 24, 5, 'Loved it! One of the best grounds I have played on.', NOW()),
(5, 25, 4, 'Good ground, but it was a bit hot in the afternoon.', NOW()),

(6, 26, 5, 'Perfect ground for a match! Would definitely recommend.', NOW()),
(7, 27, 4, 'Nice place, but could be a little less crowded.', NOW()),
(8, 28, 3, 'Decent ground, but needs more seating for spectators.', NOW()),
(9, 29, 5, 'Fantastic! Everything was perfect, from the turf to the seating.', NOW()),
(10, 30, 4, 'Good place to play, but the management could be more responsive.', NOW()),

(1, 31, 5, 'Loved playing here. Clean, well-maintained, and spacious.', NOW()),
(2, 32, 4, 'Good experience, but the ground could be softer.', NOW()),
(3, 33, 3, 'It was okay, but the facilities could be upgraded.', NOW()),
(4, 34, 5, 'Amazing! Best experience I’ve had in a long time.', NOW()),
(5, 35, 4, 'Nice ground, but it was a bit too expensive for the quality.', NOW()),

(6, 36, 5, 'Wonderful ground with top-class facilities.', NOW()),
(7, 37, 4, 'Good, but needs better management.', NOW()),
(8, 38, 3, 'Ground was fine, but not very clean.', NOW()),
(9, 39, 5, 'Best ground I’ve played at! Highly recommended.', NOW()),
(10, 40, 4, 'Nice ground, but could use more seating for spectators.', NOW()),

(1, 41, 5, 'Great experience! Would love to play here again.', NOW()),
(2, 42, 4, 'Good overall, but the ground could be a bit softer.', NOW()),
(3, 43, 3, 'Decent, but there were too many people around.', NOW()),
(4, 44, 5, 'Excellent turf, great atmosphere, and fantastic facilities.', NOW()),
(5, 45, 4, 'Good ground, but a bit crowded during peak hours.', NOW()),

(6, 46, 5, 'Wonderful ground with amazing facilities.', NOW()),
(7, 47, 4, 'Nice ground, but management could improve in some areas.', NOW()),
(8, 48, 3, 'The ground was good, but some maintenance issues.', NOW()),
(9, 49, 5, 'Fantastic experience, loved the ground!', NOW()),
(10, 50, 4, 'Nice place to play, but the ground could use some repairs.', NOW());