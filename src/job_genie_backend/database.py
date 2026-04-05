import mysql.connector

def DatabaseCreate():
    cnx = mysql.connector.connect(user='root', password='Sumit@24', host='localhost')
    print("Connected to MySQL server successfully!")
    Cursor = cnx.cursor()
    Cursor.execute("")
    Cursor.close()
    cnx.close()


def DatabaseShow():
    conn = mysql.connector.connect(user='root', password='Sumit@24', host='localhost', database='JobGenie')
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    for table in cursor:
        print(table[0])
    cursor.close()
    conn.close()

def TablesCreate():
    cnx = mysql.connector.connect(user='root', password='Sumit@24', host='localhost', database='JobGenie')
    Cursor = cnx.cursor()
    Cursor.execute("CREATE TABLE IF NOT EXISTS Users(userId int AUTO_INCREMENT PRIMARY KEY, name varchar(20), email varchar(20), contactNo int(10), address varchar(100), password varchar(100), role varchar(20),education varchar(100), experience varchar(100),preferredLocation varchar(100))")
    Cursor.execute("CREATE TABLE IF NOT EXISTS Jobs(jobId int AUTO_INCREMENT PRIMARY KEY,companyName varchar(100), title varchar(100), description varchar(255), location varchar(100), salary int(10),education varchar(100), experience varchar(100),skills varchar(100), postedDate Date, lastDate Date)")
    Cursor.execute("CREATE TABLE IF NOT EXISTS AppliedJobs(userId int(5), jobId int(5), userName varchar(20), companyName varchar(100), appliedDate Date, status varchar(20))")
    Cursor.close()
    cnx.close()

def InsertData(tableName, data):
    cnx = mysql.connector.connect(user='root', password='Sumit@24', host='localhost', database='JobGenie')
    Cursor = cnx.cursor()
    if tableName == "Users":
        print("Inserting data into Users table...")
        Cursor.execute("INSERT INTO Users(name, email, contactNo, address, password, role, education, experience, preferredLocation) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", data)
    elif tableName == "Jobs":
        Cursor.execute("INSERT INTO Jobs(companyName, title, description, location, salary, education, experience, skills, postedDate, lastDate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)", data)
    elif tableName == "AppliedJobs":
        Cursor.execute("INSERT INTO AppliedJobs(userId, jobId,userName ,companyName ,appliedDate ,status) VALUES (%s,%s,%s,%s,%s,%s)", data)
    cnx.commit()
    Cursor.close()
    cnx.close()

def CheckCredential(email, password):
    cnx = mysql.connector.connect(user='root', password='Sumit@24', host='localhost', database='JobGenie')
    Cursor = cnx.cursor()
    Cursor.execute("SELECT * FROM Users WHERE email = %s AND password = %s", (email, password))
    result = Cursor.fetchall()
    Cursor.close()
    cnx.close()
    return result 