import pymongo
import pyodbc
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# SQL server information
server = 'tcp:mcruebs04.isad.isadroot.ex.ac.uk'
database = 'BEMM459_GroupL'
username = 'GroupL'
password = 'DjwN801+Bs'

# Driver for Mac machine.  Comment out when on windows machine.
cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password+';TrustServerCertificate=yes;Encrypt=no;')
cursor = cnxn.cursor()

# Mongo Connection
# Mongo server information
mongoClient = pymongo.MongoClient('mongodb://KKamran:DigF479%2BKh@mcruebs04.ex.ac.uk:27017/?authSource=BEMM459_KKamran&authMechanism=SCRAM-SHA-256&readPreference=primary&ssl=false&directConnection=true')
print('These are the database names that your connection can see')
print(mongoClient.list_database_names())

# Use your database name here
DB = mongoClient["BEMM459_KKamran"]
print(DB.list_collection_names())

#Demo Application Flow for SQL 

#Step 1 -Create Owner Account
cursor.execute("insert into Owners (ownerid, first_name, last_name, mobile, email) values (53, 'Carena', 'Dallaway', '43-248-2527', 'cdallawayt@usnews.com');")
cnxn.commit()
print ('Registration of Owner completed.')

#Step 2 - Owner List a Property 
cursor.execute("insert into Properties (propertyid, ownerid, postcode, property_type, status) values (102, 52, 'EX44SQ', 'Apartment', 1);")
cnxn.commit()

#Add entry to a collection called Properties

myprop = DB["Properties"]
prop = { 
      "propertyid": 102, 
      "property_desc": " Very Beautiful and spacious house in the countryside", 
      "address": "1234 Country Lane", 
      "postcode": "EX44SQ", 
      "property_type": "House", 
      "rooms": 5, 
      "bathrooms": 3, 
      "expected_monthlyrent": 2000, 
      "expected_deposit": 3000, 
      "Amenities": ["Park"] 
   }

x = myprop.insert_one(prop)
if x.inserted_id is not None:
    print("Property added Successfully.")
else:
    print("Error")

#Step 3 - Owner Updates Property 
myquery = { "address": "1234 Country Lane" }
newvalues = { "$set": { "address": "*** 4041 Oak St Changed to New Exeter***" } }
myprop.update_one(myquery, newvalues)
print ('Property data updated successfully.')

#print documents in the collection after the update:
for x in myprop.find(myquery):
    print(x)

#Step 4 - Customer Signup
cursor.execute("insert into Customers (customerid, first_name, last_name, dob, mobile, email, profession, status) values (201, 'Vishal', 'Pansare', '1989-04-11','33-248-2527', 'vishal@usnews.com','Student',1);")
cnxn.commit()
print ('Customer signed up on the application.')

#Step 5 - Customer search for a property

print ('Showing List of Properties to Customer based on his requirement using Filtering method on Mongodb')
prop_data = myprop.find()

for x in prop_data:
    print(x)

# Advanced Filtering - Customer can look for specific property where resnt is higher than a certain value (this type of filtering is universal and applies to all bumeric values) 
query = { "expected_monthlyrent": { "$gt": 3000 } }
doc = myprop.find(query)

for z in doc:
    print(z)

# Filtering property with Parking
myquery = { "Parking" }
mydoc = myprop.find(myquery)

for x in mydoc:
    print(x)

#Step 6 - Customer books appointment to view property
cursor.execute("insert into Appointments (appointmentid, propertyid, customerid, appointment_datetime) values (63, 101, 201, '2023-04-11 13:00:00');")
cnxn.commit()
print ('Customer Property Viewing Appointment Booked.')

#Step 7 - Customer reschedule appointment 
cursor.execute("UPDATE Appointments SET appointment_datetime = '2023-04-13 13:00:00' WHERE appointmentid=63;")
cnxn.commit()
print ('Customer Property Viewing Appointment Time Updated.')

#Step 8 - Customer gives feedback after viewing property
cursor.execute("insert into PropertyFeedback (feedbackid, propertyid, customerid, rating_location, rating_amenities, rating_price, rating_overall, feedbackdate) values (401,101,201,9,7,8,8,'2023-04-15');")
cnxn.commit()
print ('Customer Submitted the Feedback.')

#Step 9 - Customer puts his application
cursor.execute("insert into Applications (applicationid, propertyid, customerid, proposed_deposit, proposed_rent, proposed_movingdate, stayduration, applicationdate) values (101,101,201,1000,500,'2023-05-01',12,'2023-04-17');")
cnxn.commit()
print ('Customer filed an application to rent the apartment.')

#Step 10 - Owners views all applications
print ('Owner views all applications filed for the property listed. Data retrieved from a view which has personal data of customers, their feedback and application details')        
cursor.execute("SELECT * FROM ApplicationsDetails where propertyid=1")
for row in cursor.fetchall():
    print (row)

#Step 11 - Deal Finalized between Customer and Owner
cursor.execute("insert into DealsMaster (dealsid, propertyid, customerid, final_monthlyrent, final_deposit, dealdate, contract_startdate, contract_enddate) values (51,101,201,500,1000,'2023-04-20','2023-05-01','2024-04-30');")
cnxn.commit()
print ('Owner finalized a deal with a customer and property status changed to rented.')


#Step 12 - Delete properties older than 5 years
cursor.execute("Delete from DealsMaster where contract_enddate < '2018-04-22'")
cnxn.commit()
print ('All properties whose contract dates ended 5 years ago are deleted from database to improve efficiency of the application.')

## Analysis

# Get Average Ratings of Properties for Heatmap
print ('Getting average ratings for all the properties for which feedback is submitted.')
avg_sql = "SELECT propertyid, AVG(rating_location) as avg_rating_location, AVG(rating_amenities) as avg_rating_amenities, AVG(rating_price) as avg_rating_price, AVG(rating_overall) as avg_rating_overall from PropertyFeedback GROUP BY propertyid"
data = pd.read_sql(avg_sql,cnxn)
data

# Creating the dataframe from Mongodb 
results = myprop.find()
df = pd.DataFrame(results, columns = ['propertyid','postcode','property_type', 'rooms', 'bathrooms', 'expected_monthlyrent', 'expected_deposit'])
df

# Checking and exportingdescriptive statistics of the extracted data 
d1 = df.describe()
d1.to_csv('data.csv')

# Room-Rent relation
s1 = sns.lmplot(x='rooms', y='expected_monthlyrent', data=df)
plt.savefig('Relation.png')

# Rent distribution
s2 = sns.histplot(df, x="expected_monthlyrent")
s2.set(xlabel='Monthly Rent')
plt.savefig('Rent.png')

# Merged Data from SQL and NoSQL for further Anlaysis
fin = pd.merge(df, data, left_index=True, right_index=True)

fin1 = fin[["rooms","bathrooms", "expected_monthlyrent", "expected_deposit", "avg_rating_location","avg_rating_amenities", "avg_rating_price", "avg_rating_overall" ]] 

# Descriptive tatistics for merged data
d2 = fin1.describe()
d2.to_csv('data2.csv')

# Plotting heatmap for the correlated values
cor = fin1.corr()

f = sns.heatmap(cor, annot=True)
plt.figure(figsize=(15,8))
fig = f.get_figure()
fig.savefig('sat.png')
