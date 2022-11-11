from api.models.Events import Event
from api.models.db import db
from flask import Blueprint, request, jsonify
import logging
from flask_security import current_user, login_required
from api.services.WebHelpers import WebHelpers
import time
from datetime import datetime

event_bp = Blueprint("event_bp", __name__)


@login_required
@event_bp.get("/api/event/<int:id>")
def get_event(id):

    event = Event.query.get(id)

    if event:
        logging.info(f"User id - {current_user.id} - accessed event id - {event.id} -")

        return event.serialize()

    return WebHelpers.EasyResponse(f"Event with id {id} doesnt exist.", 404)


@login_required
@event_bp.get("/api/event")
def get_events():

    event = Event.query.all()

    logging.info(f"User id - {current_user.id} accessed all events.")
    events = jsonify([x.serialize() for x in event])
    resp = events
    resp.status_code = 200
    return resp


@login_required
@event_bp.post("/api/event")
def create_event():

    event_name = request.form["name"]
    event_description = request.form["description"]
    event_time = request.form["time"]

    # ts = ciso8601.parse_datetime(t)

    timestamp = datetime.strptime(event_time, "%m/%d/%Y %H:%M")

    event = Event(
        name=event_name,
        description=event_description,
        time=timestamp,
        owner_id=current_user.id,
    )

    db.session.add(event)
    db.session.commit()
    logging.warning(
        f"User id - {current_user.id} - created new event id - {event.id} -"
    )
    return event.serialize()


@login_required
@event_bp.put("/api/event/<int:id>")
def update_event(id):

    event = Event.query.get(id)

    if event:
        event_name = request.form["name"]
        event_description = request.form["description"]
        event_time = request.form["time"]

        timestamp = datetime.strptime(event_time, "%m/%d/%Y %H:%M")

        event.name = event_name
        event.description = event_description
        event.time = timestamp

        db.session.commit()

        logging.warning(f"User id - {current_user.id} - modified event - {event.id} -")
        return WebHelpers.EasyResponse(f"Event id {event.id} updated.", 200)
    return WebHelpers.EasyResponse(f"Event with id {id} does not exist.", 404)


@login_required
@event_bp.delete("/api/event/<int:id>")
def delete_event(id):

    event = Event.query.get(id)

    if event:
        db.session.delete(event)
        db.session.commit()
        logging.warning(f"User id - {current_user.id} - deleted event - {id} -")
        return WebHelpers.EasyResponse(f"Event deleted.", 200)
    return WebHelpers.EasyResponse(f"Event with id {id} does not exist.", 404)


@login_required
@event_bp.put("/api/event/join/<int:id>")
def join_event(id):

    event = Event.query.get(id)

    if event:
        event.join_event(current_user)
        return WebHelpers.EasyResponse(f"You are now attending {event.name}!", 200)
    return WebHelpers.EasyResponse(f"Event with {id} not found.", 404)


@login_required
@event_bp.put("/api/event/leave/<int:id>")
def leave_event(id):

    event = Event.query.get(id)
    if event:
        event.leave_event(current_user)
        return WebHelpers.EasyResponse(f"You are no longer attending {event.name}", 200)
    return WebHelpers.EasyResponse(f"Event with {id} not found.", 404)
