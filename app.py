from flask import Flask, render_template, url_for, request, redirect, flash, session
from models import db, Property, Renter, MaintenanceRequest
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = '123456'  # Replace with a more secure and unique key


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rental_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads/'  # Directory to store uploaded images

#initializing the database
db.init_app(app)

migrate = Migrate(app, db)

engine = create_engine('sqlite:///./rental_management.db')  # Current folder

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


@app.route('/manage_properties', methods=['GET', 'POST'])
def manage_properties():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        location = request.form.get('location')
        rent = request.form.get('rent')
        amenities = request.form.get('amenities')
        photo_path = request.form.get('photo_path')
        description = request.form.get('description')

        new_property = Property(
            name=name,
            location=location,
            rent=rent,
            amenities=amenities,
            photo_path=photo_path,
            description=description
        )

        try:
            db.session.add(new_property)
            db.session.commit()

            # After adding, redirect to the same route to display updated properties
            return redirect(url_for('manage_properties'))

        except Exception as e:
            return f"There was an issue adding the property: {e}"

    # If method is GET, display the form and properties
    properties = Property.query.all()  # Query all properties from the database
    return render_template('manage_properties.html', properties=properties)

# Route to edit a property
@app.route('/edit_property/<int:id>', methods=['GET', 'POST'])
def edit_property(id):
    property_to_edit = Property.query.get_or_404(id)

    if request.method == 'POST':
        property_to_edit.name = request.form('name')
        property_to_edit.location = request.form('location')
        property_to_edit.rent_amount = request.form('rent_amount')
        property_to_edit.amenities = request.form('amenities')
        property_to_edit.photo_path = request.form('photo_path')
        property_to_edit.description = request.form('description')

        try:
            db.session.commit()
            return redirect('/property_management')
        except Exception as e:
            return f"There was a problem editing the property: {e}"

    return render_template('edit_property.html', property=property_to_edit)

# Route to delete a property
@app.route('/delete_property/<int:id>')
def delete_property(id):
    property_to_delete = Property.query.get_or_404(id)

    try:
        db.session.delete(property_to_delete)
        db.session.commit()
        return redirect('/manage_properties')
    except Exception as e:
        return f"There was a problem deleting the property: {e}"


@app.route('/manage_profile', methods=['GET', 'POST'])
def manage_profile():
    if request.method == 'POST':
        print(request.form)
        # Get form data
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        move_in_date_str = request.form.get('move_in_date')
        property_id = request.form.get('property_id')

        # Debugging: Print parsed form data
        print(f"Name: {full_name}, Email: {email}, Phone: {phone_number}, Move-in Date: {move_in_date_str}, Property: {property_id}")
        
        try:
            # Convert move_in_date_str to datetime object
            move_in_date = datetime.strptime(move_in_date_str, '%Y-%m-%d')

            # Create a new Renter instance
            new_renter = Renter(
                full_name=full_name,
                email=email,
                phone_number=phone_number,
                move_in_date=move_in_date,
                property_id=property_id
            )

            # Save the new renter to the database
            db.session.add(new_renter)
            db.session.commit()

            print(f"Renter {new_renter.full_name} added successfully!")

            # Redirect to view the profile
            return redirect(url_for('view_profile', renter_id=new_renter.id))

        except Exception as e:
            flash(f"There was an issue saving the profile: {e}", 'danger')
            return redirect(url_for('manage_profile'))  # Redirect back to the form on error

    # Query properties for GET request (form display)
    properties = Property.query.all()
    return render_template('manage_profile.html', properties=properties)


@app.route('/view_profile/<int:renter_id>', methods=['GET'])
def view_profile(renter_id):
    # Query the renter's profile using their ID
    renter = Renter.query.get_or_404(renter_id)

    # Render the profile page and pass the renter object
    return render_template('view_profile.html', renter=renter)

@app.route('/edit_profile/<int:renter_id>', methods=['GET', 'POST'])
def edit_profile(renter_id):
    renter = Renter.query.get_or_404(renter_id)

    if request.method == 'POST':
        renter.full_name = request.form.get('full_name')
        renter.email = request.form.get('email')
        renter.phone_number = request.form.get('phone_number')
        renter.move_in_date = datetime.strptime(request.form.get('move_in_date'), '%Y-%m-%d')
        renter.property_id = request.form.get('property_id')

        db.session.commit()
        return redirect(url_for('view_profile', renter_id=renter.id))

    properties = Property.query.all()
    return render_template('edit_profile.html', renter=renter, properties=properties)


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

@app.route('/rent-tracking', methods=['GET'])
def rent_tracking():
    properties = Property.query.all()
    
    total_rent_collected = 0
    total_outstanding = 0
    for property in properties:
        for payment in property.payments:
            if payment.payment_status == 'Paid':
                total_rent_collected += payment.amount_paid
            else:
                total_outstanding += property.rent_amount - payment.amount_paid

    return render_template('rent_tracking.html', properties=properties, 
                           total_rent_collected=total_rent_collected, total_outstanding=total_outstanding)


if __name__ == '__main__':
    app.run(debug=True)
