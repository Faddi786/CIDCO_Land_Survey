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
    value_softdel = db.Column(db.Integer)


    def __repr__(self):
        return f'<DropdownValues are : {self.dropdownvalues_uid}, {self.node_name}, {self.sector}, {self.block_name}, {self.plot_no},{self.value_softdel}>'






# Route to fetch data for dropdowns
@app.route('/dropdown_values_admin_panel', methods=['GET'])
def dropdown_values_admin_panel():
    # the thing doesnt ends here since we are using soft delte with the help of the another column as is_dropdownvalues_active so when the page loads the filtering logic where we have put we also have to consider a condition that to filter the data where is_dropdownvalues_active is 1
    # dont use all instead add a condition that is_dropdownvalues_active should be 1 where 1 means active
    
    # Query all the values from the DropdownValues table
    dropdown_data = dropdown_values.query.filter_by(value_softdel=1).all()


    # Prepare the data to be returned as JSON
    data = {
        'dropdownvalues_uid': [item.dropdownvalues_uid for item in dropdown_data],
        'Node_Name': [item.node_name for item in dropdown_data],
        'Sector': [item.sector for item in dropdown_data],
        'Block_Name': [item.block_name for item in dropdown_data],
        'Plot_No': [item.plot_no for item in dropdown_data],
        'value_softDel':[item.value_softdel for item in dropdown_data]
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
    
    print(updated_data)
    # Extract values from the received JSON
    node_name = updated_data.get('column1')
    sector = updated_data.get('column2')
    block_name = updated_data.get('column3')
    plot_no = updated_data.get('column4')
    dropdownvalues_uid = updated_data.get('uid')
    #first take the uid that we are getting from the requrest
    # then go in the dropdownvalue_uid column match this uid if match found then go in the is_dropdownvalues_active and set this value to 0 
    # so basically we are soft deleleting the entry but the data persists in the database table
    
    print("these si the uid")
    print(dropdownvalues_uid)


    print("these are the values we got from the updated drop down values")
    print(node_name,sector,block_name,plot_no)
    # Find the record in the database to update (example: updating the first record)
    record = dropdown_values.query.filter_by(dropdownvalues_uid=dropdownvalues_uid).first() # You can modify this to update a specific record

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

    record = dropdown_values.query.filter_by(dropdownvalues_uid=uid_to_delete).first()
    print(f"value of record is: {record}")

    
    if record:
        # Update the 'value_softDel' column to 0
        record.value_softdel = 0
        
        # Commit the changes to the database
        db.session.commit()

        # # Optionally, refresh the record to ensure the update is applied
        # db.session.refresh(record)
        
        # Respond back to the front end
        return jsonify({'message': 'Record updated successfully', 'uid': uid_to_delete})
    else:
        return jsonify({'message': 'UID not found', 'uid': uid_to_delete}), 404





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