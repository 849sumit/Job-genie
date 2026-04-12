from tabnanny import check
from unittest import result

from flask import Flask, request, jsonify

import userDashboard

from job_genie_backend.database import CheckCredential, InsertData
from job_genie_backend.schemas import UserSignup

from flask import Blueprint
user_login_bp = Blueprint('userlogin', __name__)
user_signup_bp = Blueprint('userSingup', __name__)

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
    print(name, email, contactNo, address, password, role, education, experience, preferredLocation)
    
    InsertData("Users", (name, email, contactNo, address, password, role, education, experience, preferredLocation))
    
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
    
    return jsonify({'message': 'Login successful'}), 200

# if __name__ == '__main__':
#     app.run(debug=True)