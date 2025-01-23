from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


#Admin, Customer, sp, booking, service

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String, unique=True)

class sp(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True)
    address = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    experience = db.Column(db.Integer)
    phone = db.Column(db.String)
    city = db.Column(db.String)
    status = db.Column(db.String)
    incoming_booking = db.relationship("Booking", backref = "prof")
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))



class User(db.Model):
    __tablename__ = "customer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True)
    address = db.Column(db.String)
    city = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    phone = db.Column(db.String)
    status=db.Column(db.String)
    sent_booking = db.relationship("Booking", backref="customer")


class Booking(db.Model):
    __tablename__ = "booking"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.String)
    time = db.Column(db.String)
    address = db.Column(db.String)
    status = db.Column(db.String)
    rating = db.Column(db.Integer)
    ratingmessage=db.Column(db.String)
    remark=db.Column(db.String)
    professional_id = db.Column(db.Integer, db.ForeignKey("sp.id"), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)

class ServiceCategory(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True)
    base_price = db.Column(db.Integer)
    professionals = db.relationship("sp",backref = "category")



