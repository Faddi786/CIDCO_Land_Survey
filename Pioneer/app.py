from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Update the database URI to MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Akhatri%402023@localhost/plot_details'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable track modifications to save memory
app.config['UPLOAD_FOLDER'] = './uploads'  # Folder to save uploaded files

db = SQLAlchemy(app)

# for registration form
@app.route('/regiForm')
def regiForm():
    return render_template('regiForm.html')

@app.route('/manager')
def manager():
    return render_template('manager.html')

# Route for the user page
@app.route('/user')
def user():
    return render_template('user.html')

@app.route('/')
def index():
    return render_template('admin.html')

@app.route('/loginForm', methods=['GET', 'POST'])
def login():
    return render_template('loginForm.html')  # Display login form


class UserInfo(db.Model):
    userinfo_uid = db.Column(db.Integer, primary_key=True)
    phone_no = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Integer, nullable=False)


# Define the model for dropdown_values table
class dropdown_values(db.Model):
    dropdownvalues_uid = db.Column(db.Integer, primary_key=True)
    node_name = db.Column(db.String(255))
    sector = db.Column(db.String(255))
    block_name = db.Column(db.String(255))
    plot_no = db.Column(db.String(255))

    def __repr__(self):
        return f'<DropdownValues {self.node_name}, {self.sector}, {self.block_name}, {self.plot_no}>'






# Route to fetch data for dropdowns
@app.route('/dropdown_values_admin_panel', methods=['GET'])
def dropdown_values_admin_panel():
    # Query all the values from the DropdownValues table
    dropdown_data = dropdown_values.query.all()

    # Prepare the data to be returned as JSON
    data = {
        'dropdownvalues_uid': [item.dropdownvalues_uid for item in dropdown_data],
        'Node_Name': [item.node_name for item in dropdown_data],
        'Sector': [item.sector for item in dropdown_data],
        'Block_Name': [item.block_name for item in dropdown_data],
        'Plot_No': [item.plot_no for item in dropdown_data]
    }

    # Print the data before calling jsonify
    print("Data being sent as JSON response:")
    print(data)  # This prints the Python dictionary  
    return jsonify(data)  # This sends the data as a JSON response



    
# Route to update data in the database
@app.route('/update_dropdown_values', methods=['POST'])
def update_dropdown_values():
    # Get the updated data from the frontend
    updated_data = request.get_json()  # Get the JSON data sent from frontend

    # Extract values from the received JSON
    node_name = updated_data.get('column1')
    sector = updated_data.get('column2')
    block_name = updated_data.get('column3')
    plot_no = updated_data.get('column4')

    print("these are the values we got from the updated drop down values")
    print(node_name,sector,block_name,plot_no)
    # Find the record in the database to update (example: updating the first record)
    record = dropdown_values.query.first()  # You can modify this to update a specific record

    # Update the fields
    if record:
        record.node_name = node_name
        record.sector = sector
        record.block_name = block_name
        record.plot_no = plot_no

        # Commit the changes to the database
        db.session.commit()

        # Return success response
        return jsonify({'success': True})

    return jsonify({'success': False, 'message': 'Record not found'})
    


# Define the route to handle the delete request
@app.route('/delete_values', methods=['POST'])
def delete_values():
    # Get the JSON data sent from the front end
    request_data = request.get_json()
    
    # Extract the uid from the request data
    uid_to_delete = request_data.get('uid')
    
    # Print the UID to the console
    print("Received UID to delete:", uid_to_delete)
    
    # Optionally, you can implement logic to delete the corresponding record in the database
    # e.g., dropdown_values.query.filter_by(dropdownvalues_uid=uid_to_delete).delete()
    
    # Respond back to the front end
    return jsonify({'message': 'UID received', 'uid': uid_to_delete})





@app.route('/phone_no_validation', methods=['GET'])
def phone_no_validation():
    # Query all the user data from the UserInfo table
    userdetails = UserInfo.query.all()

    # Prepare the data to be returned as JSON, including all fields from the UserInfo table
    users_data = [
        {
            'userinfo_uid': user.userinfo_uid,
            'phone_no': user.phone_no,
            'name': user.name,
            'role': user.role
        }
        for user in userdetails
    ]

    # Print the data before sending the response for debugging
    print("Data being sent as JSON response:")
    print(users_data)

    # Return the users' data as a JSON response
    return jsonify({'users': users_data})






if __name__ == '__main__':
    app.run(debug=True)
