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
('SGY9876B', 'Toyota', 'Wish', 'Available', 'SOSS', 5000, 1.2968, 103.845);

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