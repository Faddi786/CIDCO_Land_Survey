from flask import Flask, render_template, request, redirect, jsonify,session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from multiprocessing import connection
from flask_cors import CORS
from static.python_functions import helper_functions


app = Flask(__name__)
CORS(app)

# Update the database URI to MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Akhatri%402023@localhost/plot_details'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable track modifications to save memory
app.config['UPLOAD_FOLDER'] = './uploads'  # Folder to save uploaded files

# Update the database URI to MySQL
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Akhatri%402023@localhost/plot_details_db'
db = SQLAlchemy(app)

#--------------------------------------------------------------------------------
                                    # Template Routes
@app.route('/')
def index():
    return render_template('loginForm.html')


# for registration form
@app.route('/regiForm')
def regiForm():
    return render_template('regiForm.html')

@app.route('/manager')
def manager():
    return render_template('manager.html')

# Route for the user page
@app.route('/survey_user')
def survey_user():
    return render_template('survey_user.html')



# Route for the user page
@app.route('/validator_user')
def validator_user():
    return render_template('validator_user.html')


@app.route('/validator_verify')
def validator_verify():
    return render_template('validator_form_accept_reject.html')


# Route for the user page
@app.route('/admin_user')
def admin_user():
    return render_template('admin_user.html')


@app.route('/admin_table')
def admin_table():
    return render_template('admin.html')

@app.route('/userInfo_edit_byAdmin')
def userInfo_edit_byAdmin():
    return render_template('userInfo_edit_byAdmin.html')


# Route for the user page
@app.route('/qc_user')
def qc_user():
    return render_template('qc_user.html')


# Route for the user page
@app.route('/survey_form_input')
def survey_form_input():
    return render_template('survey_form_input.html')





@app.route('/loginForm', methods=['GET', 'POST'])
def login():
    return render_template('loginForm.html')  # Display login form



@app.route('/qcTable')
def qcTable():
    return render_template('qc_output_table.html')


@app.route('/survey_output_form')
def survey_output_form():
    return render_template('qc_form_verify.html')


@app.route('/qc_form')
def qc_form():
    return render_template('qc_form.html')

@app.route('/validator_form_accept_reject')
def validator_form_accept_reject():
    return render_template('validator_form_accept_reject.html')



@app.route('/validator_table')
def validator_table():
    return render_template('validatorOUTPUTtable.html')



@app.route("/editByQC",methods=['POST','GET'])
def editByQC():
    return render_template('editByQC.html')


# {}



# {}


#----------------------------------------------------------------------------------------------------
                                         # Classes

class user_info(db.Model):
    userinfo_uid = db.Column(db.Integer, primary_key=True)
    phone_no = db.Column(db.Integer, nullable=False)    # not sure yaha dataType biginteger aiga k nai... since DB me bigINt hai
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Integer, nullable=False)
    value_softdel = db.Column(db.Integer)

    def __repr__(self):
        return f'<DropdownValues are : {self.userinfo_uid}, {self.phone_no}, {self.name}, {self.name}, {self.role},{self.value_softdel}>'


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




# Model for storing plot details
class survey_form_data(db.Model):
    surveyformdata_uid = db.Column(db.Integer, primary_key=True)#
    #plotdetails_uid=db.Column(db.Integer,primary_key=True)#this has been deleted frm the database instead of this we have above variable 
    user_name = db.Column(db.String(200), nullable=True) #
    node_name = db.Column(db.String(100), nullable=True)#
    sector_no = db.Column(db.String(100), nullable=True)#
    block_name = db.Column(db.String(100), nullable=True)#
    plot_name = db.Column(db.String(100), nullable=True)#
    allotment_date = db.Column(db.Date, nullable=True)#
    plot_status = db.Column(db.String(20),nullable=True)
    original_allottee = db.Column(db.String(200), nullable=True)#
    area = db.Column(db.String(1000), nullable=True)#
    use_of_plot = db.Column(db.String(100), nullable=True)#
    FSI = db.Column(db.Float, nullable=True)
    term_of_lease = db.Column(db.Integer ,nullable=True)
    rate = db.Column(db.Float, nullable=True)#
    ownerNtransferDate = db.Column(db.String(10000), nullable=True)#
    surveyor_remarks = db.Column(db.Text, nullable=True)#
    entry_date_created = db.Column(db.DateTime, default=datetime.utcnow)#
    front_photo =  db.Column(db.String(500), nullable=True)#
    left_photo =  db.Column(db.String(1000), nullable=True)#
    back_photo =  db.Column(db.String(1000), nullable=True)#
    right_photo =  db.Column(db.String(1000), nullable=True)#
    plot_sketch =  db.Column(db.String(500), nullable=True)#
    surveyform_status = db.Column(db.Integer,default=0 , nullable=False)#
    is_qc_done = db.Column(db.Integer,default=0 , nullable=False)#
    is_validation_done = db.Column(db.Integer,default=0 , nullable=False)#
    validator_remarks = db.Column(db.String(200), nullable=False)#

    def __repr__(self):
        return f"<Plot {self.surveyformdata_uid}>"

# Define the sector_table model
class sector_table(db.Model):
    __tablename__ = 'sector_table'
    user_name = db.Column(db.String(255), nullable=False)
    phone_no = db.Column(db.String(15), nullable=False)
    sector_name = db.Column(db.String(255), nullable=False)
    sectortable_uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sectortable_isactive = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<SectorTable: user_name='{self.user_name}', sector_name='{self.sector_name}', phone_no='{self.phone_no}', sectortable_isactive='{self.sectortable_isactive}'>"
    




#--------------------------------------------------------------------------------
                                    # Data Routes




                # Module
#----------------------------------------------
                # Login Page


@app.route('/phone_no_validation', methods=['GET'])
def phone_no_validation():
    # Query all the user data from the user_info table
    userdetails = user_info.query.all()

    # Prepare the data to be returned as JSON, including all fields from the user_info table
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
    print("Data being sent as JSON response: user_data")
    print(users_data)

    # Return the users' data as a JSON response
    return jsonify({'users': users_data})


                # Module
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                # Input Survey Form



# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'images'  # Folder to store images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif','jfif','avif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the images folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Route to fetch filtered dropdown data
@app.route('/get_dropdown_values', methods=['GET'])
def get_dropdown_values():
    # Get filter parameters from request arguments
    node_name = request.args.get('node_name')
    sector = request.args.get('sector')
    block_name = request.args.get('block_name')

    # Query the database and filter based on the parameters
    query = dropdown_values.query

    if node_name:
        query = query.filter_by(node_name=node_name)
    if sector:
        query = query.filter_by(sector=sector)
    if block_name:
        query = query.filter_by(block_name=block_name)

    dropdown_data = query.all()

    # Prepare the response data with unique values
    data = {
        'Node_Name': list(set(item.node_name for item in dropdown_data if item.node_name)),
        'Sector': list(set(item.sector for item in dropdown_data if item.sector)),
        'Block_Name': list(set(item.block_name for item in dropdown_data if item.block_name)),
        'Plot_No': list(set(item.plot_no for item in dropdown_data if item.plot_no))
    }

    # print("Filtered data being sent as JSON response:")
    # print(data)

    return jsonify(data)



# Route to handle form submission
@app.route('/submit_form_data', methods=['POST', 'GET'])
def submit_form_data():
    if request.method == 'POST':
        try:
            # Extract form data
            user_name = request.form.get('user_name')#
            node_name = request.form.get('node_name')#
            sector_no = request.form.get('sector_no')#
            block_name = request.form.get('block_name')#
            plot_name = request.form.get('plot_name')#
            plot_status = request.form.get('plot_status')
            allotment_date = request.form.get('allotment_date')#
            original_allottee = request.form.get('original_allottee')#
            area = request.form.get('area')#
            use_of_plot = request.form.get('use_of_plot')#
            FSI = request.form.get('FSI')
            term_of_lease = request.form.get('term_of_lease')
            rate = request.form.get('rate')#
            ownerNtransferDate = request.form.get('ownerNtransferDate')#
            surveyor_remarks = request.form.get('surveyor_remarks')#
 

            # Process uploaded files
            front_photo = request.files.get('front_photo')#
            left_photo = request.files.get('left_photo')#
            back_photo = request.files.get('back_photo')#
            right_photo = request.files.get('right_photo')#
            plot_sketch = request.files.get('plot_sketch')#

            # Save each file if present and allowed
            def save_file(file):
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    return filename
                return None

            front_photo_filename = save_file(front_photo)
            left_photo_filename = save_file(left_photo)
            back_photo_filename = save_file(back_photo)
            right_photo_filename = save_file(right_photo)
            plot_sketch_filename = save_file(plot_sketch)

            # print(front_photo_filename,left_photo_filename)


            print(user_name, node_name, sector_no, block_name, plot_name,plot_status, allotment_date, original_allottee, area, use_of_plot,FSI,term_of_lease, rate, ownerNtransferDate, surveyor_remarks)
            print("about to take store ")

            # Create a new plot_details record
            new_plot = survey_form_data(
                user_name=user_name, #
                node_name=node_name,
                sector_no=sector_no,
                block_name=block_name,
                plot_name=plot_name,
                plot_status = plot_status,
                allotment_date=allotment_date,
                original_allottee=original_allottee,
                area=area,
                use_of_plot=use_of_plot,
                FSI = FSI,
                term_of_lease = term_of_lease,
                rate=rate,
                ownerNtransferDate=ownerNtransferDate,
                surveyor_remarks=surveyor_remarks,
                front_photo=front_photo_filename,
                left_photo=left_photo_filename,
                back_photo=back_photo_filename,
                right_photo=right_photo_filename,
                plot_sketch=plot_sketch_filename,
            )

            print(';;;;;;;;;;')
            print(f"User Name: {new_plot.user_name}")

            print(new_plot)
            # Save to the database
            db.session.add(new_plot)
            db.session.commit()
            print('committted to DB')

            return redirect('/survey_user')
        except Exception as e:
            return f"There was an issue submitting the form: {str(e)}"
    else:
        print("error aala ")
        return render_template('survey_user.html')








                # Module
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                # Output table (QC/Validator/Admin)






# Example route to query plot details
@app.route('/query_plots', methods=['POST','GET'])
def query_plots():
    # Retrieve the button value from the form
    button = request.form.get('button', 'default')

    # Retrieve role and sector from the session
    role = "qc"
    sector = "1"

    if not role or not sector:
        return jsonify({"error": "Role and sector must be set in session"}), 400

    # Use the query function
    try:
        results = query_plot_details(role, button, sector)
        return jsonify([plot.to_dict() for plot in results])  # Convert results to JSON-friendly format
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/output_table', methods=['POST', 'GET'])
def output_table():

    print("flask route")
    # Query the required columns from the survey_form_data table
    plots = survey_form_data.query.with_entities(
        survey_form_data.node_name,
        survey_form_data.sector_no,
        survey_form_data.block_name,
        survey_form_data.plot_name,
        survey_form_data.plot_status,
        survey_form_data.entry_date_created,
        survey_form_data.user_name.label('surveyor_name'),  # Assuming 'user_name' is the surveyor's name
        survey_form_data.surveyformdata_uid,
        survey_form_data.surveyor_remarks, # {}
        survey_form_data.surveyform_status,
        survey_form_data.is_qc_done,
        survey_form_data.is_validation_done,
        survey_form_data.validator_remarks
    ).all()

    # Prepare the data to return
    output = []
    for plot in plots:
        plot_data = {
            'node_name': plot.node_name,
            'sector_no': plot.sector_no,
            'block_name': plot.block_name,
            'plot_name': plot.plot_name,
            'plot_status':plot.plot_status,
            'date_uploaded': plot.entry_date_created.strftime('%Y-%m-%d %H:%M:%S'),
            'surveyor_name': plot.surveyor_name,
            'surveyformdata_uid': plot.surveyformdata_uid,
            'surveyor_remarks':plot.surveyor_remarks,
            'surveyform_status': plot.surveyform_status,
            'is_qc_done': plot.is_qc_done,
            'is_validation_done':plot.is_validation_done,
            'validator_remarks':plot.validator_remarks
        }
        output.append(plot_data)


    print("this is the output table data")
    print(output)

    return jsonify(output)


json_data = {}

@app.route('/send_formid')
def send_formid():
    global json_data

    surveyformdata_uid = request.args.get('form_id')
    print('this is the formid', surveyformdata_uid)

      # Extract data from the DB based on the form_id
    try:
        json_data = extract_rows_from_db(surveyformdata_uid)
        print('This is the data that we extracted from db for the id ', json_data)  # This is your data for the given form_id
        return jsonify({"message": "Form ID received successfully"}), 200
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "Failed to retrieve data from the database"}), 500




@app.route('/get_outputform_data' )
def get_outputform_data():
    global json_data
    print('this is the filtered df for the given form id   ..................  get_outputform_data ', json_data)

    # Convert DataFrame to JSON
    return jsonify(json_data)



# {} UPDATE IN DB BY QC



# {}






@app.route('/update_validation', methods=['POST'])
def update_validation():
    
    request_data = request.get_json()

    surveyformdata_uid = request_data.get('surveyformdata_uid')
    is_validation_done = request_data.get('is_validation_done')
    surveyform_status = request_data.get('surveyform_status')
    is_qc_done = request_data.get('is_qc_done')
    validator_remarks = request_data.get('validator_remarks')
    print("Received data:", request_data)

    if not surveyformdata_uid or is_validation_done is None:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Query the existing record
        survey_form = db.session.query(survey_form_data).filter_by(surveyformdata_uid=surveyformdata_uid).first()
        
        if not survey_form:
            return jsonify({"error": "Survey form not found"}), 404

        # Update the fields based on validation status
        if is_validation_done == 1:  # Accept
            survey_form.is_validation_done = is_validation_done
            survey_form.surveyform_status = surveyform_status
        elif is_validation_done == 2:  # Reject
            survey_form.is_validation_done = is_validation_done
            survey_form.is_qc_done = is_qc_done
            survey_form.surveyform_status = surveyform_status
            survey_form.validator_remarks = validator_remarks

        # Commit changes to the database
        db.session.commit()

        return jsonify({"message": "Validation updated successfully!"})

    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred while updating validation"}), 500






                # Module
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                                        # Admin Panel

                
#----------------------------------------------
                # Dropdown Values Page (Admin)

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
    print("Data being sent as JSON response: data")
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



                # Module
#----------------------------------------------
                # Manage Sector (Admin)



@app.route('/onload_manage_sector', methods=['GET'])
def onload_manage_sector():
    try:
        # print("[DEBUG] Entered onload_manage_sector route")
        
        # Retrieve all data from sector_table
        # print("[DEBUG] Querying SectorTable...")
        sectors = sector_table.query.filter_by(sectortable_isactive=1).all()
        # print(f"[DEBUG] Retrieved {len(sectors)} records from SectorTable")

        # Convert data to a list of dictionaries
        sector_list = []
        for sector in sectors:
            sector_data = {
                "user_name": sector.user_name,
                "phone_no": sector.phone_no,
                "sector_name": sector.sector_name,
                "sectortable_uid":sector.sectortable_uid,
                "sectortable_isactive":sector.sectortable_isactive
            }
            sector_list.append(sector_data)
        
        print(f"[DEBUG] these are the records to be sent to the web page {sector_list}")

        # print("[DEBUG] Successfully created sector list")
        return jsonify(sector_list), 200
    except Exception as e:
        print(f"[ERROR] Exception occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500






@app.route('/del_values', methods=['POST', 'GET'])
def del_values():
    # Get the JSON data sent from the front end
    request_data = request.get_json()
    
    # Extract the sectortable_uid from the request data
    sectortable_uid_to_delete = request_data.get('sectortable_uid')
    
    # Print the sectortable_uid to the console for debugging
    print("Received UID to delete:", sectortable_uid_to_delete)

    # Query the database to find the record by sectortable_uid
    record = sector_table.query.filter_by(sectortable_uid=sectortable_uid_to_delete).first()
    print(f"value of record is: {record}")

    if record:
        # Update the 'phone_no' column (or another column if necessary) to mark as deleted
        record.sectortable_isactive = '0'  # Setting the phone_no to '0' to mark as deleted
        
        # Commit the changes to the database
        db.session.commit()

        # Respond back to the front end
        return jsonify({'message': 'Record updated successfully', 'sectortable_uid': sectortable_uid_to_delete})
    else:
        return jsonify({'message': 'UID not found', 'sectortable_uid': sectortable_uid_to_delete}), 404





@app.route('/update_values', methods=['POST'])
def update_values():
    # Get the JSON data sent from the front end
    request_data = request.get_json()
    print("we are here boysss")
    print(request_data)
    # Extract the values from the request
    sectortable_uid = request_data.get('sectortableUid')
    user_name = request_data.get('username')
    sector_name = request_data.get('sectorName')
    phone_no = request_data.get('phoneNo')

    # Print the received data for debugging
    print(f"Received data to update: UID={sectortable_uid}, User={user_name}, Sector={sector_name}, Phone={phone_no}")

    # Query the database to find the record by sectortable_uid
    record = sector_table.query.filter_by(sectortable_uid=sectortable_uid).first()
    print("we are here after the record tabels")
    print("this is the record")
    print(record)
    if record:
        print("we are insinde the record if statmenet ")
        # Update the fields with the new values
        record.user_name = user_name
        record.sector_name = sector_name
        record.phone_no = phone_no

        # Commit the changes to the database
        db.session.commit()

        # Respond back to the front end
        return jsonify({'message': 'Record updated successfully'})
    else:
        return jsonify({'message': 'UID not found'}), 404
    



#----------------------------------------------
# Employee Table (Admin) - Put Code here





# {} helper functions

def extract_rows_from_db(surveyformdata_uid):
    try:
        # Query the survey_form_data table using the given surveyformdata_uid
        plot_detail = survey_form_data.query.filter(survey_form_data.surveyformdata_uid == surveyformdata_uid).first()

        if plot_detail:
            # Return the data as a dictionary
            return {
                'surveyformdata_uid': surveyformdata_uid,
                'user_name': plot_detail.user_name,
                'node_name': plot_detail.node_name,
                'sector_no': plot_detail.sector_no,
                'block_name': plot_detail.block_name,
                'plot_name': plot_detail.plot_name,
                'plot_status': plot_detail.plot_status,
                'allotment_date': plot_detail.allotment_date.strftime('%Y-%m-%d'),  # Formatting the date
                'original_allottee': plot_detail.original_allottee,
                'area': plot_detail.area,
                'use_of_plot': plot_detail.use_of_plot,
                'FSI' : plot_detail.FSI,
                'term_of_lease' : plot_detail.term_of_lease,
                'rate': plot_detail.rate,
                'ownerNtransferDate':plot_detail.ownerNtransferDate,
                'surveyor_remarks': plot_detail.surveyor_remarks,
                'front_photo': plot_detail.front_photo,
                'left_photo': plot_detail.left_photo,
                'back_photo': plot_detail.back_photo,
                'right_photo': plot_detail.right_photo,
                'plot_sketch': plot_detail.plot_sketch,
                'entry_date_created': plot_detail.entry_date_created.strftime('%Y-%m-%d %H:%M:%S'),  # Formatting the datetime
                'surveyform_status': plot_detail.surveyform_status,
                'is_qc_done':plot_detail.is_qc_done,
                'is_validation_done':plot_detail.is_validation_done,
                'validator_remarks':plot_detail.validator_remarks
            }
        else:
            # If no record is found, return an error message
            return {'error': 'Plot details not found'}
    
    except Exception as e:
        # Handle any exceptions that might occur during the query
        return {'error': f'An error occurred: {str(e)}'}



def query_plot_details(role, button, sector):
    query = survey_form_data.query
    data = request.get_json()
    selected_button = data.get('selectedButton')  # Button: 'default', 'accept', 'reject', etc.
    #date_filter = data.get('dateFilter')         # Month-Year filter if applicable
    role = request.args.get('role')              # Assuming the role is passed as a query param
    sector = request.args.get('sector')   
    role='qc'

   # Apply filtering based on role and button
    if role == 'qc':
        if selected_button == "default":
            query = query.filter_by(is_qc_done='0', sector_no=sector)
        elif selected_button == "accept":
            query = query.filter_by(is_qc_done='1', sector_no=sector)
        elif selected_button == "reject":
            query = query.filter_by(is_validation_done='2', sector_no=sector)

    elif role == 'validator':
        if selected_button == "default":
            query = query.filter_by(is_validation_done='0', sector_no=sector)
        elif selected_button == "accept":
            query = query.filter_by(is_validation_done='1', sector_no=sector)
        elif selected_button == "reject":
            query = query.filter_by(is_validation_done='2', sector_no=sector)

    elif role == 'admin':
        if selected_button == "complete":
            query = query.filter_by(surveyform_status='1', sector_no=sector)
        elif selected_button == "incomplete":
            query = query.filter_by(surveyform_status='0', sector_no=sector)
        elif selected_button == "pending(QC end)":
            query = query.filter_by(is_qc_done='0', sector_no=sector)
        elif selected_button == "pending(Validator end)":
            query = query.filter_by(is_validation_done='0', sector_no=sector)

    # If no button is selected (clear filter), fetch all data
    if not selected_button:
        query = survey_form_data.query.filter_by(sector_no=sector)

    results = query.all()
    return jsonify([result.to_dict() for result in results])
# {}






#----------------------------------------------
                # Dashboard code here 
#----------------------------------------------







# {}
# user info editsection trial code --------------------------------------------------------------------------------------------




# 
# Route to fetch filtered dropdown data
@app.route('/get_editUser_values', methods=['GET'])
def get_editUser_values():
    # Get filter parameters from request arguments
    name = request.args.get('name')
    phone_no = request.args.get('phone_no')
    role = request.args.get('role')

    # Query the database and filter based on the parameters
    query = user_info.query

    if name:
        query = query.filter_by(name=name)
    if phone_no:
        query = query.filter_by(phone_no=phone_no)
    if role:
        query = query.filter_by(role=role)

    userEdit = query.all()

    # Prepare the response data with unique values
    data = {
        'name': list(set(item.name for item in userEdit if item.name)),
        'phone_no': list(set(item.phone_no for item in userEdit if item.phone_no)),
        'role': list(set(item.role for item in userEdit if item.role))
    }

    print("Filtered data being sent as JSON response:")
    print(data)

    return jsonify(data)
# 





@app.route('/userEdit_values_admin_panel', methods=['GET'])
def userEdit_values_admin_panel():
    # the thing doesnt ends here since we are using soft delte with the help of the another column as is_dropdownvalues_active so when the page loads the filtering logic where we have put we also have to consider a condition that to filter the data where is_dropdownvalues_active is 1
    # dont use all instead add a condition that is_dropdownvalues_active should be 1 where 1 means active
    
    # Query all the values from the DropdownValues table
    userEdit = user_info.query.filter_by(value_softdel=1).all()


    # Prepare the data to be returned as JSON
    data = {
        'userinfo_uid': [item.userinfo_uid for item in userEdit],
        'name': [item.name for item in userEdit],
        'phone_no': [item.phone_no for item in userEdit],
        'role': [item.role for item in userEdit],
        'value_softdel':[item.value_softdel for item in userEdit]
    }

    # Print the data before calling jsonify
    print("Data being sent as JSON response: data")
    print(data)  # This prints the Python dictionary  
    return jsonify(data)  # This sends the data as a JSON response



    
# Route to update data in the database
@app.route('/update_userEdit_values', methods=['POST'])
def update_userEdit():
    # Get the updated data from the frontend
    updated_data = request.get_json()  # Get the JSON data sent from frontend
    
    print("rolcheckcheckcheckcheckcheckcheckcheckcheckcheckcheckcheckcheckcheckcheckcheckcheckcheckcheckcheckcheckcheckcheckcheckcheckcheckcheck")
    print(updated_data)
    print("checkcheckcheckcheckcheckcheckcheckcheckcheckcheckcheckcheckcheckcheckcheckcheckcheckcheckcheckcheckcheckcheckcheckcheckcheckcheckcheck")
    # Extract values from the received JSON
    name = updated_data.get('column1')
    phone_no = updated_data.get('column2')
    role = updated_data.get('column3')
    userinfo_uid = updated_data.get('uid')
    #first take the uid that we are getting from the requrest
    # then go in the dropdownvalue_uid column match this uid if match found then go in the is_dropdownvalues_active and set this value to 0 
    # so basically we are soft deleleting the entry but the data persists in the database table
    
    print("these si the uid")
    print(userinfo_uid)


    print("these are the values we got from the updated drop down values")
    print(name,phone_no,role)
    # Find the record in the database to update (example: updating the first record)
    record = user_info.query.filter_by(userinfo_uid=userinfo_uid).first() # You can modify this to update a specific record

    # Update the fields
    if record:
        record.name = name
        record.phone_no = phone_no
        record.role = role

        # Commit the changes to the database
        db.session.commit()

        # Return success response
        return jsonify({'success': True})

    return jsonify({'success': False, 'message': 'Record not found'})
    


# Define the route to handle the delete request
@app.route('/delete_user_values', methods=['POST'])
def delete_user_values():
    # Get the JSON data sent from the front end
    request_data = request.get_json()
    
    # Extract the uid from the request data
    uid_to_delete = request_data.get('uid')
    
    # Print the UID to the console
    print("Received UID to delete:", uid_to_delete)

    record = user_info.query.filter_by(userinfo_uid=uid_to_delete).first()
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

# {}------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)

