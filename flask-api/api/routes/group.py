from api.models.db import db
from api.models.Users import Group, User
from flask_jwt_extended import current_user, jwt_required
from flask import (
    Blueprint,
    request,
    jsonify,
)
from api.services.WebHelpers import WebHelpers

group_bp = Blueprint("group_bp", __name__)

@group_bp.post("/api/group")
@jwt_required()
def create_group():

    name = request.form["name"]
    description = request.form["description"]
    invite_only = request.form["inviteOnly"].capitalize()

    if invite_only == "False":
        invite_only = False
    else:
        invite_only = True
    

    group = Group.query.filter_by(name=name).scalar()
    
    if group is None:
        new_group = Group(
            name=name,
            description=description,
            invite_only=invite_only
        )
        group.make_owner(current_user)

        db.session.add(new_group)
        db.session.commit()

        return WebHelpers.EasyResponse(f'Group {new_group.name} created.', 200)

@group_bp.delete("/api/group/<int:id>")
@jwt_required()
def delete_group(id):

    group = Group.query.get(id)

    if group:
        if group.check_role(current_user) == 'Owner' or 'Admin' in current_user.roles:
            db.session.delete(group)
            db.session.commit()
            return WebHelpers.EasyResponse(f'Group with id {id} deleted.', 200)
        return WebHelpers.EasyResponse(f'You must be the owner of the group to delete it.', 400)
    return WebHelpers.EasyResponse(f'That group does not exist.', 404)

@group_bp.put("/api/group/<int:id>")
@jwt_required()
def edit_group(id):

    group = Group.query.get(id)

    name = request.form['name']
    description = request.form['description']
    invite_only = request.form["inviteOnly"].capitalize()

    if invite_only == "False":
        invite_only = False
    else:
        invite_only = True

    if group:
        if group.check_role(current_user) == 'Owner' or 'Admin' in current_user.roles:
            group.name = name
            group.description = description
            group.invite_only = invite_only
            db.session.commit()
            return WebHelpers.EasyResponse(f'Group with id ({id}) updated', 200)
        return WebHelpers.EasyResponse(f'You must be the owner_id of the group to edit it.', 400)
    return WebHelpers.EasyResponse(f'That group does not exist.', 404)

@group_bp.get("/api/group")
@jwt_required()
def get_all_groups():

    groups = Group.query.all()

    resp = jsonify([x.serialize() for x in groups])
    resp.status_code = 200

    return resp
            
@group_bp.get("/api/group/<int:id>")
@jwt_required()
def get_group(id):

    group = Group.query.get(id)

    resp = jsonify(group.serialize())

    resp.status_code = 200

    return resp

@group_bp.post("/api/group/<int:id>/join")
@jwt_required()
def join_group(id):

    #functionality for users to join groups
    group = Group.query.get(id)
    if group:
            if group.check_role(current_user) == None:
                if group.invite_only == False:
                    current_user.join_group(group)
                    return WebHelpers.EasyResponse(f"You have joined group id ({id})", 200)
                return WebHelpers.EasyResponse(f'Sorry, this group is invite only. Contact the owner_id or a moderator for an invite.', 400)
            return WebHelpers.EasyResponse(f'You are already in this group.', 400)
        
    return WebHelpers.EasyResponse(f'Group with id ({id}) not found.', 404)

@group_bp.delete("/api/group/<int:id>/leave")
@jwt_required()
def leave_group(id):

    #functionality for users to leave groups
    group = Group.query.get(id)

    if group:
        status = group.check_role(current_user)
        if status:
            if status != 'Owner':
                current_user.leave_group(group)
                return WebHelpers.EasyResponse(f"You have left group id ({id})", 200)
            return WebHelpers.EasyResponse(f'You may not leave the group as the owner, transfer the ownership role to another user to leave the group.', 400)
        return WebHelpers.EasyResponse(f'You are not in this group.', 400)
    return WebHelpers.EasyResponse(f'Group with id ({id}) not found.', 404)

@group_bp.put("/api/group/<int:id>/user/<int:userId>/change-role/<string:role>")
@jwt_required()
def change_users_role(id, userId, role):

    group = Group.query.get(id)

    if group:
        current_user_status = group.check_role(current_user)
        if current_user_status:
            if current_user_status == 'Owner':
                user = User.query.get(userId)
                if user:
                    if role == 'Owner':
                        group.make_owner(user, current_user)
                        return WebHelpers.EasyResponse(f'User ({userId}) made owner of group ({id})', 200)
                    elif role == 'Moderator':
                        group.make_moderator(user)
                        return WebHelpers.EasyResponse(f'User ({userId}) made moderator of group ({id})', 200)
                    elif role == 'Kicked':
                        user.leave_group(group)
                        return WebHelpers.EasyResponse(f'User ({userId}) has been removed from the group ({id})', 200)
                    else:
                        return WebHelpers.EasyResponse(f'That role does not exist!', 400)
                return WebHelpers.EasyResponse(f'That user does not exist!', 400)
            return WebHelpers.EasyResponse(f'You must be the owner of the group to change another users role.', 400)
        return WebHelpers.EasyResponse(f'You are not currently in this group.', 400)
    return WebHelpers.EasyResponse(f'The group with that id does not exist.', 400)




