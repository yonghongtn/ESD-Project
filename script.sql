-- create RentalReports DB
drop schema if exists RentalReports;
create schema RentalReports;
use RentalReports;

-- create reports table
create table reports
(ReportID int not null auto_increment primary key,
DriverID int not null,
PlateNo varchar(8) not null,
Outcome varchar(255) not null,
Content varchar(255) not null);

-- create RentalVehicle DB
drop schema if exists RentalVehicle;
create schema RentalVehicle;
use RentalVehicle;

-- create vehicle table
create table vehicle
(PlateNo varchar(8) not null primary key,
Brand varchar(20) not null,
Model varchar(50) not null,
VehicleStatus varchar(50) not null,
ParkingSpotName varchar(255) not null,
Price float not null,
Latitude float not null,
Longitude float not null);

-- insert values into vehicle table
INSERT INTO vehicle VALUES
('SGA2345C', 'Kia', 'Nitro Hybrid', 'Available', 'SCIS', 1000, 1.42681, 103.836),
('SGK4321D', 'Honda', 'Civic', 'Available', 'LKCSOB', 2000, 1.40145, 103.818),
('SGL9987H', 'Mercedes-Benz', 'GLA-Class', 'Available', 'YPHSOL', 3000, 1.37427, 103.846),
('SGX1234A', 'Hyundai', 'Avante', 'Available', 'SOA', 4000, 1.29924, 103.854),
('SGY9876B', 'Toyota', 'Wish', 'Available', 'SOSS', 5000, 1.2968, 103.845),
('SGA2346C', 'Nissan', 'X-Trail', 'Unavailable', 'SCIS', 2000, 1.42681, 103.836),
('SGK4322D', 'BMW', '3 Series', 'Available', 'LKCSOB', 3000, 1.40145, 103.818),
('SGL9988H', 'Volkswagen', 'Jetta', 'Unavailable', 'YPHSOL', 4000, 1.37427, 103.846),
('SGX1235A', 'Audi', 'A4', 'Available', 'Available', 'SOA', 5000, 1.29924, 103.854),
('SGY9877B', 'Toyota', 'Corolla', 'Unavailable', 'SOSS', 6000, 1.2968, 103.845),
('SGA2347C', 'Nissan', 'X-Trail', 'Available', 'SCIS', 7000, 1.42681, 103.836),
('SGK4323D', 'Volkswagen', 'Jetta', 'Unavailable', 'LKCSOB', 8000, 1.40145, 103.818),
('SGL9989H', 'Mercedes-Benz', 'CLA-Class', 'Available', 'YPHSOL', 9000, 1.37427, 103.846),
('SGX1236A', 'Hyundai', 'Ioniq Hybrid', 'Unavailable', 'SOA', 10000, 1.29924, 103.854),
('SGY9878B', 'Toyota', 'Camry', 'Available', 'SOSS', 11000, 1.2968, 103.845),
('SGA2348C', 'Kia', 'Sorento', 'Unavailable', 'SCIS', 12000, 1.42681, 103.836),
('SGK4324D', 'Honda', 'City', 'Available', 'LKCSOB', 13000, 1.40145, 103.818),
('SGL9990H', 'Mercedes-Benz', 'E-Class', 'Unavailable', 'YPHSOL', 14000, 1.37427, 103.846),
('SGX1237A', 'BMW', '3 Series', 'Available', 'SOA', 15000, 1.29924, 103.854),
('SGY9879B', 'Toyota', 'Vios', 'Unavailable', 'SOSS', 16000, 1.2968, 103.845);

-- create RentalTrip DB
drop schema if exists RentalTrip;
create schema RentalTrip;
use RentalTrip;

-- create rental table
create table rental
(RentalID int not null auto_increment primary key,
DriverID int not null,
PlateNo varchar(8) not null,
StartTime datetime not null,
EndTime datetime,
StartLocation int not null,
EndLocation int,
BookingDuration float not null,
TotalFare float not null);

-- create DesignatedParkingSpot DB
drop schema if exists DesignatedParkingSpot;
create schema DesignatedParkingSpot;
use DesignatedParkingSpot;

-- create parkingspot table
create table parkingSpot
(Code int not null auto_increment primary key,
Name varchar(255) not null,
Latitude float not null,
Longitude float not null);

-- insert values into parkingspot table
INSERT INTO parkingspot(name, latitude, longitude) VALUES
('SCIS', 1.42681, 103.836),
('LKCSOB', 1.40145, 103.818),
('YPHSOL', 1.37427, 103.846),
('SOA', 1.29924, 103.854),
('SOSS', 1.2968, 103.845);