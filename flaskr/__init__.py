import os
import datetime
from flask import Flask, jsonify, request, abort
from sqlalchemy import event
from models import setup_db, Actor, Movie, Gender
from auth.auth import requires_auth


def create_app(test_config=None):
    app = Flask(__name__)

    # Setup Database
    setup_db(app)

    '''

    Actor Route

    '''

    @app.route('/actors')
    @requires_auth(permission='get:actors')
    def get_actors():
        # Get all actors | if no id provided
        actors = [actor.format() for actor in Actor.query.all()]

        return jsonify({
            'actors': actors,
            'total_actors': len(actors),
            'success': True,
            'status_code': 200,
        })

    @app.route('/actors', methods=['POST'])
    @requires_auth(permission='post:actors')
    def add_actor():
        name = request.get_json()['name']
        age = request.get_json()['age']
        gender = request.get_json()['gender']

        # Check that there is name, age and gender in the request
        if not (name and age and gender) or not (
                isinstance(name, str)
                and isinstance(age, int)
                and isinstance(gender, str)
                ):
            abort(400)

        # Create Actor
        actor = Actor(
            name.strip(),
            age,
        )

        # Gender for actor
        actor_gender = Gender.query.filter_by(
                gender=gender.replace(' ', '').lower()).first()

        # Check if the gender is wrong | Not in database
        if not actor_gender:
            abort(400)

        # Add Gender , Actor relationship
        actor_gender.actors.append(actor)

        # Insert actor to database
        try:
            actor.insert()
            return jsonify({
                'success': True,
                'status_code': 201,
                'actor_id': actor.id,
            })
        except Exception as e:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth(permission='delete:actors')
    def delete_actor(actor_id):
        actor = Actor.query.get_or_404(actor_id)

        try:
            actor.delete()
            return jsonify({
                'success': True,
                'status_code': 200,
                'actor_id': actor.id,
            })
        except Exception as e:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth(permission='patch:actors')
    def update_actor(actor_id):
        actor = Actor.query.get_or_404(actor_id)
        my_request = request.get_json()

        # Check that there is at least one field to change
        if not my_request:
            abort(400)

        # Get the fields | if there is data or make it to default
        name = my_request['name'] if 'name' in my_request else ''
        age = my_request['age'] if 'age' in my_request else 0
        gender = my_request['gender'] if 'gender' in my_request else ''

        # Check that the data type is correct
        if (name and not isinstance(name, str)) or (
                age and not isinstance(age, int)) or (
                gender and not isinstance(gender, str)
                ):
            abort(400)

        # Update Actor data if it is exist | else assign it to the old value
        actor.name = name.strip() if name else actor.name
        actor.age = age if age != 0 else actor.age

        # Check if there is gender
        if gender:
            # Get the new gender | if there is a new one
            actor_gender_new = Gender.query.filter_by(
                gender=gender.replace(' ', '').lower()
                ).first()

            # Check if the gender passed from user is right
            if not actor_gender_new:
                abort(400)

            # Get the old gender
            actor_gender_old = Gender.query.get(actor.gender_id)

            # Check that new Actor gender differrent than the old Actor gender
            if actor_gender_new.gender != actor_gender_old.gender:
                # Add the actor to the new gender
                actor_gender_new.actors.append(actor)

        try:
            actor.update()
            return jsonify({
                'actor': actor.format(),
                'success': True,
                'status_code': 200,
            })
        except Exception as e:
            abort(422)

    '''

    Movie Route

    '''

    # Convert date from Str to Int | Return day, month, year
    def convert_date(release_date):
        day, month, year = tuple(
            [int(date) for date in release_date.split('/')]
            )

        # Check that the date if correct
        if (day < 1 or day > 31) or (
            month < 1 or month > 12) or (
                year > datetime.datetime.now().year):
            abort(400)

        return day, month, year

    @app.route('/movies')
    @requires_auth(permission='get:movies')
    def get_movies():
        movies = [movie.format() for movie in Movie.query.all()]

        return jsonify({
            'movies': movies,
            'total_movies': len(movies),
            'success': True,
            'status_code': 200,
        })

    @app.route('/movies', methods=['POST'])
    @requires_auth(permission='post:movies')
    def add_movie():

        # Check if title and release_date exists
        if ('title' not in request.get_json()) or (
                'release_date' not in request.get_json()):
            abort(400)

        title = request.get_json()['title']
        release_date = request.get_json()['release_date']

        # Check the data type
        if not (isinstance(title, str) and isinstance(release_date, str)):
            abort(400)

        # Convert datetime to datetime object | Global format: d/m/y
        day, month, year = convert_date(release_date)

        # Year, month, day
        try:
            datetime_obj = datetime.datetime(year, month, day)
        except Exception as e:
            abort(400)

        # Create movie object
        movie = Movie(title.strip(), datetime_obj)

        try:
            movie.insert()
            return jsonify({
                'movie_id': movie.id,
                'success': True,
                'status_code': 201
            })
        except Exception as e:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth(permission='delete:movies')
    def delete_movie(movie_id):
        movie = Movie.query.get_or_404(movie_id)

        try:
            movie.delete()
            return jsonify({
                'movie_id': movie.id,
                'success': True,
                'status_code': 200
            })
        except Exception as e:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth(permission='patch:movies')
    def update_movie(movie_id):
        movie = Movie.query.get(movie_id)
        my_request = request.get_json()

        # Check that there is at least one field to change
        if not my_request:
            abort(400)

        # Get the fields | if there is data or make it to default
        title = my_request['title'] if 'title' in my_request else ''
        release_date = my_request['release_date'] if(
            'release_date' in my_request) else ''

        # Check that the data type is correct
        if (title and not isinstance(title, str)) or (
                release_date and not isinstance(release_date, str)
                ):
            abort(400)

        # Update Movie data if it is exist | else assign it to the old value
        movie.title = title.strip() if title else movie.title

        # Check if there is release_date
        if release_date:
            day, month, year = convert_date(release_date)
            # Try to convert date from String to DateObject
            try:
                movie.release_date = datetime.datetime(year, month, day) if(
                    release_date) else movie.release_date
            except Exception as e:
                abort(400)

        try:
            movie.update()
            return jsonify({
                'movie': movie.format(),
                'success': True,
                'status_code': 200,
            })
        except Exception as e:
            abort(422)

    def get_error_msg(status_code, msg):
        return jsonify({
            'message': msg,
            'status_code': status_code,
            'success': False
        })

    @app.errorhandler(400)
    def bad_request(e):
        return (get_error_msg(400, 'Bad Request'), 400)

    @app.errorhandler(404)
    def not_found(e):
        return (get_error_msg(404, 'Not Found'), 404)

    @app.errorhandler(422)
    def unprocessable(e):
        return (get_error_msg(422, 'Cannot be processed'), 422)

    @app.errorhandler(401)
    def unauthorized(e):
        return (get_error_msg(
            401, 'You don\'t have Authorization to access this endpoint'), 401)

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
