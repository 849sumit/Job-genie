from datetime import date

from flask import request, jsonify

from job_genie_backend.database import CheckCredential, GetUserIdByEmail, InsertData

from flask import Blueprint
user_login_bp = Blueprint('userlogin', __name__)
user_signup_bp = Blueprint('userSingup', __name__)
New_Job_bp = Blueprint('New_Job', __name__ )

@user_signup_bp.route('/signUp', methods=['POST'])
def sign_up():
    user = request.get_json() 
    
    if not user:
        return jsonify({'error': 'No data provided'}), 400
    
    name = user.get('name')
    email = user.get('email')
    contactNo = user.get('contactNo')
    address = user.get('address')
    password = user.get('password')
    role = user.get('role', 'candidate')
    education = user.get('education')
    experience = user.get('experience')
    preferredLocation = user.get('preferredLocation', 'All India')
    noOfEmployees = user.get('noOfEmployees')
    website = user.get('website')
    operatingSince = user.get('operatingSince')
    print(name, email, contactNo, address, password, role, education, experience, preferredLocation)
    
    InsertData("Users", (name, email, contactNo, address, password, role, education, experience, preferredLocation, noOfEmployees, website, operatingSince))
    
    return jsonify({'message': 'User created successfully'}), 201

@user_login_bp.route('/login', methods=['GET'])
def login():
    print(request.args)
    email = request.args.get('email')
    password = request.args.get('password')
    result = CheckCredential(email, password)
    print('result', result)
    if not result:
        return jsonify({'error': 'Invalid email or password'}), 401
    
    role = result[6]

    return jsonify(role)

@New_Job_bp.route('/NewJob', methods=['POST'])
def postJob():
    user = request.get_json() 

    email = user.get('email')
    title = user.get('title')
    description = user.get('description')
    salary = user.get('salary')
    experience = user.get('experience')
    education = user.get('education')
    lastDate = user.get('lastDate')
    skills = user.get('skills')
    location = user.get('location', 'All India')

    company_name = GetUserIdByEmail(email)[1]

    InsertData("Jobs", (company_name,title, description, location, salary, education, experience, skills, date.today(), lastDate))
    
    return jsonify({'message': 'Job created successfully'}), 201