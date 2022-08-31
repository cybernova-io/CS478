from flask import Blueprint, redirect, render_template, flash, request, session, url_for, send_from_directory
from flask_login import login_required, logout_user, current_user, login_user
from ..models import db, User
from .. import login_manager
from flask_login import logout_user
from sqlalchemy import create_engine, MetaData
import json
from flask import current_app as app



app_bp = Blueprint('app_bp', __name__)

@app_bp.route('/', methods = ['GET'])
def index():
    return 'Index'

@app_bp.route('/download_db', methods=['GET'])
def dump_sqlalchemy():
    """ Returns the entire content of the database. """
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    meta = MetaData()
    meta.reflect(bind=engine)  # http://docs.sqlalchemy.org/en/rel_0_9/core/reflection.html
    result = {}
    for table in meta.sorted_tables:
        if table.name != 'User':
            result[table.name] = [dict(row) for row in engine.execute(table.select())]

    with open('app/uploads/database.json', 'w') as file:
        json.dump(result, file)
    file.close()

    return send_from_directory('uploads', 'database.json', as_attachment=True)

@app_bp.route('/upload_db', methods=['GET', 'POST'])
def load_sqlalchemy():
    """ Processes a database json file dump. """
    if request.method == 'GET':
        return '''
                    <!doctype html>
                    <title>DB Importer</title>
                    <h>Upload exported DB JSON file.</h1>
                    <form method=post enctype=multipart/form-data>
                        <input type=file name=file>
                            <input type=submit value=Upload>
                    </form>
                '''

    if request.method == 'POST':
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
       
        file_path = WebUtils(request).handle_upload()
        data = ''

        file = open(file_path)
        data = json.load(file)

        for row in data['TableName']:
            engine.execute(
                TableName.__table__.insert(),
                row
            )

        return 'Database loaded.'