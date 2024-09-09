from flask import Flask, render_template, url_for, request, redirect
from models import db, Property, Tenant, RentPayment, MaintenanceRequest
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rental_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads/'  # Directory to store uploaded images

db.init_app(app)

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/request-demo')
def request_demo():
    # Redirects to the role selection page when the "Request Demo" button is clicked
    return render_template('role_selection.html')

@app.route('/dashboard')
def dashboard():
    role = request.args.get('role')
    if role == 'landlord':
        return render_template('landlord_dashboard.html')
    elif role == 'renter':
        return render_template('renter_dashboard.html')
    else:
        # if no role is selected
        return redirect(url_for('request_demo'))

@app.route('/pay_rent', methods=['POST'])
def pay_rent():
    # Use M-Pesa API SDK or HTTP request to initiate payment
    phone_number = request.form.get('phone')
    amount = request.form.get('amount')
    # Logic to interact with M-Pesa API here
    
    # If payment is successful, save the transaction details
    return redirect(url_for('payment_history'))

# Route to manage properties
@app.route('/property_management')
def property_management():
    # Retrieve all properties from the database
    properties = Property.query.all()
    return render_template('property_management.html', properties=properties)

# Add property page
@app.route('/add_property_page')
def add_property_page():
    return render_template('add_property.html')

# Route to add a property
@app.route('/add_property', methods=['POST'])
def add_property():
    property_name = request.form.get('name')
    location = request.form.get('location')
    rent = request.form.get('rent')
    amenities = request.form.get('amenities')
    photo = request.files.get('photo')

    # Save the uploaded photo
    if photo:
        photo_filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))
    else:
        photo_filename = None

    # Create a new Property object and add it to the database
    new_property = Property(
        name=property_name,
        location=location,
        rent=rent,
        amenities=amenities,
        photo_path=photo_filename
    )
    db.session.add(new_property)
    db.session.commit()
    
    # redirect to manage properties page after adding
    return redirect(url_for('manage_properties'))

# Route to edit a property
@app.route('/edit_property/<int:property_id>', methods=['GET', 'POST'])
def edit_property(property_id):
    # Retrieve the property to be edited
    property_to_edit = Property.query.get_or_404(property_id)
    
    if request.method == 'POST':
        # Update the property details from the form
        property_to_edit.name = request.form['name']
        property_to_edit.location = request.form['location']
        property_to_edit.rent = request.form['rent']
        property_to_edit.amenities = request.form['amenities']
        
        # Update the photo if a new one is uploaded
        if request.files['photo']:
            photo = request.files['photo']
            photo_filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))
            property_to_edit.photo_path = photo_filename

        # Commit changes to the database
        db.session.commit()
        return redirect(url_for('manage_properties'))

    return render_template('edit_property.html', property=property_to_edit)

# Route to delete a property
@app.route('/delete_property/<int:property_id>', methods=['POST'])
def delete_property(property_id):
    # Find the property to delete and remove it from the database
    property_to_delete = Property.query.get_or_404(property_id)
    db.session.delete(property_to_delete)
    db.session.commit()
    return redirect(url_for('manage_properties'))

if __name__ == '__main__':
    app.run(debug=True)
