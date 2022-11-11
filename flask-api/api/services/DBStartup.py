from api.models.Users import User, Role
from api.models.Posts import Post, PostLike, PostComment
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
            password=password,
        )

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

    if User.query.count() == 2:
        password = hash_password("password")
        user2 = user_datastore.create_user(
            first_name="John",
            last_name="Second",
            grad_year="2027",
            major="Economics",
            username="Coolguyjohn",
            email="john@email.com",
            password=password,
        )
        db.session.add(user2)
        db.session.commit()

        add = user1.add_friend(user2)
        db.session.add(add)
        db.session.commit()

        add1 = user2.add_friend(user1)
        db.session.add(add1)
        db.session.commit()

        add = user2.add_pending_friend(user1)
        add1 = user1.add_pending_friend(user2)
        db.session.add(add)
        db.session.add(add1)
        db.session.commit()

    if Post.query.count() == 0:
        post = Post(
            title="Just signed up",
            content="Just signed up this app is so cool",
            user_id=user2.id,
        )

        db.session.add(post)
        db.session.commit()

    if PostLike.query.count() == 0:
        post_like = PostLike(post_id=post.id, user_id=user1.id)
        db.session.add(post_like)
        db.session.commit()

    if PostComment.query.count() == 0:
        post_comment = PostComment(
            post_id=post.id,
            user_id=user1.id,
            text="Yeah its really cool, i wish i could donate them money",
        )
        db.session.add(post_comment)
        db.session.commit()
