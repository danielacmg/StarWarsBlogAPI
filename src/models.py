from flask_sqlalchemy import SQLAlchemy
from flask import Flask 

db = SQLAlchemy()


favorite_character = db.Table(
    'favorite_character',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('character_id', db.Integer, db.ForeignKey('character.id'), primary_key=True)  
)

favorite_planet = db.Table('favorite_planet',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('planet_id', db.Integer, db.ForeignKey('planet.id'), primary_key=True)
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    fave_characters = db.relationship('Character', secondary=favorite_character, backref='fave_characters')
    fave_planets = db.relationship('Planet', secondary=favorite_planet, backref='fave_planets')
    
    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # "fave_characters": list(map(lambda character: character.serialize(), self.fave_characters)),
            # "fave_planets": list(map(lambda planet: planet.serialize(), self.fave_planets))
            "fave_characters": list(map(lambda character: character.name, self.fave_characters)),
            "fave_planets": list(map(lambda planet: planet.name, self.fave_planets))
        }

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    mass = db.Column(db.String(50), nullable=False)
    hair_color = db.Column(db.String(50), nullable=False)
    skin_color = db.Column(db.String(50), nullable=False)
    eye_color = db.Column(db.String(50), nullable=False)
    birth_year= db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    # homeworld = db.Column(db.String(50), nullable=False)
    # specie = db.Column(db.String(50), nullable=False)
    # vehicle = db.Column(db.String(50), nullable=False)
    # starship = db.Column(db.String(50), nullable=False)
    # film = db.Column(db.String(150), nullable=False)
    
    def __repr__(self):
        return self.name
    
    def serialize(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color" :self.hair_color,
            "skin_color" :self.skin_color,
            "eye_color" :self.eye_color,
            "birth_year":self.birth_year,
            "gender" :self.gender,
            # "homeworld" :self.homeworld,
            # "specie" :self.specie,
            # "vehicle" :self.vehicle,
            # "starship" :self.starship,
            # "film" :self.film
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    rotation_period = db.Column(db.String(250), nullable=False)
    orbital_period = db.Column(db.String(250), nullable=False)
    diameter = db.Column(db.Integer, nullable=False)
    climate = db.Column(db.String(250), nullable=False)
    gravity = db.Column(db.String(250), nullable=False)
    terrain = db.Column(db.String(250), nullable=False)
    surface_water = db.Column(db.String(250), nullable=False)
    population = db.Column(db.String(250), nullable=False) #db.Column(db.Integer, nullable=False)
    # residents = relationship("character", back_populates="character_id")
    # film = relationship("film", back_populates="vehicle_id")
    # created = db.Column(db.String(50), nullable=False)
    # edited = db.Column(db.String(50), nullable=False) 

    def __repr__(self):
        return self.name
    
    def serialize(self):
        return {
            "id" : self.id,
            "name" :self.name,
            "rotation_period" :self.rotation_period,
            "orbital_period" :self.orbital_period,
            "diameter" : self.diameter,
            "climate" :self.climate,
            "gravity" :self.gravity,
            "terrain" :self.terrain,
            "surface_water" :self.surface_water,
            "population" :self.population,
            # "residents" :self.residents,
            # "film" :self.film,
            # "created" :self.created,
            # "edited" :self.edited
        }