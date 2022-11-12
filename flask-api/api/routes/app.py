from flask import (
    Blueprint,
    request,
    send_from_directory,
)
from ..models.Users import db, User
from .. import login_manager
from flask_security import login_required
from sqlalchemy import create_engine, MetaData
import json
from flask import current_app as app, jsonify
from ..services import WebUtils
from api.services.DBStartup import seed_db
from datetime import datetime
from flask_jwt_extended import jwt_required, current_user
from datetime import timezone
from datetime import timedelta
from flask_jwt_extended import (
    get_jwt,
    create_access_token,
    get_jwt_identity,
    set_access_cookies,
)


app_bp = Blueprint("app_bp", __name__)


@app.before_first_request
def start_up():
    seed_db()


@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response


@app_bp.route("/", methods=["GET"])
def index():
    return "Index"


@app_bp.get("/api/time")
@jwt_required()
def time():
    return jsonify({"time": "HELLOOOO"})


@app_bp.route("/download_db", methods=["GET"])
@jwt_required()
def dump_sqlalchemy():
    """Returns the entire content of the database."""
    engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    meta = MetaData()
    meta.reflect(
        bind=engine
    )  # http://docs.sqlalchemy.org/en/rel_0_9/core/reflection.html
    result = {}
    for table in meta.sorted_tables:
        result[table.name] = [dict(row) for row in engine.execute(table.select())]

    with open(app.config["UPLOADS"] + "/database.json", "w") as file:
        json.dump(result, file, default=str)
    file.close()

    return send_from_directory(
        app.config["UPLOADS"], "database.json", as_attachment=True
    )


@app_bp.route("/upload_db", methods=["GET", "POST"])
@jwt_required()
def load_sqlalchemy():
    """Processes a database json file dump."""
    if request.method == "GET":
        return """
                    <!doctype html>
                    <title>DB Importer</title>
                    <h>Upload exported DB JSON file.</h1>
                    <form method=post enctype=multipart/form-data>
                        <input type=file name=file>
                            <input type=submit value=Upload>
                    </form>
                """

    if request.method == "POST":
        engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])

        file_path = WebUtils(request).handle_upload()
        data = ""

        file = open(file_path)
        data = json.load(file)

        for row in data["User"]:
            engine.execute(User.__table__.insert(), row)

        return "Database loaded."
