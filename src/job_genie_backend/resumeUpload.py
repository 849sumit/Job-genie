import os
import re
import uuid
from flask import Blueprint, jsonify, request

from job_genie_backend.database import downloadResume, saveResume

resume_upload_bp = Blueprint('resumeUpload', __name__)
resumeDownload_bp = Blueprint('resumedownload', __name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@resume_upload_bp.route('/upload', methods=['POST'])
def upload_resume():
    print(request)
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']

    print(file)
    if not file.filename.endswith('.pdf'):
        return jsonify({"error": "Only PDF allowed"}), 400

    # unique filename
    filename = str(uuid.uuid4()) + ".pdf"
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    file.save(file_path)

    return saveResume(file, file_path)

@resumeDownload_bp.route('/download/<int:id>', methods=['GET'])
def download_resume(id):

    return downloadResume(id)