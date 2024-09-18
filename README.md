# Rental House Management System
![Screenshot (56)](https://github.com/user-attachments/assets/7b657108-f49a-440f-b6c6-d512eab4b0e3)

## Introduction
The Rental Management System is a web application designed to simplify the relationship between landlords and tenants by providing a clear, organized, and transparent way to handle rental payments, property management, and maintenance requests. The platform allows landlords to manage multiple properties, track rent payments, and communicate with tenants efficiently, while tenants can submit payments online, view payment history, and request maintenance.

- Final Project Blog Article: [https://medium.com/@donamaitsa/introduction-87bec6765603]
- Author: [https://www.linkedin.com/in/donnelly-amaitsa-442067279/]

## Features
- Add, update, and delete rental properties
- Manage tenant information
- View property details
- Search for properties

## Technologies Used
- **Python**: Backend logic
- **Flask web application framework**: To help in connecting to the database
- **HTML**: Structure of the web pages
- **CSS**: Styling of the web pages
- **JavaScript**: Client-side scripting

## Installation
To set up and run the application:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Mercy105/rental-house-management001.git

2. **Install flask application in your VS Code Terminal:**
    ```bash
    pip install flask

3. **Start a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    
4. **Setup the database:**
   ```bash
   & python3
   >>> from app import app, db
   >>> app.app_context().push()
   >>> db.create_all()
   >>> exit()

5. **Run the application:**
   ```bash
   python3 app.py

6. **Access web app from your local machine:**
   http://127.0.0.1:5000

## Usage
- Landlords: Can manage properties, view tenants' rent history, track payments, and handle maintenance requests.
- Tenants: Can submit rent payments online, view payment history, and request maintenance through a dedicated dashboard.
- Both users will receive notifications about upcoming rent payments or pending requests.

## Contributing
We welcome contributions to the Rental Management System project! If you would like to contribute, please follow these steps:
1. Fork the repository
2. Create a new branch
   ```bash
   git checkout -b branch-name
3. Make changes and commit them
   ```bash
   git commit -m 'Add some feature'
4. Push your branch
   ```bash
   git push origin feature-name

## Related Projects
- AppFolio: [https://www.appfolio.com/]

## Licensing
This project is licensed under the MIT License.
