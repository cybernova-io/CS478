import pytest
import sqlite3
from api.models.Posts import Post
from api import user_datastore

class TestDB:

    # check to make sure user can create post
    def test_create_post(self, client, db):
        response = client.post('/api/post/create/', data = {
            'title' : 'My Post Title',
            'content' : 'My Post Content'})

        assert response.status_code == 200


