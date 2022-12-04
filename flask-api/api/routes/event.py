from api.models.Events import Event
from api.models.Users import User
from api.models.db import db
from flask import Blueprint, request, jsonify, render_template, redirect, abort
import logging
from flask_jwt_extended import current_user, jwt_required
from api.services.WebHelpers import WebHelpers
import time
from datetime import datetime
from api.forms.EventForm import EventForm

event_bp = Blueprint("event_bp", __name__)



@event_bp.get("/event")
@jwt_required()
def get_events_page():

    events = Event.query.all()
    data = [x.serialize() for x in events]
    return render_template("/events/events.html", events=data)

@event_bp.get("/event/me")
@jwt_required()
def get_my_events_page():

    events = Event.query.all()

    my_events = []
    #could be list comprehension
    for event in events:
        if event.owner_id == current_user.id or current_user in event.attendees:
            my_events.append(event)
    data = [x.serialize() for x in my_events]

    return render_template("/events/events-me.html", events=data)


@event_bp.get("/event/<int:id>")
@jwt_required()
def get_event_page(id):

    event : Event
    event = Event.query.get(id)
    data = {}
    user = User.query.get(event.owner_id)
    data['event'] = event.serialize()

    data['user'] = user.serialize()

    return render_template("/events/single-event.html", event=data)

@event_bp.route("/event/create", methods = ['GET', 'POST'])
@jwt_required()
def create_event_page():

    if request.method == 'GET':
        form = EventForm()
        return render_template('/events/create-event.html', form=form)

    if request.method == 'POST':
        event_name = request.form["name"]
        event_description = request.form["description"]
        event_time = request.form["date"] + " " + request.form["time"]
        #"02/15/2023 5:00"
        # ts = ciso8601.parse_datetime(t)

        timestamp = datetime.strptime(event_time, "%Y-%m-%d %H:%M")

        event = Event(
            name=event_name,
            description=event_description,
            time=timestamp,
            owner_id=current_user.id,
        )

        db.session.add(event)
        db.session.commit()
        return redirect(f'/event/{event.id}')

@event_bp.post("/event/join/<int:id>")
@jwt_required()
def join_event_page(id):

    event = Event.query.get(id)

    if event:
        event.join_event(current_user)
        return redirect(f'/event/{id}')
    abort(404)

@event_bp.post("/event/leave/<int:id>")
@jwt_required()
def leave_event_page(id):

    event = Event.query.get(id)
    if event:
        event.leave_event(current_user)
        return redirect(f'/event/{id}')
    abort(404)

@event_bp.post("/event/delete/<int:id>")
@jwt_required()
def delete_event_page(id):

    event = Event.query.get(id)

    if event:
        if current_user.id == event.owner_id or current_user.is_admin(): 
            db.session.delete(event)
            db.session.commit()
            return redirect("/event")
        abort(400, "You must be the creator of this event to delete it.")
    abort(404)

@event_bp.route("/event/edit/<int:id>", methods = ['GET', 'POST'])
@jwt_required()
def update_event_page(id):

    if request.method == 'GET':
        event = Event.query.get(id)
        return render_template("/events/edit-event.html", event=event)

    if request.method == 'POST':
        event = Event.query.get(id)
        if event and current_user.id == event.owner_id:
            event_name = request.form["name"]
            event_description = request.form["description"]
            event_time = request.form["date"] + " " + request.form["time"]
            #"02/15/2023 5:00"
            # ts = ciso8601.parse_datetime(t)

            timestamp = datetime.strptime(event_time, "%Y-%m-%d %H:%M")

            event.name = event_name
            event.description = event_description
            event.time = timestamp

            db.session.commit()

            return redirect(f'/event/{event.id}')
        abort(404)

@event_bp.get("/event/user/<int:id>")
@jwt_required()
def get_events_page_profile(id):

    user = User.query.get_or_404(id)
    events = Event.query.all()

    my_events = []
    #could be list comprehension
    for event in events:
        if event.owner_id == user.id or user in event.attendees:
            my_events.append(event)

    return render_template("/events/events-not-me.html", events=my_events, user=user)


######################################################### API BELOW, SERVER RENDERING ABOVE
@event_bp.get("/api/event/<int:id>")
@jwt_required()
def get_event(id):

    event = Event.query.get(id)

    if event:
        logging.info(f"User id - {current_user.id} - accessed event id - {event.id} -")

        return event.serialize()

    return WebHelpers.EasyResponse(f"Event with id {id} doesnt exist.", 404)


@event_bp.get("/api/event")
@jwt_required()
def get_events():

    event = Event.query.all()

    logging.info(f"User id - {current_user.id} accessed all events.")
    events = jsonify([x.serialize() for x in event])
    resp = events
    resp.status_code = 200
    return resp


@event_bp.post("/api/event")
@jwt_required()
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


@event_bp.put("/api/event/<int:id>")
@jwt_required()
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


@event_bp.delete("/api/event/<int:id>")
@jwt_required()
def delete_event(id):

    event = Event.query.get(id)

    if event:
        db.session.delete(event)
        db.session.commit()
        logging.warning(f"User id - {current_user.id} - deleted event - {id} -")
        return WebHelpers.EasyResponse(f"Event deleted.", 200)
    return WebHelpers.EasyResponse(f"Event with id {id} does not exist.", 404)


@event_bp.put("/api/event/join/<int:id>")
@jwt_required()
def join_event(id):

    event = Event.query.get(id)

    if event:
        event.join_event(current_user)
        return WebHelpers.EasyResponse(f"You are now attending {event.name}!", 200)
    return WebHelpers.EasyResponse(f"Event with {id} not found.", 404)


@event_bp.put("/api/event/leave/<int:id>")
@jwt_required()
def leave_event(id):

    event = Event.query.get(id)
    if event:
        event.leave_event(current_user)
        return WebHelpers.EasyResponse(f"You are no longer attending {event.name}", 200)
    return WebHelpers.EasyResponse(f"Event with {id} not found.", 404)
