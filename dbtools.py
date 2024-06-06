import mysql.connector
from datetime import datetime

class Dbfunc:
    def __init__(self, host="localhost", user="root", password="nir123", database=None):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.mydb = self.init()
        if self.database:
            self.init_with_db(self.database)

    def init(self):
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password
        )

    def init_with_db(self, dbName):
        self.mydb = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=dbName
        )

    def show_databases(self):
        mycursor = self.mydb.cursor()
        mycursor.execute("SHOW DATABASES")
        databases = []
        for i in mycursor:
            databases.append(i[0])
        return databases

    def create_database(self, dbName):
        mycursor = self.mydb.cursor()
        if dbName not in self.show_databases():
            mycursor.execute("CREATE DATABASE " + dbName)

    def show_tables(self):
        mycursor = self.mydb.cursor()
        mycursor.execute("SHOW TABLES")
        tables = []
        for i in mycursor:
            tables.append(i[0])
        return tables

    def create_table(self, mydb, tableName, params):
        tables = self.show_tables()
        mycursor = self.mydb.cursor()
        query = "CREATE TABLE " + tableName + " " + params
        print(query)
        if tableName not in tables:
            mycursor.execute(query)

    def delete_table(self, tableName):
        tables = self.show_tables()
        mycursor = self.mydb.cursor()
        query = "DROP TABLE " + tableName
        print(query)
        if tableName in tables:
            mycursor.execute(query)

    def insert_row(self, tableName, columnNames, columnTypes, columnValues):
        mycursor = self.mydb.cursor()
        tables = self.show_tables()
        if tableName in tables:
            sql = "INSERT INTO " + tableName + " " + columnNames + " VALUES " + columnTypes
            print(sql)
            mycursor.execute(sql, columnValues)
            self.mydb.commit()
        else:
            print("No table exists with name " + tableName)

    def delete_row(self, tableName, columnName, columnValue):
        mycursor = self.mydb.cursor()
        tables = self.show_tables()
        if tableName in tables:
            sql = "DELETE FROM " + tableName + " WHERE " + columnName + " =  '" + columnValue + "'"
            print(sql)
            mycursor.execute(sql)
            self.mydb.commit()
        else:
            print("No column name with name " + tableName)

    def get_all_rows(self, tableName):
        mycursor = self.mydb.cursor()
        sql = "SELECT * FROM " + tableName
        mycursor.execute(sql)
        rows = []
        print(mycursor)
        for i in mycursor:
            rows.append(i)
        return rows

    def get_rows_from_table_with_value(self, tableName, columnName, columnValue):
        mycursor = self.mydb.cursor()
        tables = self.show_tables()
        if tableName in tables:
            sql = "SELECT * FROM " + tableName + " WHERE " + columnName + " =  '" + columnValue + "'"
            print(sql)
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            return myresult
        else:
            print("No column name with name " + tableName)


# Example usage:
# db = Dbfunc()
# db.create_database("mydatabase")
# db.create_table("mytable", "(id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255))")
# db.insert_row("mytable", "(name, email)", "(%s, %s)", ("John", "john@example.com"))
# rows = db.get_all_rows("mytable")
# for row in rows:
#     print(row)