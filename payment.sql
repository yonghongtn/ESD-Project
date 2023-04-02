drop database if exists payment;

create database payment;
use payment;

create table payment
(
PaymentID varchar(50) not null primary key,
DriverID varchar(9) not null,
RentalID varchar(10) not null,
ReportID varchar(10),
PaymentAmount decimal(10, 2) not null
);

select * from payment;