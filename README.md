# Rental Property Management System

This project is a rental property management system that uses both SQL Server and MongoDB databases to manage various operations related to rental properties. The application allows property owners to register, list, and update their properties, while customers can search for properties, book appointments to view them, and submit rental applications.

## Setup

### Prerequisites

1. Python 3.x installed
2. SQL Server
3. MongoDB
4. Required Python packages: `pymongo`, `pyodbc`, `pandas`, `seaborn`, `matplotlib`

### Database Configuration

1. Run the SQL script `QueryToGenerateTables.sql` on SQL Server to create the necessary tables, triggers, and views.
2. Set up your MongoDB database with the required collections.

### Configuration

Update the `main.py` script with the appropriate SQL server and MongoDB database connection details.

## Running the Application

Execute the `main.py` script to run the application. The script will perform the following operations:

1. Register a new owner.
2. Add a property to the system.
3. Update property information.
4. Register a new customer.
5. Search for properties based on specific requirements.
6. Book an appointment to view a property.
7. Reschedule an appointment.
8. Submit feedback after viewing a property.
9. File an application to rent a property.
10. View all applications submitted for a property.
11. Finalize a deal between a customer and owner.
12. Delete old properties from the database.

Additionally, the script demonstrates how to perform some data analysis, such as generating average ratings for properties and visualizing the relationship between the number of rooms and expected monthly rent.

## Output

The script will generate output in the form of printed messages and visualizations saved as image files. These include:

1. `Relation.png` - A scatter plot of the relationship between the number of rooms and expected monthly rent.
2. `Rent.png` - A histogram of the distribution of expected monthly rents.
3. `sat.png` - A heatmap of the correlation between various features of rental properties.

You can also export data to CSV files during the analysis process, such as the descriptive statistics of extracted data:

1. `data.csv` - Descriptive statistics for the data extracted from MongoDB.
2. `data2.csv` - Descriptive statistics for the merged data from SQL and NoSQL databases.
