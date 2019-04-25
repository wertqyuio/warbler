"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows
from sqlalchemy.exc import InvalidRequestError
from psycopg2 import IntegrityError

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserViewModel(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()
    
        u = {
            "email": "test@test.com",
            "username": "testuser",
            "password": "HASHED_PASSWORD",
            "image_url": "https:kskljlsfkjfk"
        }
        new_user = User.signup(u["username"], u["email"], u["password"],
                               u["image_url"])

        app.config['WTF_CSRF_ENABLED'] = False
        db.session.add(new_user)
        db.session.commit()

        self.client = app.test_client()

    def test_login(self):
        response = self.client.post('/login', data={"username": "testuser",
                                                    "password":
                                                    "HASHED_PASSWORD"})
        print(response)
        self.assertEqual(response.status_code, 302)

    def test_followers(self):
        response = self.client.post('/login', data={"username": "testuser",
                                                    "password":
                                                    "HASHED_PASSWORD"})
    
        user = User.query.filter_by(username="testuser").first()

        response_followers = self.client.get(f'/users/{user.id}/followers')

        self.assertEqual(response_followers.status_code, 200)

    def test_following(self):
        response = self.client.post('/login', data={"username": "testuser",
                                                    "password":
                                                    "HASHED_PASSWORD"})
    
        user = User.query.filter_by(username="testuser").first()

        response_following = self.client.get(f'/users/{user.id}/following')

        self.assertEqual(response_following.status_code, 200)