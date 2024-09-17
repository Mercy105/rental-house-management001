from flask import Flask, render_template, url_for, request, redirect, flash
from models import db, Property, Renter, MaintenanceRequest
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

@app.route('/request_demo')
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

@app.route('/manage_profile', methods=['GET'])
def manage_profile():
    return render_template('manage_profile.html')

@app.route('/save_profile', methods=['POST'])
def save_profile():
    # Get form data
    full_name = request.form.get('full_name')
    email = request.form.get('email')
    phone_number = request.form.get('phone_number')
    move_in_date = request.form.get('move_in_date')

    # Assuming you have a Renter model with fields: full_name, email, phone, move_in_date
    new_profile = Renter(full_name=full_name, email=email, phone_number=phone_number, move_in_date=move_in_date)
    
    # Save to the database
    db.session.add(new_profile)
    db.session.commit()

    flash('Profile updated successfully!', 'success')
    return redirect(url_for('renter_dashboard'))  # Redirect back to the renter's dashboard

@app.route('/maintenance_request', methods=['GET'])
def maintenance_request():
    return render_template('maintenance_request.html')

@app.route('/submit_request', methods=['POST'])
def submit_request():
     # Get form data
    property_id = request.form.get['property_id']
    description = request.form.get['description']
        
    # Handle photo upload
    photo = request.files.get('photo')
    photo_filename = None
    if photo and photo.filename != '':
        photo_filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))

    # Create new MaintenanceRequest
    new_request = MaintenanceRequest(
        property_id=property_id,
        description=description,
        photo_path=photo_filename  # Save photo path if it was uploaded
    )

    # Save to database
    db.session.add(new_request)
    db.session.commit()

    # Redirect or give success message
    return redirect(url_for('maintenance_request'))

@app.route('/pay_rent', methods=['GET'])
def pay_rent():
    # page that contains the Mpesa details
    return render_template('pay_rent.html', landlord_phone='+254799005767')

# Sample data for demonstration
payment_history_data = [
    {
        'date': '2024-09-10',
        'amount': '1200',
        'method': 'M-Pesa',
        'status': 'Completed',
        'transaction_id': 'TXN1234567',
        'invoice_link': '#'
    },
    {
        'date': '2024-08-10',
        'amount': '1200',
        'method': 'M-Pesa',
        'status': 'Completed',
        'transaction_id': 'TXN1234568',
        'invoice_link': '#'
    }
]

@app.route('/payment_history')
def payment_history():
    return render_template('payment_history.html', payment_history=payment_history_data)

# Sample data for notifications
notifications_data = [
    {
        'title': 'Payment Reminder',
        'message': 'Your rent is due on 30th September 2024. Please make sure to complete the payment.',
        'date': '2024-09-17',
        'type': 'alert'
    },
    {
        'title': 'Maintenance Request Update',
        'message': 'Your maintenance request for plumbing has been completed.',
        'date': '2024-09-15',
        'type': 'success'
    },
    {
        'title': 'Lease Renewal Reminder',
        'message': 'Your lease is up for renewal on 1st November 2024. Please contact us for further instructions.',
        'date': '2024-09-10',
        'type': 'warning'
    },
    {
        'title': 'General Notice',
        'message': 'The building will undergo scheduled maintenance on 22nd September. Expect water disruptions.',
        'date': '2024-09-05',
        'type': 'info'
    }
]

@app.route('/notifications')
def notifications():
    return render_template('notifications.html', notifications=notifications_data)


if __name__ == '__main__':
    app.run(debug=True)
