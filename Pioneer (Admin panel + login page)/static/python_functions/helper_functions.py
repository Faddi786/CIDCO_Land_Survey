# Flask and Flask-SQLAlchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Datetime module for date formatting
from datetime import datetime

# Function to extract data from the survey_form_data table based on surveyformdata_uid
def extract_rows_from_db(survey_form_data,surveyformdata_uid):
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