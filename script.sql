-- create RentalReports DB
drop schema if exists RentalReports;
create schema RentalReports;
use RentalReports;

-- create reports table
create table RentalReports.reports
(ReportID int not null auto_increment primary key,
DriverID int not null,
RentalID int not null,
PlateNo varchar(8) not null,
Outcome varchar(255) not null,
Content varchar(255) not null);

-- insert data into reports table
INSERT INTO RentalReports.reports VALUES
(1, 1, 1, 'SGA1234B', 'Replace', 'The interior was dirty'),
(2, 2, 2,'SGB2345C', 'Replace', 'The car was not clean');

-- create RentalVehicle DB
drop schema if exists RentalVehicle;
create schema RentalVehicle;
use RentalVehicle;

-- create vehicle table
create table RentalVehicle.vehicle
(PlateNo varchar(8) not null primary key,
Brand varchar(20) not null,
Model varchar(50) not null,
VehicleStatus varchar(50) not null,
ParkingSpotName varchar(255) not null,
Price float not null,
PriceID varchar(50) not null,
Latitude float not null,
Longitude float not null,
ParkingSpotID int not null);

-- insert values into vehicle table
INSERT INTO vehicle VALUES
('SGA2345C', 'Kia', 'Nitro Hybrid', 'Available', 'SCIS', 1000, 'price_1MsPOIFZwLHtEN8Wtw0f4SOT',  1.42681, 103.836,1),
('SGK4321D', 'Honda', 'Civic', 'Available', 'LKCSOB', 2000, 'price_1MsPToFZwLHtEN8WZIbuZs75', 1.40145, 103.818,2),
('SGL9987H', 'Mercedes-Benz', 'GLA-Class', 'Available', 'YPHSOL', 3000, 'price_1MsPeCFZwLHtEN8WtHaJkjbm', 1.37427, 103.846,3),
('SGX1234A', 'Hyundai', 'Avante', 'Available', 'SOA', 4000,'price_1MsPfoFZwLHtEN8WZXrbHjG9', 1.29924, 103.854,4),
('SGY9876B', 'Toyota', 'Wish', 'Available', 'SOSS', 5000,'price_1MsPiEFZwLHtEN8WN99SAd2O', 1.2968, 103.845,5);

-- create RentalTrip DB
drop schema if exists RentalTrip;
create schema RentalTrip;
use RentalTrip;

-- create rental table
create table RentalTrip.rental
(RentalID int not null auto_increment primary key,
DriverID int not null,
PlateNo varchar(8) not null,
StartTime datetime not null,
EndTime datetime,
StartLocation int not null,
EndLocation int,
BookingDuration float not null,
TotalFare float not null);

-- insert data into RentalTrip table
INSERT INTO RentalTrip.rental VALUES
(1, 1, 'SGA1234B', '2023-04-02 12:00:00', '2023-04-02 14:00:00', 1, 2, 2, 40),
(3, 3, 'SGX1234A', '2023-04-02 16:00:00', null, 1, null, 0, 0);

-- create DesignatedParkingSpot DB
drop schema if exists DesignatedParkingSpot;
create schema DesignatedParkingSpot;
use DesignatedParkingSpot;

-- create parkingspot table
create table DesignatedParkingSpot.parkingSpot
(Code int not null auto_increment primary key,
Name varchar(255) not null,
Latitude float not null,
Longitude float not null);

-- insert values into parkingspot table
INSERT INTO DesignatedParkingSpot.parkingspot(name, latitude, longitude) VALUES
('SCIS', 1.42681, 103.836),
('LKCSOB', 1.40145, 103.818),
('YPHSOL', 1.37427, 103.846),
('SOA', 1.29924, 103.854),
('SOSS', 1.2968, 103.845);

-- create Report DB
-- drop schema if exists Report;
-- create schema Report;
-- use Report;

-- create rentalreport table
-- CREATE TABLE IF NOT EXISTS `rentalreport` (
--   `ReportID` int NOT NULL AUTO_INCREMENT,
--   `DriverID` int NOT NULL,
--   `PlateNo` varchar(8) NOT NULL,
--   `Outcome` varchar(100) NOT NULL,
--   `Content` varchar(1000) NOT NULL,
--   PRIMARY KEY (`ReportID`)
-- ) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- insert data into rentalreport table
-- INSERT INTO `rentalreport` (`ReportID`, `DriverID`, `PlateNo`, `Outcome`, `Content`) VALUES
-- (1, 1, 'SGA1234B', 'Success', 'Successfully created the report'),
-- (2, 1, 'SGB2345C', 'Failure', 'Fail to create the report'),
-- (3, 1, 'SGC3456J', 'Success', 'Create the report successfully'),
-- (4, 1, 'SGX4567E', 'Failure', 'Fail to create the report'),
-- (5, 1, 'SGH5678G', 'Success', 'Create the report successfully');
-- COMMIT;
