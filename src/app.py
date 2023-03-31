"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, favorite_character, favorite_planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

##################### Users #####################################
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    all_users= list(map(lambda user: user.serialize(), users))
    return jsonify(all_users), 200

    # response_body = {
    #     "msg": "Hello, this is your GET /user response "
    # }
    # return jsonify(response_body), 200

@app.route('/users', methods=['POST'])
def create_user():
    # First we get the payload json
    body = request.get_json()    
     
    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)
    if 'password' not in body:
        raise APIException('You need to specify the password', status_code=400)
    if 'email' not in body:
        raise APIException('You need to specify the email', status_code=400)

    # to inster the user into the bd
    new_user = User(password=body['password'], email=body['email'], is_active=True)
    db.session.add(new_user)
    db.session.commit()
    return "User created", 200

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        raise APIException('User not found', status_code=404)
    db.session.delete(user)
    db.session.commit()
    return "User deleted", 200


##################### Star War's Characters #####################################
@app.route('/people', methods=['POST'])
def create_people():
    # First we get the payload json
    body = request.get_json()  
    
    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)
    if 'name' not in body:
        raise APIException('You need to specify the name', status_code=400)
    if 'height' not in body:
        raise APIException('You need to specify the height', status_code=400)
    if 'mass' not in body:
        raise APIException('You need to specify the mass', status_code=400)
    if 'hair_color' not in body:
        raise APIException('You need to specify the hair_color', status_code=400)
    if 'skin_color' not in body:
        raise APIException('You need to specify the skin_color', status_code=400)
    if 'eye_color' not in body:
        raise APIException('You need to specify the eye_color', status_code=400)
    if 'birth_year' not in body:
        raise APIException('You need to specify the birth_year', status_code=400)
    # if 'homeworld' not in body:
    #     raise APIException('You need to specify the homeworld', status_code=400)
    # if 'specie' not in body:
    #     raise APIException('You need to specify the specie', status_code=400)
    # if 'vehicle' not in body:
    #     raise APIException('You need to specify the vehicle', status_code=400)
    # if 'starship' not in body:
    #     raise APIException('You need to specify the starship', status_code=400)

    # to inster the character into the bd
    # new_character = Character(name=body['name'], height=body['height'], hair_color=body['hair_color'], skin_color=body['skin_color'], eye_color=body['eye_color'], birth_year=body['birth_year'], gender=body['gender'], homeworld=body['homeworld'], specie=body['specie'], vehicle=body['vehicle'], starship=body['starship'])
    new_character = Character(name=body['name'], height=body['height'], hair_color=body['hair_color'], skin_color=body['skin_color'], eye_color=body['eye_color'], birth_year=body['birth_year'], gender=body['gender'], mass=body['mass'])
    db.session.add(new_character)
    db.session.commit()
    return "Character created", 200

@app.route('/people', methods=['GET'])
def get_people():
    if request.method == 'GET':
        character_list = Character.query.all()
        all_characters= list(map(lambda character: character.serialize(), character_list))
        return jsonify(all_characters), 200

    return "Invalid Method", 404

@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_by_id(people_id):
    if request.method == 'GET':
        character = Character.query.get(people_id)
        return jsonify(character.serialize()), 200        

    return "Invalid Method", 404

##################### Star War's Planets #####################################
@app.route('/planet', methods=['POST'])
def create_planet():
    # First we get the payload json
    body = request.get_json()  
    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)
    if 'name' not in body:
        raise APIException('You need to specify the name', status_code=400)
    if 'rotation_period' not in body:
        raise APIException('You need to specify the rotation period', status_code=400)
    if 'orbital_period' not in body:
        raise APIException('You need to specify the orbital period', status_code=400)
    if 'diameter' not in body:
        raise APIException('You need to specify the diameter', status_code=400)
    if 'climate' not in body:
        raise APIException('You need to specify the climate', status_code=400)
    if 'gravity' not in body:
        raise APIException('You need to specify the gravity', status_code=400)
    if 'terrain' not in body:
        raise APIException('You need to specify the terrain', status_code=400)
    if 'surface_water' not in body:
        raise APIException('You need to specify the surface water', status_code=400)
    if 'population' not in body:
        raise APIException('You need to specify the population', status_code=400)
    
    new_planet = Planet(name=body['name'], rotation_period=body['rotation_period'], orbital_period=body['orbital_period'], diameter=body['diameter'], climate=body['climate'], gravity=body['gravity'], terrain=body['terrain'], surface_water=body['surface_water'], population=body['population'])
    db.session.add(new_planet)
    db.session.commit()
    return "Planet created", 200

@app.route('/planet', methods=['GET'])
def get_planet():
    if request.method == 'GET':
        planet_list = Planet.query.all()
        all_planets= list(map(lambda planet: planet.serialize(), planet_list))
        return jsonify(all_planets), 200

    return "Invalid Method", 404

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet_by_id(planet_id):
    if request.method == 'GET':
        planet = Planet.query.get(planet_id)
        return jsonify(planet.serialize()), 200        

    return "Invalid Method", 404

##################### Favorites #####################################
@app.route('/favorites/<int:user_id>', methods=['GET'])
def get_favorites(user_id):
    if request.method == 'GET':
        user = User.query.get(user_id)
        # u_mail=str(user.email)
        if len(user.fave_characters)==0:
            msje="No favorite characters yet "
        else:
            msje=" Favorite People: "+str(user.fave_characters)
    
        if len(user.fave_planets)==0:
            msje +=" No favorite planets yet"
        else: 
            msje +=" Favorite Planets: "+ str(user.fave_planets)
        
        # response_body = (
        #     #"user: "+ u_mail + 
        #     " FavoritePeople: "+u_fav_char+" FavoritePlanets: "+u_fav_plan)
        # return jsonify(response_body), 200
        return jsonify(msje), 200
    return "Invalid Method", 404
    
    
@app.route('/favorite/<int:user_id>/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(user_id, planet_id):
    user = User.query.get(user_id)

    if user is None:
        raise APIException('User not found', status_code=404)
    else:       
        planet = Planet.query.get(planet_id)
        faves = user.fave_planets        
        
        if planet in user.fave_planets:
            return "The planet is already in user's favorites. Plese choose another one"
        
        user.fave_planets.append(planet)
        db.session.commit()
        
        return "Planet added to favorites", 200    
    
@app.route('/favorite/<int:user_id>/people/<int:character_id>', methods=['POST'])
def add_favorite_people(user_id, character_id):
    user = User.query.get(user_id)

    if user is None:
        raise APIException('User not found', status_code=404)
    else:       
        character = Character.query.get(character_id)
        # faves = user.fave_characters        
        
        if character in user.fave_characters:
            return "The Character is already in user's favorites. Plese choose another one"
        
        user.fave_characters.append(character)
        db.session.commit()
        
        return "Character added to favorites", 200      
    
@app.route('/favorite/<int:user_id>/planet/<int:character_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, character_id):    
    user = User.query.get(user_id)
    if user is None:
        raise APIException('User not found', status_code=404)
    planet = Planet.query.get(planet_id)
    if planet in user.fave_planets:
        user.fave_planets.remove(planet)
        db.session.commit()     
        return "Planet deleted from favorites", 200 
    else:
        return "Planet not found in user's favorites. Please verify id"
            
@app.route('/favorite/<int:user_id>/people/<int:character_id>', methods=['DELETE'])
def delete_favorite_people(user_id, character_id):    
    user = User.query.get(user_id)
    if user is None:
        raise APIException('User not found', status_code=404)
    character = Character.query.get(character_id)
    if character in user.fave_characters:
        user.fave_characters.remove(character)        
        db.session.commit()     
        return "Character deleted from favorites", 200 
    else:
        return "Character not found in user's favorites. Please verify id"
        
    
###################################################

    
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
