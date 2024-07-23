import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import setup_db, Actor, Movie
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

# ROUTES
'''
@TODO implement endpoint
    GET /actor
        get all the details about all actors
'''
@app.route('/actors', methods=['GET'])
@requires_auth('get:actor')
def get_actors():
    try:
        return jsonify({
            'success': True,
            'drinks': [actor.__repr__() for actor in Actor.query.all()]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': "An error occurred"
        }), 500


'''
@TODO implement endpoint
    GET /actor
        get all the details about all movies
'''
@app.route('/movies', methods=['GET'])
@requires_auth('get:movie')
def get_movies():
    try:
        return jsonify({
            'success': True,
            'drinks': [movie.__repr__() for movie in Movie.query.all()]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': "An error occurred"
        }), 500


'''
@TODO implement endpoint
    DELETE /actors
        delete an actor from the database
'''
@app.route('/actors', methods=['DELETE'])
@requires_auth('delete:actor')
def delete_actor(id):
    try:
        actor = Actor.query.filter(Actor.id == id).first()
        if actor is not None:
            actor.delete()
            return jsonify({
                'success': True,
                'drink': id
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Actor not found to be deleted'
            }), 404
    except:
        return jsonify({
            'success': False,
            'error': "An error occurred"
        }), 500
    
'''
@TODO implement endpoint
    DELETE /movies
        delete a movie from the database
'''
@app.route('/movies', methods=['DELETE'])
@requires_auth('delete:movie')
def delete_movie(id):
    try:
        movie = Movie.query.filter(Movie.id == id).first()
        if movie is not None:
            movie.delete()
            return jsonify({
                'success': True,
                'drink': id
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Movie not found to be deleted'
            }), 404
    except:
        return jsonify({
            'success': False,
            'error': "An error occurred"
        }), 500


'''
@TODO implement endpoint
    POST /actors
        create a new actor in the database
'''
@app.route('/actors', methods=['POST'])
@requires_auth('post:actor')
def create_actor(id):
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')
    gender = data.get('gender')

    actor = Actor(name=name, age=age, gender=gender)
    try:
        actor.insert()
        return jsonify({
            'success': True,
            'id': actor.id
        }), 200
    except:
        return jsonify({
            'success': False,
            'error': "An error occurred"
        }), 500
    
'''
@TODO implement endpoint
    POST /movies
        create a new movie in the database
'''
@app.route('/movies', methods=['POST'])
@requires_auth('post:movie')
def create_movie(id):
    data = request.get_json()
    title = data.get('title')
    release_date = data.get('release_date')

    movie = Movie(title=title, release_date=release_date)
    try:
        movie.insert()
        return jsonify({
            'success': True,
            'id': movie.id
        }), 200
    except:
        return jsonify({
            'success': False,
            'error': "An error occurred"
        }), 500
    

'''
@TODO implement endpoint
    PATCH /actors
        edit a existing actor in the database
'''
@app.route('/actors', methods=['PATCH'])
@requires_auth('patch:actor')
def edit_actor(id):
    try:
        data = request.get_json()
        actor = Actor.query.filter(Actor.id == id).one_or_none()
        if actor:
            actor.name = data.get('name')
            actor.age = data.get('age')
            actor.gender = data.get('gender')
            actor.update()

            return jsonify({
                'success': True,
                'id': id
            }), 200

        else:
            return jsonify({
                'success': False,
                'error': 'Actor not found to be edited'
            }), 404
    except:
        return jsonify({
            'success': False,
            'error': "An error occurred"
        }), 500
    
'''
@TODO implement endpoint
    PATCH /movies
        edit a existing movie in the database
'''
@app.route('/movies', methods=['PATCH'])
@requires_auth('patch:movie')
def edit_movie(id):
    try:
        data = request.get_json()
        movie = Movie.query.filter(Movie.id == id).one_or_none()
        if movie:
            movie.title = data.get('title')
            movie.release_date = data.get('release_date')
            movie.update()

            return jsonify({
                'success': True,
                'id': id
            }), 200

        else:
            return jsonify({
                'success': False,
                'error': 'Movie not found to be edited'
            }), 404
    except:
        return jsonify({
            'success': False,
            'error': "An error occurred"
        }), 500



# Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''
@app.errorhandler(404)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resourse not found"
    }), 404

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(AuthError)
def auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response
