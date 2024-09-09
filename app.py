from flask import Flask, render_template, url_for, request, redirect
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/uploads/'  # Directory to store uploaded images

# Sample in-memory database for demonstration purposes
properties = []

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
@app.route('/manage_properties')
def manage_properties():
    return render_template('property_management.html', properties=properties)

# Route to add a property
@app.route('/add_property', methods=['GET'])
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

    # Add the new property to the properties list
    properties.append({
        'id': len(properties) + 1,
        'name': property_name,
        'location': location,
        'rent': rent,
        'amenities': amenities,
        'photo_path': photo_filename
    })

    return redirect(url_for('add_property'))

# Route to edit a property (placeholder for demo purposes)
@app.route('/edit_property/<int:property_id>')
def edit_property(property_id):
    # Implement logic to edit the property
    return f"Edit property with ID {property_id}"

# Route to delete a property
@app.route('/delete_property/<int:property_id>')
def delete_property(property_id):
    global properties
    # Filter out the property to delete
    properties = [prop for prop in properties if prop['id'] != property_id]
    return redirect(url_for('manage_properties'))


if __name__ == '__main__':
    app.run(debug=True)
