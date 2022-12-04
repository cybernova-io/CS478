from asyncore import write
from flask import flash, redirect, current_app as app, request, jsonify
from werkzeug.utils import secure_filename
import os
from os import listdir
import re
from datetime import datetime, timedelta


class WebUtils:
    def __init__(self, request):

        self.request = request
        self.ALLOWED_EXTENSIONS = {"txt", "json"}

    def allowed_file(self, filename):
        return (
            "." in filename
            and filename.rsplit(".", 1)[1].lower() in self.ALLOWED_EXTENSIONS
        )

    def handle_upload(self):

        if "file" not in self.request.files:

            data = {"msg": "No file submitted."}

            resp = jsonify(data)
            resp.status_code = 400

            return resp

        fileObject = self.request.files["file"]

        if fileObject.filename == "":

            data = {"msg": "Filename is empty."}

            resp = jsonify(data)
            resp.status_code = 400

            return resp

        if fileObject and self.allowed_file(fileObject.filename):
            filename = secure_filename(fileObject.filename)
            fileObject.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            file_path = "app/uploads/" + filename
            return file_path

    def delete_file(self):

        file_name = self.request.args.get("filename")

        if file_name is None:
            files = listdir("app/uploads/")
            if files == None:
                return "No files found."
            else:
                for i in files:
                    os.remove("app/uploads/" + i)
            return "All files successfully deleted."
        else:
            filename = secure_filename(file_name)
            file_path = "app/uploads/" + filename
            os.remove(file_path)
            return filename + " successfully deleted."

    def delete_file_form(self, directory):

        if directory == "uploads":
            file_name = self.request.form["file_name"]

            filename = secure_filename(file_name)
            file_path = "app/uploads/" + filename
            os.remove(file_path)
            return filename + " successfully deleted."

    def time_in_range_one_week(time):
        """Returns whether current is within a week of now."""
        current = datetime.utcnow()

        end = current + timedelta(days=10)

        return current <= time <= end