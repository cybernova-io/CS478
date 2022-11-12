from api.models.db import db
from flask import Blueprint, request, jsonify
import logging
from api.models.Users import User
from flask_jwt_extended import current_user, jwt_required
from api.services.WebHelpers import WebHelpers
import time
from datetime import datetime

blocked_bp = Blueprint("blocked_bp", __name__)


@blocked_bp.get("/api/user/blocked")
@jwt_required()
def blocked_users():

    blocked_users = current_user.blocked_users

    resp = jsonify([x.serialize() for x in blocked_users])

    resp.status_code = 200

    return resp


@blocked_bp.post("/api/user/blocked/<int:id>")
@jwt_required()
def block_user(id):

    user = User.query.get(id)

    if user:
        current_user.add_blocked_user(user)

        return WebHelpers.EasyResponse(
            f"{user.first_name} has been added to your blocked user list.", 200
        )
    return WebHelpers.EasyResponse(f"User with that id does not exist.")


@blocked_bp.delete("/api/user/blocked/<int:id>")
@jwt_required()
def unblock_user(id):

    user = User.query.get(id)

    if user:
        current_user.remove_blocked_user(user)

        return WebHelpers.EasyResponse(
            f"{user.first_name} has been removed from your block list", 200
        )
    return WebHelpers.EasyResponse(f"User with that id does not exist.")
