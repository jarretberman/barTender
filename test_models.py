"""Model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Ingredient, CabinetIngredient, Cabinet, Recipe, Friends, Favorites, Comment, Post

os.environ['DATABASE_URL'] = "postgresql:///bartender_test"

from app import app

db.drop_all()
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

    # def tearDown(self):
    #     """ clear tables"""
        

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no posts
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

        #User should have no messages & no posts
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

    def test_friends (self) : 
        """Adding a friend should show up in the User model"""

        u = User.signup(
            username='testuser',
            email='test@test.com',
            password= 'testtest',
            
        )

        u2 = User.signup(
            username='testuser2',
            email='test2@test.com',
            password= 'testtest',
            
        )

        db.session.add(u)
        db.session.add(u2)
        db.session.commit()

        u.friends.append(u2)

        db.session.commit
        friend = Friends.query.first()

        self.assertEqual(u2, u.friends[0])
        self.assertEqual(u2.id, friend.friend_id)

        u2.accept_friend(u.id)
        friend2 = Friends.query.filter(Friends.user_id == u2.id)

        self.assertEqual(u2.friends[0], u)
        
class PostModelTestCase (TestCase):
    """Tests the Post model"""

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

        self.u = User.signup(
            username='testuser',
            email='test@test.com',
            password= 'testtest',
            
        )
        db.session.add(self.u)
        db.session.commit()

    def test_post_model (self):
        """Post model is attributed to a User properly"""
    
        post = Post(user_id = self.u.id, content = 'my first post')
        db.session.add(post)
        db.session.commit()

        self.assertTrue(post.id)
        self.assertTrue(len(post.comments) == 0)
        self.assertEqual(self.u.posts[0], post)
        self.assertTrue(post.timestamp)

class CommentModelTestCase (TestCase):
    """Tests the Comment model"""

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

        self.u = User.signup(
            username='testuser',
            email='test@test.com',
            password= 'testtest',
            
        )
        db.session.add(self.u)
        db.session.commit()

        self.post = Post(user_id = self.u.id, content = 'my first post')
        db.session.add(self.post)
        db.session.commit()

    def test_comment_model(self):
        """Comment model relationships between User and Post should function properly"""

        comment = Comment(
            user_id = self.u.id, 
            post_id = self.post.id,
            content = 'my first comment')

        db.session.add(comment)
        db.session.commit()

        self.assertEqual(self.u.comments[0], comment)
        self.assertEqual(self.post.comments[0], comment)
        self.assertEqual(comment.user, self.u)
        self.assertEqual(comment.post, self.post)
        self.assertTrue(comment.timestamp)

class CabinetModelTestCase (TestCase):
    """Tests the Cabinet model"""

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

        self.u = User.signup(
            username='testuser',
            email='test@test.com',
            password= 'testtest',
            
        )
        db.session.add(self.u)
        db.session.commit()
    
    def test_cabinet(self):
        """Cabinet Model initialization"""

        cab = Cabinet(user_id = self.u.id)
        db.session.add(cab)
        db.session.commit()

        self.assertEqual(len(cab.ingredients), 0)

class IngredientModelTestCase (TestCase):
    """Tests the Ingredient model"""

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

        self.u = User.signup(
            username='testuser',
            email='test@test.com',
            password= 'testtest',
            
        )
        db.session.add(self.u)
        db.session.commit()

        self.cab = Cabinet(user_id = self.u.id)
        db.session.add(self.cab)
        db.session.commit()

    def test_ingredient(self):
        """ingredient Model initialization"""

        ing = Ingredient(name = 'ingredient')
        db.session.add(ing)
        db.session.commit()

        self.assertEqual(len(ing.cabinets), 0)

    def test_cabinet_relationship(self):
        """test through relationship with Ingredient and Cabinet"""
        
        ing = Ingredient(name = 'ingredient')
        self.cab.ingredients.append(ing)
        db.session.commit()

        self.assertEqual(ing.cabinets[0], self.cab)


class RecipeModelTestCase (TestCase):
    """Tests the Recipe model"""

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

    def test_recipe(self):
        """recipe Model initialization"""

        rec = Recipe(name = 'Recipe')
        db.session.add(rec)
        db.session.commit()

        self.assertTrue(rec.id > 0)

class FavoritesModelTestCase (TestCase):
    """Tests the Favorites model"""

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

        self.u = User.signup(
            username='testuser',
            email='test@test.com',
            password= 'testtest',
            
        )
        db.session.add(self.u)
        db.session.commit()

        self.rec = Recipe(name = 'Recipe')
        db.session.add(self.rec)
        db.session.commit()

    def test_favorites_model(self):
        """Tests favorites model and the relationship between User and Recipes"""

        fav = Favorites(user_id = self.u.id, recipe_id = self.rec.id)
        db.session.add(fav)
        db.session.commit()

        self.assertEqual(self.u.favorites[0], self.rec)