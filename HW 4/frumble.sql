
CREATE TABLE Sales 
        (name varchar(15), 
        discount FLOAT,
        month varchar(15),
        price INT);


--b
--non trivial functional dependancies are 
--1) name -> price
--the name of the product being sold solely determines the price of the item
--2) month -> discount
--the month that the item is sold in determines the discount

--functional dependancy that does not exist is 
--3) price -> month

--c
--BCNF
--R1(name, price)
--R3(month, discount)
--R4(month, name)

CREATE TABLE Items (
name VARCHAR(15),
price INT,
PRIMARY KEY (name)
);
--37 rows

CREATE TABLE Months (
month VARCHAR(15),
discount FLOAT,
PRIMARY KEY (month)
);
--13 rows

CREATE TABLE Relation(
month VARCHAR(15),
name VARCHAR(15),
PRIMARY KEY (month, name),
FOREIGN KEY (month) REFERENCES Months(month),
FOREIGN KEY (name) REFERENCES Items(name)
);
--427 rows

INSERT INTO Items 
SELECT DISTINCT name, price 
FROM Sales;

INSERT INTO Months 
SELECT DISTINCT month, discount 
FROM Sales;

INSERT INTO Relation
SELECT DISTINCT month, name
FROM Sales;
