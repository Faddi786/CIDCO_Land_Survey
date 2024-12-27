# Flask and Flask-SQLAlchemy
from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy


# Datetime module for date formatting
from datetime import datetime

# Function to extract data from the survey_form_data table based on surveyformdata_uid

    


# def query_plot_details(role, button, sector):
#     query = survey_form_data.query
#     data = request.get_json()
#     selected_button = data.get('selectedButton')  # Button: 'default', 'accept', 'reject', etc.
#     #date_filter = data.get('dateFilter')         # Month-Year filter if applicable
#     role = request.args.get('role')              # Assuming the role is passed as a query param
#     sector = request.args.get('sector')   
#     role='qc'

#    # Apply filtering based on role and button
#     if role == 'qc':
#         if selected_button == "default":
#             query = query.filter_by(is_qc_done='0', sector_no=sector)
#         elif selected_button == "accept":
#             query = query.filter_by(is_qc_done='1', sector_no=sector)
#         elif selected_button == "reject":
#             query = query.filter_by(is_validation_done='2', sector_no=sector)

#     elif role == 'validator':
#         if selected_button == "default":
#             query = query.filter_by(is_validation_done='0', sector_no=sector)
#         elif selected_button == "accept":
#             query = query.filter_by(is_validation_done='1', sector_no=sector)
#         elif selected_button == "reject":
#             query = query.filter_by(is_validation_done='2', sector_no=sector)

#     elif role == 'admin':
#         if selected_button == "complete":
#             query = query.filter_by(surveyform_status='1', sector_no=sector)
#         elif selected_button == "incomplete":
#             query = query.filter_by(surveyform_status='0', sector_no=sector)
#         elif selected_button == "pending(QC end)":
#             query = query.filter_by(is_qc_done='0', sector_no=sector)
#         elif selected_button == "pending(Validator end)":
#             query = query.filter_by(is_validation_done='0', sector_no=sector)

#     # If no button is selected (clear filter), fetch all data
#     if not selected_button:
#         query = survey_form_data.query.filter_by(sector_no=sector)

#     results = query.all()
#     return jsonify([result.to_dict() for result in results])