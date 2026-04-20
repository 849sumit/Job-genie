from flask_cors import CORS

from job_genie_backend.userDashboard import user_dashboard_bp, job_history_bp, applyNow_bp, apply_bp, ChangePassword_bp,edit_bp,profile_bp, company_dashboard_bp, company_Applicants_bp,update_Status_bp, job_history_company_bp
from job_genie_backend.logInSignUp import user_login_bp,user_signup_bp,New_Job_bp
from job_genie_backend.resumeUpload import resume_upload_bp, resumeDownload_bp

from flask import Flask
app = Flask(__name__)

CORS(app)

# Register all blueprints
app.register_blueprint(user_dashboard_bp)
app.register_blueprint(user_signup_bp)
app.register_blueprint(user_login_bp)
app.register_blueprint(job_history_bp)
app.register_blueprint(applyNow_bp)
app.register_blueprint(apply_bp)
app.register_blueprint(ChangePassword_bp)
app.register_blueprint(edit_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(resumeDownload_bp)
app.register_blueprint(resume_upload_bp)
app.register_blueprint(company_dashboard_bp)
app.register_blueprint(company_Applicants_bp)
app.register_blueprint(update_Status_bp)
app.register_blueprint(job_history_company_bp)
app.register_blueprint(New_Job_bp)

@app.route('/')
def home():
    return "Job Genie Backend running!"


if __name__ == "__main__":
    app.run(debug=True)

