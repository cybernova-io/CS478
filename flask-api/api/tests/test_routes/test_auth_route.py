import pytest
import sqlite3
from api.models.Users import User
from api import user_datastore


class TestDB:

    # check to make sure signup works
    def test_signup_user(self, client, db):

        response = client.post(
            "/api/signup",
            data={
                "firstName": "Person",
                "lastName": "Person1",
                "major": "Basket Weaving",
                "gradYear": "2024",
                "username": "TheCoolPerson",
                "password": "password",
                "email": "person@gmail.com",
            },
        )

        assert response.status_code == 201

    # check to make sure user is found
    def test_signup_user_already_exists(self, client, db):
        response = client.post(
            "/api/signup",
            data={
                "firstName": "Person",
                "lastName": "Person1",
                "major": "Basket Weaving",
                "gradYear": "2024",
                "username": "TheCoolPerson",
                "password": "password",
                "email": "person@gmail.com",
            },
        )

        assert response.status_code == 400

    def test_login_user(self, client, db):

        # make sure login works
        response = client.post(
            "/api/login", data={"email": "person@gmail.com", "password": "password"}
        )

        assert response.status_code == 200

        # make sure it recognizes you are already logged in
        response = client.post(
            "/api/login", data={"email": "person@gmail.com", "password": "password"}
        )
        assert response.status_code == 400

        # make sure it recognizes logout
        response = client.get("/api/logout")
        assert response.status_code == 200

        # make sure recognizes invalid email/password combination
        response = client.post(
            "/api/login", data={"email": "person@gmail.com", "password": "password123"}
        )
        assert response.status_code == 405

    def test_friends(self, client, db):

        response = client.get("/api/friends")
        assert response.status_code == 200
