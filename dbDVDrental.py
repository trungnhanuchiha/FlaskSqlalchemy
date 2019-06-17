from flask import  Flask

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import TSVECTOR


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/dvdrental'
db = SQLAlchemy(app)

Film_Catergory = db.Table('film_category', db.Column('film_id', db.Integer, db.ForeignKey('film.film_id')),
                          db.Column('category_id', db.Integer, db.ForeignKey('category.category_id')),
                          db.Column('last_update', db.TIMESTAMP))

Film_Actor = db.Table('film_actor', db.Column('film_id', db.Integer, db.ForeignKey('film.film_id')),
                          db.Column('actor_id', db.Integer, db.ForeignKey('actor.actor_id')),
                          db.Column('last_update', db.TIMESTAMP))


class Category(db.Model):
    __tablename__ = 'category'
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    last_update = db.Column(db.TIMESTAMP)

    films = db.relationship('Film', secondary=Film_Catergory, lazy='subquery', backref=db.backref('catergories', lazy=True))

class Film(db.Model):
    __tablename__ = 'film'
    film_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    release_year = db.Column(db.Integer)
    language_id = db.Column(db.Integer, db.ForeignKey('language.language_id'))
    rental_duration = db.Column(db.Integer)
    rental_rate = db.Column(db.Float)
    length = db.Column(db.Integer)
    replacement_cost = db.Column(db.Float)
    rating  = db.Column(db.String)
    last_update = db.Column(db.TIMESTAMP)
    special_features = db.Column(db.ARRAY(db.Integer, dimensions=1))
    fulltext = db.Column(TSVECTOR)

    inventories = db.relationship('Inventory', backref='film', lazy=True)

class Language(db.Model):
    __tablename__ = 'language'
    language_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    last_update = db.Column(db.TIMESTAMP)

    films = db.relationship('Film', backref='language', lazy=True)

class Actor(db.Model):
    __tablename__ = 'actor'
    actor_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    last_update = db.Column(db.TIMESTAMP)

    films = db.relationship('Film', secondary=Film_Actor, lazy='subquery', backref=db.backref('actors', lazy=True))


class Inventory(db.Model):
    __tablename__ = 'inventory'
    inventory_id = db.Column(db.Integer, primary_key=True)
    film_id = db.Column(db.Integer, db.ForeignKey('film.film_id'))
    store_id = db.Column(db.Integer, db.ForeignKey('store.store_id'))
    last_update = db.Column(db.TIMESTAMP)

    rentals = db.relationship('Rental', backref='inventory', lazy=True)

class Rental(db.Model):
    __tablename__ = 'rental'
    rental_id = db.Column(db.Integer, primary_key=True)
    rental_date = db.Column(db.TIMESTAMP)
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.inventory_id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'))
    return_date = db.Column(db.TIMESTAMP)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'))
    last_update = db.Column(db.TIMESTAMP)

    payments = db.relationship('Payment', backref='rental', lazy=True)


class Payment(db.Model):
    __tablename__ = 'payment'
    payment_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'))
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'))
    rental_id = db.Column(db.Integer, db.ForeignKey('rental.rental_id'))
    amount = db.Column(db.Float)
    payment_day = db.Column(db.TIMESTAMP)




class Staff(db.Model):
    __tablename__ = 'staff'
    staff_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    address_id = db.Column(db.Integer, db.ForeignKey('address.address_id'))
    email = db.Column(db.String)
    store_id = db.Column(db.Integer, db.ForeignKey('store.store_id'))
    active = db.Column(db.Boolean)
    username = db.Column(db.String)
    password = db.Column(db.String)
    last_update = db.Column(db.TIMESTAMP)
    picture = db.Column(db.BINARY)

    payments = db.relationship('Payment', backref='staff', lazy=True)
    rentals = db.relationship('Rental', backref='staff', lazy=True)
    stores = db.relationship('Store', backref='manager', lazy=True)


class Customer(db.Model):
    __tablename__ = 'customer'
    customer_id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('store.store_id'))
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    address_id = db.Column(db.Integer, db.ForeignKey('address.address_id'))
    activebool = db.Column(db.Boolean)
    create_date = db.Column(db.TIMESTAMP)
    last_update = db.Column(db.TIMESTAMP)
    active = db.Column(db.Integer)

    rentals = db.relationship('Rental', backref='customer', lazy=True)
    payments = db.relationship('Payment', backref='customer', lazy=True)


class Address(db.Model):
    __tablename__ = 'address'
    address_id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String)
    address2 = db.Column(db.String)
    district = db.Column(db.String)
    city_id = db.Column(db.Integer, db.ForeignKey('city.city_id'))
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    last_update = db.Column(db.TIMESTAMP)

    customers = db.relationship('Customer', backref='address', lazy=True)
    staffs = db.relationship('Staff', backref='address', lazy=True)
    stores = db.relationship('Store', backref='address', lazy=True)


class City(db.Model):
    __tablename__ = 'city'
    city_id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String)
    country_id = db.Column(db.Integer, db.ForeignKey('country.country_id'))
    last_update = db.Column(db.TIMESTAMP)

    addresses = db.relationship('Address', backref='city', lazy=True)


class Country(db.Model):
    country_id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String)
    last_update = db.Column(db.TIMESTAMP)

    cities = db.relationship('City', backref='country', lazy=True)



class Store(db.Model):
    store_id = db.Column(db.Integer, primary_key=True)
    manager_staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'))
    address_id = db.Column(db.Integer, db.ForeignKey('address.address_id'))
    last_update = db.Column(db.TIMESTAMP)




session = db.session()

