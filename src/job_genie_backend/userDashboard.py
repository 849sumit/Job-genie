from flask import jsonify, request

from flask import Blueprint, jsonify, request
from job_genie_backend.database import (
    GetApplicantsByCompanyEmail,
    GetCompanyDashboardCountsByEmail,
    GetApplicationsByRole,
    GetJobHistoryCompany,
    GetLastWeekHiringActivity,
    updateStatus
)


from job_genie_backend.database import ChangePassword, GetDashboardCountsByEmail, GetJobHistory, GetJobTitlesCount, GetlastWeekActivity, GetJobDetails, applyForPost, editValue, getProfileData, isChangePassword

from flask import Blueprint

user_dashboard_bp = Blueprint('user_dashboard', __name__)
job_history_bp = Blueprint('job_history',__name__)
applyNow_bp = Blueprint('applyNow', __name__)
apply_bp = Blueprint('apply', __name__)
ChangePassword_bp = Blueprint('changePassword', __name__)
edit_bp = Blueprint('edit',__name__)
profile_bp = Blueprint('profile',__name__)
company_dashboard_bp = Blueprint('company_dashboard', __name__)
company_Applicants_bp = Blueprint('company_Applicants', __name__)
update_Status_bp = Blueprint('update_Status',__name__)
job_history_company_bp = Blueprint('job_history_company',__name__)

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

    return GetJobHistory(email)

@job_history_company_bp.route('/jobhistoryCompany', methods=['GET'])
def historyCompany():
    email = request.args.get('email')

    return GetJobHistoryCompany(email)


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


@edit_bp.route('/edit', methods=['POST'])
def edit() :
    user = request.get_json() 
    email = user.get('email')
    changedField = user.get('changedField')
    value = user.get('value')
    editValue(email,changedField,value)
    return jsonify({"message": "Edit successfully"}), 200

@profile_bp.route('/profile', methods=['GET'])
def profile() :
    email = request.args.get('email')
    print('result')
    return getProfileData(email)


@company_dashboard_bp.route('/companyDashboard', methods=['GET'])
def company_dashboard():
    email = request.args.get('email')
    print("Company dashboard requested for:", email)

    dashboard_response = {
        "appliedVsAccepted": GetCompanyDashboardCountsByEmail(email),
        "applicationsByRole": GetApplicationsByRole(email),
        "lastWeekHiringActivity": GetLastWeekHiringActivity(email)
    }

    print("Final company dashboard response:", dashboard_response)
    return jsonify(dashboard_response)

@company_Applicants_bp.route('/companyApplicants', methods=['GET'])
def company_applicants():
    email = request.args.get('email')
    print("Company applicants requested for:", email)

    applicants = GetApplicantsByCompanyEmail(email)

    return jsonify(applicants)

@update_Status_bp.route('/status', methods=['POST'])
def status():
    value = request.get_json()
    jobId = value.get('jobId')
    userId = value.get('userId')
    status = value.get('status')
    updateStatus(status, userId, jobId)
    return jsonify({"message": "Status Updated"}), 200