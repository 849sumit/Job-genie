import random
from datetime import date, timedelta
from sqlite3 import Row

from flask import jsonify, send_file
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
    Cursor.execute("CREATE TABLE IF NOT EXISTS resumes (id INT AUTO_INCREMENT PRIMARY KEY,filename VARCHAR(255),filepath VARCHAR(500), userId INT)")
    print("created")
    Cursor.close()
    cnx.close()

def InsertData(tableName, data):
    cnx = mysql.connector.connect(user='root', password='Sumit@24', host='localhost', database='JobGenie')
    Cursor = cnx.cursor()
    if tableName == "Users":
        Cursor.execute("INSERT INTO Users(name, email, contactNo, address, password, role, education, experience, preferredLocation) " \
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",tuple(data[:9]))
        cnx.commit()
        if(data[5] == 'company'):
            email = data[1]
            user_id = GetUserIdByEmail(email)[0]
            Cursor.execute("INSERT INTO company(userId, noOfEmployees, website, OperatingSince) VALUES (%s, %s, %s, %s)", (user_id, data[9], data[10], data[11]))
    elif tableName == "Jobs":
        Cursor.execute("INSERT INTO Jobs(companyName, title, description, location, salary, education, experience, skills, postedDate, lastDate) " \
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)", data)
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
    return result [0]

def GetUserIdByEmail(email):
    cnx = mysql.connector.connect(user='root', password='Sumit@24', host='localhost', database='JobGenie')
    Cursor = cnx.cursor()
    Cursor.execute("SELECT userId, name, password, role FROM Users WHERE email = %s", (email,))
    row = Cursor.fetchall()
    Cursor.close()
    cnx.close()
    return row[0] if row else None

def GetDashboardCountsByEmail(email):
    cnx = mysql.connector.connect(user='root', password='Sumit@24', host='localhost', database='JobGenie')
    Cursor = cnx.cursor()
    user_id = GetUserIdByEmail(email)[0]
    Cursor.execute("SELECT COUNT(*) FROM Appliedjobs WHERE userId = %s", (user_id,))
    applied_count = Cursor.fetchone()[0] or 0
    Cursor.execute("SELECT COUNT(*) FROM response WHERE userId = %s", (user_id,))
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
    today = date.today()
    last_week = today - timedelta(days=7)
    
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

def editValue(email, changeField, value) :
    user_id = GetUserIdByEmail(email)[0]
    cnx = mysql.connector.connect(user='root', password='Sumit@24', host='localhost', database='JobGenie')
    Cursor = cnx.cursor()
    if(changeField == 'Location'):
        Cursor.execute("update users set address = %s where userId = %s ", (value,user_id))
    elif(changeField == 'Phone'):
        Cursor.execute("update users set contactNo = %s where userId = %s ", (value,user_id))
    elif(changeField == 'Education'):
        Cursor.execute("update users set education = %s where userId = %s ", (value,user_id))
    elif(changeField == 'NoOfEmployees'):
        Cursor.execute("update company set noOfEmployees = %s where userId = %s", ((value,user_id)))
    cnx.commit()
    Cursor.close()
    cnx.close()

def getProfileData(email):
    user_id = GetUserIdByEmail(email)[0]
    role = GetUserIdByEmail(email)[3]
    cnx = mysql.connector.connect(user='root', password='Sumit@24', host='localhost', database='JobGenie')
    Cursor = cnx.cursor()
    if(role == 'company'):
        Cursor.execute("select u.*, c.noOfEmployees, c.website, DATE_FORMAT(c.OperatingSince, '%Y-%m-%d') from users u join company c on c.userId = u.userId  where u.userId = %s ", (user_id,))
    else:
        Cursor.execute("select * from users where userId = %s", (user_id,))
    row = Cursor.fetchall()
    print('row printed')
    print(row)
    Cursor.close()
    cnx.close()
    return row


def saveResume(file, file_path):
    # user_id = GetUserIdByEmail(email)[0]
    cnx = mysql.connector.connect(user='root', password='Sumit@24', host='localhost', database='JobGenie')
    cursor = cnx.cursor()

    cursor.execute(
        "INSERT INTO resumes (filename, filepath) VALUES (%s, %s)",
        (file.filename, file_path)
    )

    cnx.commit()
    resume_id = cursor.lastrowid
    cursor.close()
    cnx.close()

    return jsonify({
        "id": resume_id,
        "filename": file.filename
    })

def downloadResume(id):
    cnx = mysql.connector.connect(user='root', password='Sumit@24', host='localhost', database='JobGenie')
    cursor = cnx.cursor(dictionary=True)

    cursor.execute("SELECT * FROM resumes WHERE id = %s", (id,))
    resume = cursor.fetchone()

    cursor.close()
    cnx.close()

    if not resume:
        return jsonify({"error": "File not found"}), 404

    return send_file(
        resume['filepath'],
        as_attachment=True,
        download_name=resume['filename']
    )

def GetCompanyDashboardCountsByEmail(email):
    # Example: query total applicants vs accepted candidates for this company
    return [
        {"title": "Applied", "value": 42, "color": "#2563eb"},
        {"title": "Accepted", "value": 18, "color": "#10b981"}
    ]

def GetApplicationsByRole(email):
    # Example: query applications grouped by job role
    return [
        {"title": "Software Engineer", "value": 12, "color": "#3b82f6"},
        {"title": "Data Analyst", "value": 8, "color": "#f59e0b"},
        {"title": "UI/UX Designer", "value": 6, "color": "#8b5cf6"},
        {"title": "ML Engineer", "value": 5, "color": "#ef4444"},
        {"title": "Content Strategist", "value": 4, "color": "#14b8a6"}
    ]

def GetLastWeekHiringActivity(email):
    # Example: query daily applied vs accepted counts for the past week
    return [
        {"date": "Mon", "applied": 5, "accepted": 2},
        {"date": "Tue", "applied": 6, "accepted": 3},
        {"date": "Wed", "applied": 4, "accepted": 1},
        {"date": "Thu", "applied": 7, "accepted": 3},
        {"date": "Fri", "applied": 8, "accepted": 4},
        {"date": "Sat", "applied": 3, "accepted": 1},
        {"date": "Sun", "applied": 2, "accepted": 0}
    ]

def GetApplicantsByCompanyEmail(email):
    cnx = mysql.connector.connect(user='root', password='Sumit@24', host='localhost', database='JobGenie')
    cursor = cnx.cursor(dictionary=True)
    company_name = GetUserIdByEmail(email)[1]
    cursor.execute("""
        select a.userId, a.jobId, a.userName, a.appliedDate, a.status, j.title, j.description, u.education, u.email, u.experience, u.skills, u.preferredLocation 
        from appliedjobs a 
        JOIN users u ON a.userId = u.userId
        JOIN jobs j ON a.jobId = j.jobId
        where a.companyName = %s ;
    """, (company_name,))
    result = cursor.fetchall()
    cnx.close()
    return result

def updateStatus(value, userId, jobId):
    cnx = mysql.connector.connect(user='root', password='Sumit@24', host='localhost', database='JobGenie')
    cursor = cnx.cursor()
    cursor.execute("Update appliedJobs set status = %s where userId= %s and jobId = %s", (value, userId, jobId))
    cnx.commit()
    cursor.close()
    cnx.close()

def GetJobHistoryCompany(email):
    company_name = GetUserIdByEmail(email)[1]
    cnx = mysql.connector.connect(user='root', password='Sumit@24', host='localhost', database='JobGenie')
    Cursor = cnx.cursor()
    Cursor.execute("select title, postedDate ,lastDate, experience, count(j.userId) as count from jobs a JOIN appliedjobs j ON a.jobId = j.jobId where a.companyName = %s group by a.jobId; ", (company_name,))
    results = Cursor.fetchall()
    print(results)
    Cursor.close()
    cnx.close()
    return results