import mysql.connector as mysql
from mysql.connector import errorcode 
class DataBase:
    def __init__(self, root: str, password:str, host:str, database:str ) -> None:
        self.root = root
        self.password = password
        self.host = host
        self.database = database
        self.__isConnectionAcheived = False
        self.__isDatabaseCreated = False
        self.connection = self.connectToDB()
        self.cursor = self.connection.cursor()
    def getConnectionStatus(self):
        print(self.__isConnectionAcheived)
        return self.__isConnectionAcheived
    def getDatabaseCreationStatus(self):
        print(self.__isDatabaseCreated)
        return self.__isDatabaseCreated
    def connectToDB(self):
        try:
            cnx = mysql.connect(user=self.root , password=self.password, host=self.host, database = self.database)
            self.__isConnectionAcheived = True
            return cnx
        except mysql.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
            self.__iscConnectionAcheived = False
        
    def createDatabase(self, dbName:str):
        if self.__isConnectionAcheived == False:
            self.connectToDB()
        try:
            self.cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(dbName))
            self.__isDatabaseCreated = True
        except mysql.Error as err:
            self.__isDatabaseCreated = False
            print("Failed creating database: {}".format(err))
            return
    def useDB(self, dbName):
        if self.__isConnectionAcheived == False:
            self.connectToDB()
        try:
            self.cursor.execute("USE {}".format(dbName))
        except mysql.Error as err:
            print("Database {} does not exists.".format(dbName))
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.createDatabase(dbName)
                print("Database {} created successfully.".format(dbName))
                self.connection.database = dbName
            else:
                print(err)
                exit(1)
    def execute(self, command):
        if self.__isConnectionAcheived == False:
            self.connectToDB()
        self.cursor.execute(command)
        self.connection.commit()
    def createTable(self, tableName, columns):
        if self.__isConnectionAcheived == False:
            self.connectToDB()
        try:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS {} ({})".format(tableName, columns))
        except mysql.Error as err:
            print("Failed creating table: {}".format(err))
            exit(1)
    def insertData(self, tableName, columns, values):
        if self.__isConnectionAcheived == False:
            self.connectToDB()
        try:
            self.cursor.execute("INSERT INTO {} ({}) VALUES ({})".format(tableName, columns, values))
        except mysql.Error as err:
            print("Failed inserting data: {}".format(err))
            exit(1)
    def deleteDB(self, dbName):
        if self.__isConnectionAcheived == False:
            self.connectToDB()
        try:
            self.cursor.execute("DROP DATABASE {}".format(dbName))
        except mysql.Error as err:
            print("Failed deleting database: {}".format(err))
            exit(1)
    def clearTable(self, tableName):
        if self.__isConnectionAcheived == False:
            self.connectToDB()
        try:
            self.cursor.execute("DELETE FROM {}".format(tableName))
        except mysql.Error as err:
            print("Failed clearing table: {}".format(err))
            exit(1)
    def deleteTable(self, tableName):
        if self.__isConnectionAcheived == False:
            self.connectToDB()
        try:
            self.cursor.execute("DROP TABLE {}".format(tableName))
        except mysql.Error as err:
            print("Failed deleting table: {}".format(err))
            exit(1)
    def close(self):
        self.connection.close()