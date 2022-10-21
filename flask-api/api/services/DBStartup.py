from api.models.Users import User, Role
from api import user_datastore
from api.models.db import db
import logging
from flask_security.utils import hash_password

def seed_db():
    """Initial seeding of database on application start up."""

    if Role.query.count() == 0:

        admin_role = Role(
            id=1,
            name="Admin",
            description="Role for users that manage an organizations instance of the platform.",
        )
        
        db.session.add(admin_role)
        db.session.commit()
        logging.warning(f"No roles found, default roles created.")

    if User.query.count() == 0:
        password = hash_password("password")
        admin = user_datastore.create_user(
            first_name="ADMIN",
            last_name="ADMIN",
            grad_year="2024",
            major="ADMINISTRATION",
            username="ADMIN",
            email="ADMIN@EMAIL.COM",
            password=password)

        user_datastore.add_role_to_user(admin, "Admin")
        db.session.add(admin)
        db.session.commit()
        logging.warning(
            f"No admin found, default admin account made. Make sure default credentials are changed."
        )

    if User.query.count() == 1:
        password = hash_password("password")
        user1 = user_datastore.create_user(
            first_name="Bob",
            last_name="Smith",
            grad_year="2026",
            major="Basket Weaving",
            username="TheBob",
            email="bob@gmail.com",
            password=password,

        )
        db.session.add(user1)
        db.session.commit()
