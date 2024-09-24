from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime
from sqlalchemy import Enum

# Initialize Flask app
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rental_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy()


# Define Property model
class Property(db.Model):
    __tablename__ = 'properties'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    rent = db.Column(db.Numeric(10, 2), nullable=False)
    renter_id = db.Column(db.Integer, db.ForeignKey('renter.id'), unique=True)   
    amenities = db.Column(db.Text)
    photo_path = db.Column(db.String(255))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Relationships
    renter = db.relationship('Renter', back_populates='property', uselist=False)
    payment = db.relationship('RentPayment', backref='property', lazy=True)

class RentPayment(db.Model):
    __tablename__ = 'rent_payments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'))
    renter_id = db.Column(db.Integer, db.ForeignKey('renter.id'))
    amount_paid = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.Date, default=datetime.utcnow)
    payment_status = db.Column(db.String(50), default='Pending')  # Could be 'Paid', 'Late', 'Pending'
    
    def __repr__(self):
        return f"<RentPayment {self.amount_paid} for Property {self.property_id}>"

# Define Tenant model
class Renter(db.Model):
    __tablename__ = 'renter'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    property_id = db.Column(db.Integer, nullable=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    move_in_date = db.Column(db.DateTime)

    # Relationships
    property = db.relationship('Property', back_populates="renter", uselist=False)
    
    def __init__(self, full_name, email, phone_number, move_in_date, property_id):
        self.full_name = full_name;
        self.email = email;
        self.phone_number = phone_number;
        self.move_in_date = move_in_date;
        self.property_id = property_id;
