from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """Connect the database to the Flask App
    """

    db.app = app
    db.init_app(app)

# build database schema
class Friends (db.Model):
    """Friends list model"""

    __tablename__ = 'friends'

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        primary_key = True,
    )

    friend_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        primary_key = True,
    )

# Users
class User(db.Model):
    """User Model"""
    
    def __repr__ (self):
        """Clearer Representation String"""
        return f'<User {self.id} : {self.username}, {self.email}>'
    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )
    
    friends = db.relationship(
        'User', 
        secondary='friends',
        primaryjoin=(Friends.user_id == id),
        secondaryjoin = (Friends.friend_id == id)
        )

    favorites = db.relationship(
        'Recipe',
        secondary='favorites'
    )

    def accept_friend(self, friend_id):

        friend = User.query.get(friend_id)
        self.friends.append(friend)
        db.session.commit()

    @classmethod
    def signup(cls, username, email, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            #image_url=image_url,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.
        If it finds such a user, returns that user object.
        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

# Cabinet : User <-> Cabinet/ Ingredients >-- Cabinet

class Cabinet(db.Model):
    """Cabinet model to store ingredients"""

    __tablename__ = 'cabinets'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )

    user = db.relationship('User')

    ### MAKE INGREDIENTS RELATIONSHIP
    ingredients = db.relationship(
        'Ingredient',
        secondary='cabinet_ingredients',
        backref = 'cabinets')

class CabinetIngredient(db.Model):
    """Many to Many table for Ingredients and Cabinets"""

    __tablename__ = 'cabinet_ingredients'

    cabinet_id = db.Column(
        db.Integer,
        db.ForeignKey('cabinets.id', ondelete='CASCADE'),
        nullable = False,
        primary_key=True
    ) 

    ingredient_id = db.Column(
        db.Integer,
        db.ForeignKey('ingredients.id', ondelete='CASCADE'),
        nullable = False,
        primary_key=True
    )

# Ingredients 
class Ingredient(db.Model):
    """Ingredient Model"""

    __tablename__= 'ingredients'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    
    name = db.Column(
        db.String(50),
        nullable=False,
    )


# Friends : Users >--< Users



#Favorites : Users >--< Recipes

class Favorites (db.Model):
    """Favorites model"""

    __tablename__ = 'favorites'

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable = False,
        primary_key = True,
    )

    recipe_id = db.Column(
        db.Integer,
        db.ForeignKey('recipes.id', ondelete='CASCADE'),
        nullable = False,
        primary_key = True,
    )


#Posts : Posts --< User

class Post(db.Model):
    """Post Model"""
    __tablename__ = 'posts'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    content = db.Column(
        db.String(500),
        nullable=False,
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable = False,
    )

    user = db.relationship('User', backref= 'posts')
    

#comments : Comments --< Post / Comments >--- Users

class Comment(db.Model):
    """Comment Model"""
    __tablename__ = 'comments'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    content = db.Column(
        db.String(500),
        nullable=False,
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )

    post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.id', ondelete='CASCADE'),
        nullable = False,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable = False,
    )

    user = db.relationship('User', backref= 'comments')
    post = db.relationship('Post', backref= 'comments')

#recipes 

class Recipe(db.Model):
    """Recipe Model"""

    __tablename__ = 'recipes'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    
    name = db.Column(
        db.String(50),
        nullable=False,
    )

    ingredients = db.relationship(
        'Ingredient',
        secondary= 'recipe_ingredient',
        backref= 'recipes'
    )

class RecipeIngredient(db.Model):
    """Relationship between recipes and ingredients"""

    __tablename__ = 'recipe_ingredient'

    recipe_id = db.Column(
        db.Integer,
        db.ForeignKey('recipes.id', ondelete='CASCADE'),
        nullable = False,
    )

    ingredient_id = db.Column(
        db.Integer,
        db.ForeignKey('ingredients.id', ondelete='CASCADE'),
        nullable = False,
    )