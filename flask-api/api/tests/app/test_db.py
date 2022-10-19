import pytest
import sqlite3
from api.models.Users import User


class TestDB:
    def test_db_entry(self, session):
        
        assert session

        user = User(first_name="bob",
        last_name="smith",
        major="Basket Weaving",
        grad_year = "2020",
        email="bob@gmail.com")

        assert user
        session.add(user)
        session.commit()

        test_user = User.query.get(1)

        assert test_user