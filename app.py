from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)


@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/request-demo')
def request_demo():
    # Redirects to the role selection page when the "Request Demo" button is clicked
    return render_template('role_selection.html')

@app.route('/dashboard')
def dashboard():
    role = request.args.get('user_role')
    if role == 'landlord':
        return render_template('landlord_dashboard.html')
    elif role == 'renter':
        return render_template('renter_template.html')
    else:
        # if no role is selected
        return redirect(url_for('request_demo'))
    

if __name__ == '__main__':
    app.run(debug=True)
