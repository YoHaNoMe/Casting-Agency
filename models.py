import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from flask_migrate import Migrate
from dotenv import load_dotenv, set_key

# Load Environments
load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
dev_database_name = os.getenv("DATABASE_NAME")


def setup_db(app, path=''):
    database_path = 'postgres:///{}'.format(dev_database_name)
    app.config['SQLALCHEMY_DATABASE_URI'] = path if path else database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    migrate.init_app(app, db)
    db.create_all()
    # For development Database
    if not int(os.getenv("GENDER_CREATED", 0)):
        try:
            Gender(gender='male').insert()
            Gender(gender='female').insert()
        except Exception as e:
            print(e)
        set_key('.env', "GENDER_CREATED", "1")

    # For Test Database
    if not int(os.getenv("TEST_GENDER_CREATED", 0)) and path:
        try:
            Gender(gender='male').insert()
            Gender(gender='female').insert()
        except Exception as e:
            print(e)
        set_key('.env', "TEST_GENDER_CREATED", "1")


# Casting table | Movie => Casting <= Actor
casting = db.Table(
    'casting',
    db.Column(
        'movie_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True),
    db.Column(
        'actor_id', db.Integer, db.ForeignKey('actors.id'), primary_key=True)
)


# Movie
class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, unique=True)
    release_date = db.Column(db.DateTime, nullable=False)
    actors = db.relationship(
        'Actor',
        secondary="casting",
        # lazy=True,
        # backref=db.backref('movies', lazy=True)
    )

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def insert_actors(self, actors):
        self.actors.extend(actors)
        db.session.commit()

    def update(self):
        db.session.commit()

    def update_actors(self, actors):
        self.actors.clear()
        self.actors.extend(actors)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date.strftime("%d/%m/%Y"),
            'actors': [actor.name for actor in self.actors]
        }


# Actor
class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    age = db.Column(db.Integer, nullable=False)
    gender_id = db.Column(
        db.Integer, db.ForeignKey('gender.id'), nullable=False)
    movies = db.relationship(
        "Movie",
        secondary="casting"
    )

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender.gender,
            'movies': [movie.title for movie in self.movies]
        }


class Gender(db.Model):
    __tablename__ = 'gender'

    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String, unique=True, nullable=False)
    actors = db.relationship('Actor', backref='gender', lazy=True)

    def __init__(self, gender):
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
