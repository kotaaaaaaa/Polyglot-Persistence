create table Customers ( 

customerid INT NOT NULL PRIMARY KEY, 

first_name VARCHAR(25), 

last_name VARCHAR(25), 

dob DATE, 

mobile VARCHAR(15), 

email VARCHAR(50), 

profession VARCHAR(50), 

status BIT 

); 

 

 

create table Owners ( 

ownerid INT not null PRIMARY KEY, 

first_name VARCHAR(25), 

last_name VARCHAR(25), 

mobile VARCHAR(15), 

email VARCHAR(50) 

); 

 

create table PostcodeMaster ( 

postcode varchar(10) NOT NULL PRIMARY KEY, 

city VARCHAR(25), 

county VARCHAR(25), 

country VARCHAR(25) 

); 

 
 
 

create table Properties ( 

propertyid INT NOT NULL PRIMARY KEY, 

ownerid INT, 

postcode VARCHAR(10), 

property_type VARCHAR(25), 

status BIT 

); 

 
 
 

create table Appointments ( 

appointmentid INT NOT NULL PRIMARY KEY, 

propertyid INT, 

customerid INT, 

appointment_datetime DATETIME 

); 

 
 
 

create table PropertyFeedback ( 

feedbackid INT NOT NULL PRIMARY KEY, 

propertyid INT, 

customerid INT, 

rating_location INT, 

rating_amenities INT, 

rating_price INT, 

rating_overall INT, 

feedbackdate DATE 

); 

 
 
 

create table Applications ( 

applicationid INT NOT NULL PRIMARY KEY, 

propertyid INT, 

customerid INT, 

proposed_depostit INT, 

proposed_rent INT, 

proposed_movingdate DATE, 

stayduration INT, 

applicationdate DATE 

); 

 
 
 

create table DealsMaster ( 

dealsid INT NOT NULL PRIMARY KEY, 

propertyid INT, 

customerid INT, 

final_monthlyrent INT, 

final_deposit INT, 

dealdate DATE, 

contract_startdate DATE, 

contract_enddate DATE 

); 

CREATE TRIGGER UpdatePropertyStatus
ON DealsMaster
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE Properties SET status=0 from Properties 
	inner join inserted i on 
	i.propertyid=Properties.propertyid
END


CREATE VIEW [dbo].[ApplicationsDetails]
AS
SELECT        dbo.Applications.applicationid, dbo.Applications.propertyid, dbo.Applications.customerid, dbo.Customers.first_name, dbo.Customers.last_name, dbo.Customers.dob, dbo.Customers.profession, 
                         dbo.Applications.proposed_deposit, dbo.Applications.proposed_rent, dbo.Applications.proposed_movingdate, dbo.Applications.stayduration, dbo.PropertyFeedback.rating_location, dbo.PropertyFeedback.rating_amenities, 
                         dbo.PropertyFeedback.rating_price, dbo.PropertyFeedback.rating_overall, dbo.Applications.applicationdate, dbo.Customers.email, dbo.Customers.mobile
FROM            dbo.Applications INNER JOIN
                         dbo.Customers ON dbo.Applications.customerid = dbo.Customers.customerid INNER JOIN
                         dbo.PropertyFeedback ON dbo.Customers.customerid = dbo.PropertyFeedback.customerid AND dbo.Applications.propertyid = dbo.PropertyFeedback.propertyid

