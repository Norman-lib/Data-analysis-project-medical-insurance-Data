from preprocessing.binaryChange import changeValuesToBinary
from file_managment.writeData import writeData
from file_managment.readData import readData
from plotData import plotData 
import mysql.connector as mysql
from mysql.connector import errorcode
from dataBaseManagment import DataBase
import csv

df = readData("Train_Data.csv")
ROOT = ""
PASSWORD = ""
HOST = ""
DATABASE = ""
DB_NAME = "InsurranceData"
# Preprocessing functions
processed = changeValuesToBinary(df)
print(processed.head())
print(processed.describe())
plotData(processed,"age", "charges",  "scatter")
plotData(processed, "age",  "bmi",  "scatter")
plotData(processed, "charges",  "children",  "scatter")

writeData("Train_Data_Processed.csv", processed)

# Database functions
# Creating new database class
db = DataBase(ROOT, PASSWORD, HOST, DATABASE)
# Checking connection status and reconnecting if not connected
if (db.getConnectionStatus() == False ):
    db.connectToDB()

# Creating new database
db.createDatabase(DB_NAME)
# Checking database creation status
db.getDatabaseCreationStatus()

# Using the database
db.useDB(DB_NAME)

# Creating new table
db.createTable("insured", "id INT AUTO_INCREMENT PRIMARY KEY, age INT NOT NULL, bmi FLOAT NOT NULL, children INT NOT NULL, smoker VARCHAR(20), region VARCHAR(20), charges FLOAT NOT NULL" )

# Clearing the table
db.clearTable("insurred")

# Inserting data into the table
add_insurred = ("INSERT INTO insurred "
                "( age, bmi, children, smoker, region, charges) "
                "VALUES ( %s, %s, %s, %s, %s, %s)")
for index, row in processed.iterrows():
    try:
        data_insurred = ( row["age"], row["bmi"], row["children"], row["smoker"], row["region"], row["charges"])
        db.cursor.execute(add_insurred, data_insurred)
        db.connection.commit()
    except mysql.Error as err:
        print("Failed inserting data: {}".format(err))
        exit(1)
db.close()


# try:
#     cnx = mysql.connect(user="root" , password="hamza123", host="localhost", database = "login-db")
# except mysql.Error as err:
#   if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#     print("Something is wrong with your user name or password")
#   elif err.errno == errorcode.ER_BAD_DB_ERROR:
#     print("Database does not exist")
#   else:
#     print(err)
# cursor = cnx.cursor()

# def create_database(cursor):
#     try:
#         cursor.execute(
#             "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
#     except mysql.Error as err:
#         print("Failed creating database: {}".format(err))
#         exit(1)

# try:
#     cursor.execute("USE {}".format(DB_NAME))
# except mysql.Error as err:
#     print("Database {} does not exists.".format(DB_NAME))
#     if err.errno == errorcode.ER_BAD_DB_ERROR:
#         create_database(cursor)
#         print("Database {} created successfully.".format(DB_NAME))
#         cnx.database = DB_NAME
#     else:
#         print(err)
#         exit(1)


# cursor.execute("Use {}".format(DB_NAME))
# try:
#     cursor.execute("CREATE TABLE IF NOT EXISTS insurred (id INT AUTO_INCREMENT PRIMARY KEY, age INT NOT NULL, bmi FLOAT NOT NULL, children INT NOT NULL, smoker VARCHAR(20), region VARCHAR(20), charges FLOAT NOT NULL)")
# except mysql.Error as err:
#     print("Failed creating table: {}".format(err))
#     exit(1)
# try:
#     cursor.execute("ALTER TABLE insurred DROP COLUMN name")
# except mysql.Error as err:
#     print("Failed dropping column: {}".format(err))
#     exit(1)
