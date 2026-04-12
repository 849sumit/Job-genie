import random
from datetime import date, timedelta
from sqlite3 import Row

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
    Cursor.execute("CREATE TABLE IF NOT EXISTS response(userId int(5), jobId int(5), userName varchar(20), companyName varchar(100), appliedDate Date, status varchar(20))")
    print("created")
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
    elif tableName == "response":
        Cursor.execute("INSERT INTO response(userId, jobId, userName, companyName, appliedDate, status) VALUES (%s, %s, %s, %s, %s, %s)", data)
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

def GetUserIdByEmail(email):
    cnx = mysql.connector.connect(user='root', password='Sumit@24', host='localhost', database='JobGenie')
    Cursor = cnx.cursor()
    Cursor.execute("SELECT userId, name, password FROM Users WHERE email = %s", (email,))
    row = Cursor.fetchall()
    Cursor.close()
    cnx.close()
    return row[0] if row else None

def GetDashboardCountsByEmail(email):
    cnx = mysql.connector.connect(user='root', password='Sumit@24', host='localhost', database='JobGenie')
    Cursor = cnx.cursor()
    Cursor.execute("SELECT COUNT(*) FROM Appliedjobs WHERE userId = (select userId from Users where email = %s LIMIT 1)", (email,))
    applied_count = Cursor.fetchone()[0] or 0
    Cursor.execute("SELECT COUNT(*) FROM response WHERE userId = (select userId from Users where email = %s  LIMIT 1)", (email,))
    response_count = Cursor.fetchone()[0] or 0
    print(applied_count,response_count)
    Cursor.close()
    cnx.close()

    appliedSummary = [
        { "title": "Applied", "value": applied_count, "color": "#2563eb" },
        { "title": "Responses", "value": response_count, "color": "#10b981" }
    ]

    return appliedSummary



def GetJobTitlesCount(email):
    user_id = GetUserIdByEmail(email)[0]
    cnx = mysql.connector.connect(user='root', password='Sumit@24', host='localhost', database='JobGenie')
    Cursor = cnx.cursor()
    Cursor.execute("select title, count(*) from Jobs where jobId in (select jobId from Appliedjobs where userId = %s) group by title", (user_id,))
    results = Cursor.fetchall()
    print(results)
    Cursor.close()
    cnx.close()

    def random_color():
        return "#{:06x}".format(random.randint(0, 0xFFFFFF))

    sectorSummary = [
        {"title": title, "value": count, "color": random_color()}
        for title, count in results
    ]

    return sectorSummary

def GetlastWeekActivity(email):
    user_id = GetUserIdByEmail(email)[0]
    user_name =GetUserIdByEmail(email)[1]
    print(user_name)
    today = date.today()
    print(user_id, today)
    last_week = today - timedelta(days=7)
    print(last_week)
    cnx = mysql.connector.connect(user='root', password='Sumit@24', host='localhost', database='JobGenie')
    Cursor = cnx.cursor()
    Cursor.execute("SELECT COUNT(*) AS applied_jobs, appliedDate FROM appliedjobs WHERE userId = %s AND appliedDate BETWEEN %s AND %s group by appliedDate", (user_id, last_week, today))
    applied_results = Cursor.fetchall()
    print("Applied results:", applied_results)

    Cursor.execute("SELECT COUNT(*) AS applied_jobs, responseDate FROM response WHERE userId = %s AND responseDate BETWEEN %s AND %s group by responseDate;", (user_id, last_week, today))
    response_results = Cursor.fetchall()
    print("Response results:", response_results)
    Cursor.close()
    cnx.close()

    print(applied_results)
    print(response_results)

    applied_dict = {r[1]: r[0] for r in applied_results}
    response_dict = {r[1]: r[0] for r in response_results}

    print("Applied dict:", applied_dict)
    print("Response dict:", response_dict)

    # Build final list for the last 7 days
    week_activity = []
    for i in range(7):
        day_date = last_week + timedelta(days=i)
        week_activity.append({
            "date": day_date.strftime("%Y-%m-%d"),
            "applied": applied_dict.get(day_date, 0),
            "responded": response_dict.get(day_date, 0)
        })
    print(week_activity)
    return week_activity


def  GetJobHistory(email) : 
    user_id = GetUserIdByEmail(email)[0]
    cnx = mysql.connector.connect(user='root', password='Sumit@24', host='localhost', database='JobGenie')
    Cursor = cnx.cursor()
    Cursor.execute("select j.title, a.companyName, DATE_FORMAT(a.appliedDate, '%Y-%m-%d'), a.status from appliedjobs a JOIN jobs j ON a.jobId = j.jobId where a.userId = %s ", (user_id,))
    results = Cursor.fetchall()
    print(results)
    Cursor.close()
    cnx.close()
    return results

def GetJobDetails() :
    cnx = mysql.connector.connect(user='root', password='Sumit@24', host='localhost', database='JobGenie')
    Cursor = cnx.cursor()
    Cursor.execute("select companyName, title, location, DATE_FORMAT(lastDate, '%Y-%m-%d') AS lastDate, DATE_FORMAT(postedDate, '%Y-%m-%d') AS postedDate , description, salary, experience, skills, jobId from jobs")
    results = Cursor.fetchall()
    print(results)
    Cursor.close()
    cnx.close()
    return results

def applyForPost(email, jobId) :
    user_id = GetUserIdByEmail(email)[0]
    user_name =GetUserIdByEmail(email)[1]
    company_Name =GetCompanyNameByJobId(jobId)[0]
    InsertData('AppliedJobs', (user_id, jobId, user_name, company_Name, date.today(),'pending'))

def GetCompanyNameByJobId(jobId) :
    cnx = mysql.connector.connect(user='root', password='Sumit@24', host='localhost', database='JobGenie')
    Cursor = cnx.cursor()
    Cursor.execute("select companyName from jobs where jobId = %s",(jobId,))
    row = Cursor.fetchall()
    print(row)
    Cursor.close()
    cnx.close()
    return row[0] if row else None

def isChangePassword(email, oldPassword) :
    user_password = GetUserIdByEmail(email)[2]
    if(user_password == oldPassword) :
        return 1
    else :
        return 0
    
def ChangePassword(email, password) :
    user_id = GetUserIdByEmail(email)[0]
    cnx = mysql.connector.connect(user='root', password='Sumit@24', host='localhost', database='JobGenie')
    Cursor = cnx.cursor()
    Cursor.execute("update users set password = %s where userId = %s ", (password,user_id))
    cnx.commit()
    Cursor.close()
    cnx.close()