from flask import Flask, app, jsonify, request

from job_genie_backend.database import ChangePassword, GetDashboardCountsByEmail, GetJobHistory, GetJobTitlesCount, GetlastWeekActivity, GetJobDetails, applyForPost, isChangePassword

from flask import Blueprint

user_dashboard_bp = Blueprint('user_dashboard', __name__)
job_history_bp = Blueprint('job_history',__name__)
applyNow_bp = Blueprint('applyNow', __name__)
apply_bp = Blueprint('apply', __name__)
ChangePassword_bp = Blueprint('changePassword', __name__)

@user_dashboard_bp.route('/dashboard', methods=['GET'])
def dashboard():
    email = request.args.get('email')
    print(email)

    dashboardResponse = {
        "appliedVsResponse":  GetDashboardCountsByEmail(email),
        "ApplicationsBySector": GetJobTitlesCount(email),
        "lastWeekActivity" : GetlastWeekActivity(email)
    }
    print("final response ", dashboardResponse)
    return dashboardResponse



@job_history_bp.route('/jobhistory', methods=['GET'])
def history():
    email = request.args.get('email')
    print(email)

    return GetJobHistory(email)



@applyNow_bp.route('/applyNow', methods=['GET'])
def applyNow():

    return GetJobDetails()

@apply_bp.route('/apply',methods=['POST'])
def apply() :
    user = request.get_json() 
    email = user.get('email')
    jobId = user.get('jobId')
    applyForPost(email,jobId)
    print("inserted successfully")
    return jsonify({"message": "Application submitted successfully"}), 200


@ChangePassword_bp.route('/changePassword',methods=['POST'])
def changePassword() :
    user = request.get_json() 
    email = user.get('email')
    password = user.get('newPassword')
    oldPassword = user.get('oldPassword')
    if(isChangePassword(email, oldPassword)==1):
        ChangePassword(email, password)
        return jsonify({"message": "Application submitted successfully"}), 200
    else :
        return jsonify({"message": "Old Password is not correct"}), 500