import pytest
import sqlite3
from api.models.Users import User
from api import user_datastore

#Due to DB seeding some default values will already be in database.

class TestDB:

    def test_user(self, db):
        
        assert db

        user = User(first_name="Person",
        last_name="Person1",
        major="Basket Weaving",
        grad_year = "2020",
        username="TheCoolPerson",
        password="password",
        email="person@gmail.com")

        assert user
        db.session.add(user)
        db.session.commit()

        test_user = User.query.filter_by(username="TheCoolPerson").first()

        assert test_user == user

    def test_user1(self, db):
    
        user1 = User(first_name="Person1",
        last_name="Person2",
        major="Basket Weaving",
        grad_year = "2020",
        username="ThePerson",
        password="password",
        email="person1@gmail.com")

        db.session.add(user1)
        db.session.commit()

        assert user1
