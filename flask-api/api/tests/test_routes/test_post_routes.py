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

    # check to make sure a user can get a post
    def test_get_post(self, client, db):
        response = client.get('/api/post')

        assert response.status_code == 200
        
    # check to make sure user can get a specific post
    def test_get_single_post(self, client, db):
        response = client.get('/api/post/<int:id>', 

        data = {
            'id' : 1
        })
        assert response.status_code == 200