from cgi import test
from api.models.Users import User

class TestFriends:

    def test_users1(self, db):

        assert db
    
        user = User.query.filter_by(username="ThePerson").first()
        user1 = User.query.filter_by(username="TheCoolPerson").first()

        assert user.username != user1.username
        