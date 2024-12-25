from multiprocessing import connection
from flask import Flask, render_template, request, redirect, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
#from sqlalchemy import create_engine
from datetime import datetime
import os
import common_functions

app = Flask(__name__)

# Update the database URI to MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Akhatri%402023@localhost/plot_details_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable track modifications to save memory
app.config['UPLOAD_FOLDER'] = './uploads'  # Folder to save uploaded files
db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('output_table.html')


@app.route('/survey_output_form')
def survey_output_form():
    return render_template('survey_output_form.html')


@app.route('/qc_form')
def qc_form():
    return render_template('qc_form.html')

@app.route('/validator_form_accept_reject')
def validator_form_accept_reject():
    return render_template('validator_form_accept_reject.html')

# Model for storing plot details
class survey_form_data(db.Model):
    surveyformdata_uid = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(200), nullable=False)
    node_name = db.Column(db.String(100), nullable=False)
    sector_no = db.Column(db.String(100), nullable=False)
    block_name = db.Column(db.String(100), nullable=False)
    plot_name = db.Column(db.String(100), nullable=False)
    allotment_date = db.Column(db.Date, nullable=False)
    original_allottee = db.Column(db.String(200), nullable=False)
    area = db.Column(db.Float, nullable=False)
    use_of_plot = db.Column(db.String(100), nullable=False)
    rate = db.Column(db.Float, nullable=False)
    t1owner_name = db.Column(db.String(200), nullable=False)
    t1transfer_date = db.Column(db.Date, nullable=False)
    t2owner_name = db.Column(db.String(200), nullable=False)
    t2transfer_date = db.Column(db.Date, nullable=False)
    t3owner_name = db.Column(db.String(200), nullable=False)
    t3transfer_date = db.Column(db.Date, nullable=False)
    t4owner_name = db.Column(db.String(200), nullable=False)
    t4transfer_date = db.Column(db.Date, nullable=False)
    t5owner_name = db.Column(db.String(200), nullable=False)
    t5transfer_date = db.Column(db.Date, nullable=False)
    t6owner_name = db.Column(db.String(200), nullable=False)
    t6transfer_date = db.Column(db.Date, nullable=False)
    t7owner_name = db.Column(db.String(200), nullable=False)
    t7transfer_date = db.Column(db.Date, nullable=False)
    t8owner_name = db.Column(db.String(200), nullable=False)
    t8transfer_date = db.Column(db.Date, nullable=False)
    t9owner_name = db.Column(db.String(200), nullable=False)
    t9transfer_date = db.Column(db.Date, nullable=False)
    t10owner_name = db.Column(db.String(200), nullable=False)
    t10transfer_date = db.Column(db.Date, nullable=False)
    t11owner_name = db.Column(db.String(200), nullable=False)
    t11transfer_date = db.Column(db.Date, nullable=False)
    t12owner_name = db.Column(db.String(200), nullable=False)
    t12transfer_date = db.Column(db.Date, nullable=False)
    surveyor_remarks = db.Column(db.Text, nullable=True)
    front_photo = db.Column(db.String(200), nullable=False)
    left_photo = db.Column(db.String(200), nullable=False)
    back_photo = db.Column(db.String(200), nullable=False)
    right_photo = db.Column(db.String(200), nullable=False)
    plot_sketch = db.Column(db.String(200), nullable=False)
    entry_date_created = db.Column(db.DateTime, default=datetime.utcnow)
    surveyform_status = db.Column(db.String(200), nullable=False)
    is_qc_done = db.Column(db.String(200), nullable=False)
    is_validation_done = db.Column(db.String(200), nullable=False)
    validator_remarks = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<Plot {self.id}>"



@app.route('/output_table', methods=['POST', 'GET'])
def output_table():

    print("flask route")
    # Query the required columns from the survey_form_data table
    plots = survey_form_data.query.with_entities(
        survey_form_data.node_name,
        survey_form_data.sector_no,
        survey_form_data.block_name,
        survey_form_data.plot_name,
        survey_form_data.entry_date_created,
        survey_form_data.user_name.label('surveyor_name'),  # Assuming 'user_name' is the surveyor's name
        survey_form_data.surveyformdata_uid,
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
            'date_uploaded': plot.entry_date_created.strftime('%Y-%m-%d %H:%M:%S'),
            'surveyor_name': plot.surveyor_name,
            'surveyformdata_uid': plot.surveyformdata_uid,
            'surveyform_status': plot.surveyform_status,
            'is_qc_done': plot.is_qc_done,
            'is_validation_done':plot.is_validation_done,
            'validator_remarks':plot.validator_remarks
        }
        output.append(plot_data)


    print("this is the output table data")
    print(output)

    return jsonify(output)


# json_data = {}

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





@app.route('/get_outputform_data')
def get_outputform_data():
    global json_data
    print('this is the filtered df for the given form id', json_data)

    # Convert DataFrame to JSON
    return jsonify(json_data)


# Function to extract data from the survey_form_data table based on surveyformdata_uid
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
                'allotment_date': plot_detail.allotment_date.strftime('%Y-%m-%d'),  # Formatting the date
                'original_allottee': plot_detail.original_allottee,
                'area': plot_detail.area,
                'use_of_plot': plot_detail.use_of_plot,
                'rate': plot_detail.rate,
                't1owner_name': plot_detail.t1owner_name,
                't1transfer_date': plot_detail.t1transfer_date.strftime('%Y-%m-%d'),
                't2owner_name': plot_detail.t2owner_name,
                't2transfer_date': plot_detail.t2transfer_date.strftime('%Y-%m-%d'),
                't3owner_name': plot_detail.t3owner_name,
                't3transfer_date': plot_detail.t3transfer_date.strftime('%Y-%m-%d'),
                't4owner_name': plot_detail.t4owner_name,
                't4transfer_date': plot_detail.t4transfer_date.strftime('%Y-%m-%d'),
                't5owner_name': plot_detail.t5owner_name,
                't5transfer_date': plot_detail.t5transfer_date.strftime('%Y-%m-%d'),
                't6owner_name': plot_detail.t6owner_name,
                't6transfer_date': plot_detail.t6transfer_date.strftime('%Y-%m-%d'),
                't7owner_name': plot_detail.t7owner_name,
                't7transfer_date': plot_detail.t7transfer_date.strftime('%Y-%m-%d'),
                't8owner_name': plot_detail.t8owner_name,
                't8transfer_date': plot_detail.t8transfer_date.strftime('%Y-%m-%d'),
                't9owner_name': plot_detail.t9owner_name,
                't9transfer_date': plot_detail.t9transfer_date.strftime('%Y-%m-%d'),
                't10owner_name': plot_detail.t10owner_name,
                't10transfer_date': plot_detail.t10transfer_date.strftime('%Y-%m-%d'),
                't11owner_name': plot_detail.t11owner_name,
                't11transfer_date': plot_detail.t11transfer_date.strftime('%Y-%m-%d'),
                't12owner_name': plot_detail.t12owner_name,
                't12transfer_date': plot_detail.t12transfer_date.strftime('%Y-%m-%d'),
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

@app.route("/editByQC",methods=['GET'])
def editByQC():
    return render_template('editByQC.html')

# Example route to query plot details
@app.route('/query_plots', methods=['POST'])
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






@app.route('/delete_values', methods=['POST', 'GET'])
def delete_values():
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



if __name__ == '__main__':
    app.run(debug=True)