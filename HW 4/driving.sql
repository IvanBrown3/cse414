CREATE TABLE InsuranceCo (
    name VARCHAR(30),
    phone INT,
    maxLiability FLOAT,
    PRIMARY KEY (name)
);

CREATE TABLE Person (
    ssn INT,
    name VARCHAR(30),
    PRIMARY KEY (ssn)
);

CREATE TABLE Vehicle (
    licensePlate VARCHAR(30),
    year INT,
    insuranceCoName VARCHAR(30),
    ssn INT,
    PRIMARY KEY (licensePlate),
    FOREIGN KEY (insuranceCoName) REFERENCES InsuranceCo(name),
    FOREIGN KEY (ssn) REFERENCES Person(ssn)
);

CREATE TABLE Car (
    make VARCHAR(30),
    licensePlate VARCHAR(30),
    FOREIGN KEY (licensePlate) REFERENCES Vehicle(licensePlate)
);

CREATE TABLE ProfessionalDriver (
    ssn INT,
    medicalHistory VARCHAR(30),
    FOREIGN KEY (ssn) REFERENCES Person(ssn)
);

CREATE TABLE Truck (
    capacity INT,
    licensePlate VARCHAR(30),
    truckDriver INT,
    FOREIGN KEY (licensePlate) REFERENCES Vehicle(licensePlate),
    FOREIGN KEY (truckDriver) REFERENCES ProfessionalDriver(ssn) 
);

CREATE TABLE Driver (
    driverID INT,
    ssn INT,
    FOREIGN KEY (ssn) REFERENCES Person(ssn)
);

CREATE TABLE NonProfessionalDriver (
    ssn INT,
    FOREIGN KEY (ssn) REFERENCES Person(ssn)
);

CREATE TABLE DRIVES (
  licensePlate VARCHAR(30),
  ssn INT,
  PRIMARY KEY (ssn, licensePlate),
  FOREIGN KEY (ssn) REFERENCES Person(ssn),
  FOREIGN KEY (licensePlate) REFERENCES Vehicle(licensePlate)
);


--b. The insures relationship is a many to one relationship. It is an attribute contained in the insurance company and is references here 
--FOREIGN KEY (insuranceCoName) REFERENCES InsuranceCo(name).
--I chose to represent it this way because it would be trivial to make a table called insures
--this is because vehicle is always able to reference the insurance company and the maxliability provided by the company.

--c. Drives is a many to many relationship that has foreign keys from person and vehicle's primary key. Due to there being two priamry keys for 
--vehicle, it makes sense to make it as its own table to reference both sides of the diagram. 
-- Operates table is unessecary since it creates a many to one relationship with truck and vehicles. From the ER diagram
--it is clear that one professional driver operates a truck, so the relationship was representated with the FOREIGN KEY (truckDriver) REFERENCES ProfessionalDriver(ssn) line.
