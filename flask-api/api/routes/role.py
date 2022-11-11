from api.models.Users import Role
from api.models.db import db
from flask import Blueprint, request
import logging
from flask_security import current_user
from api.services.WebHelpers import WebHelpers

role_bp = Blueprint("role_bp", __name__)


@role_bp.get("/api/role/<int:id>")
def get_role(id):

    role = Role.query.get(id)
    if role:
        logging.info(f"User id - {current_user.id} - accessed role id - {role.id} -")
        resp = role.serialize()
        resp.status_code = 200
        return resp
    return WebHelpers.EasyResponse(f"Role with id {id} doesnt exist.", 404)


@role_bp.get("/api/role")
def get_roles():

    role = Role.query.all()
    logging.info(f"User id - {current_user.id} accessed all roles.")
    roles = [x.serialize() for x in role]
    resp = roles
    resp.status_code = 200
    return resp


@role_bp.post("/api/role")
def create_role():

    role_name = request.form["name"]
    role_description = request.form["description"]

    role = Role(name=role_name, description=role_description)

    db.session.add(role)
    db.session.commit()
    logging.warning(f"User id - {current_user.id} - created new role id - {role.id} -")
    return role.serialize()


@role_bp.put("/api/role/<int:id>")
def update_role(id):

    role = Role.query.get(id)

    if role:
        role_name = request.form["name"]
        role_description = request.form["description"]

        role.name = role_name
        role.description = role_description
        db.session.commit()

        logging.warning(f"User id - {current_user.id} - modified role - {role.id} -")
        return WebHelpers.EasyResponse(f"Role id {role.id} updated.", 200)
    return WebHelpers.EasyResponse(f"Role with id {id} does not exist.", 404)


@role_bp.delete("/api/role/<int:id>")
def delete_role(id):

    role = Role.query.get(id)

    if role:
        db.session.delete(role)
        db.session.commit()
        logging.warning(f"User id - {current_user.id} - deleted role - {id} -")
        return WebHelpers.EasyResponse(f"Role deleted.", 200)
    return WebHelpers.EasyResponse(f"Role with id {id} does not exist.", 404)
