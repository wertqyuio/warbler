"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

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


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_user_repr(self):
        """Does our __repr__ function work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        self.assertEqual(u.__repr__(),
                         f"<User #{u.id}: {u.username}, {u.email}>")

    def test_user_following(self):
        """Does is following return true when u follows u2"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        u2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.add(u2)
        u.following.append(u2)  # u is following u2

        db.session.commit()

        self.assertEqual(u.is_following(u2), True)  # u IS following u2
        self.assertEqual(u2.is_followed_by(u), True)  # u2 IS followed by u
        self.assertEqual(u.is_followed_by(u2), False)  # u ISN'T followed by u2

    def test_user_not_following(self):
        """Does is following return false when we check if u follows u2,
           when u2 follows u"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        u2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.add(u2)
        u.followers.append(u2)

        db.session.commit()

        self.assertEqual(u.is_following(u2), False)

    def test_new_user(self):
        u = {
            "email": "test@test.com",
            "username": "testuser",
            "password": "HASHED_PASSWORD",
            "image_url": "https:kskljlsfkjfk"
        }
        count = User.query.count()
        new_user = User.signup(u["username"], u["email"], u["password"],
                               u["image_url"])
        db.session.add(new_user)
        db.session.commit()
        new_count = User.query.count()
        self.assertEqual(new_count, count+1)

    def test_fail_user(self):
        u = {
            "email": "test@test.com",
            "username": "testuser",
            "password": "HASHED_PASSWORD",
            "image_url": "https:kskljlsfkjfk"
        }

        u2 = {
            "email": "test2@test.com",
            "username": "testuser",
            "password": "HASHED_PASSWORD",
            "image_url": "https:kskljlsfkjfk"

        }

        new_user = User.signup(u["username"], u["email"], u["password"],
                               u["image_url"])
        db.session.add(new_user)
        db.session.commit()
        count = User.query.count()
        try:
            new_user_two = User.signup(u2["username"], u2["email"],
                                       u2["password"],
                                       u2["image_url"])
            db.session.add(new_user_two)
            db.session.rollback()

        except:
            pass

        db.session.commit()
        new_count = User.query.count()
        self.assertEqual(new_count, count)

    def test_authenticate_user(self):
        u = {
            "email": "test@test.com",
            "username": "testuser",
            "password": "HASHED_PASSWORD",
            "image_url": "https:kskljlsfkjfk"
        }
        new_user = User.signup(u["username"], u["email"], u["password"],
                               u["image_url"])
        db.session.add(new_user)
        db.session.commit()
        test_user = User.authenticate(u["username"], u["password"])
        self.assertEqual(new_user, test_user)

    def test_authenticate_username_fail(self):
        u = {
            "email": "test@test.com",
            "username": "testuser",
            "password": "HASHED_PASSWORD",
            "image_url": "https:kskljlsfkjfk"
        }
        new_user = User.signup(u["username"], u["email"], u["password"],
                               u["image_url"])
        db.session.add(new_user)
        db.session.commit()

        test_user = User.authenticate("test", u["password"])
        self.assertEqual(test_user, False)

    def test_authenticate_password_fail(self):
        u = {
            "email": "test@test.com",
            "username": "testuser",
            "password": "HASHED_PASSWORD",
            "image_url": "https:kskljlsfkjfk"
        }
        new_user = User.signup(u["username"], u["email"], u["password"],
                               u["image_url"])
        db.session.add(new_user)
        db.session.commit()

        test_user = User.authenticate(u["username"], "bad password")
        self.assertEqual(test_user, False)
