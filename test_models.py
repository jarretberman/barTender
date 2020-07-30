"""Model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Ingredient, CabinetIngredient, Cabinet, Recipe, Friends, Favorites, Comment, Post

os.environ['DATABASE_URL'] = "postgresql:///bartender_test"

from app import app

db.create_all()


class UserModelTestCase(TestCase):
    """Testing User Model"""

    def setUp(self):
        """create test client, and add sample data"""
        
        User.query.delete()
        Cabinet.query.delete()
        Recipe.query.delete()
        Friends.query.delete()
        Favorites.query.delete()
        Comment.query.delete()
        Post.query.delete()
        Ingredient.query.delete()
        db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        """ clear tables"""
        

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
        self.assertEqual(len(u.friends), 0)
        self.assertEqual(len(u.posts), 0)

    def test_signup_user(self):
        """Does signup class method work?"""

        u = User.signup(
            username='testuser',
            email='test@test.com',
            password= 'testtest',
        )

        db.session.add(u)
        db.session.commit()

        #User should have no messages & no followers
        self.assertEqual(len(u.friends), 0)
        self.assertEqual(len(u.posts), 0)
        #User password should be encrypted and not stored as entered password
        self.assertNotEqual('testtest', u.password)

    def test_authenicate_user(self):
        """Does authenticate class method work"""

        u = User.signup(
            username='testuser',
            email='test@test.com',
            password= 'testtest',
            
        )

        db.session.add(u)
        db.session.commit()

        #Properly authenticates when password is correct
        self.assertEqual(u, User.authenticate(username='testuser',password='testtest'))
        #Returns false if it can't authenticate
        self.assertFalse(User.authenticate(username='testuser',password='wrongpassword'))


