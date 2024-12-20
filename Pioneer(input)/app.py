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



@app.route('/')
def index():
    return render_template('Survey_form.html')



# Model for storing plot details
class plot_details(db.Model):
    plotdetails_uid = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(200), nullable=True)
    node_name = db.Column(db.String(100), nullable=True)
    sector_no = db.Column(db.String(100), nullable=True)
    block_name = db.Column(db.String(100), nullable=True)
    plot_name = db.Column(db.String(100), nullable=True)
    allotment_date = db.Column(db.Date, nullable=True)
    original_allottee = db.Column(db.String(200), nullable=True)
    area = db.Column(db.Float, nullable=True)
    use_of_plot = db.Column(db.String(100), nullable=True)
    rate = db.Column(db.Float, nullable=True)
    t2owner_name = db.Column(db.String(200), nullable=True)
    t2transfer_date = db.Column(db.Date, nullable=True)
    t3owner_name = db.Column(db.String(200), nullable=True)
    t3transfer_date = db.Column(db.Date, nullable=True)
    t4owner_name = db.Column(db.String(200), nullable=True)
    t4transfer_date = db.Column(db.Date, nullable=True)
    t5owner_name = db.Column(db.String(200), nullable=True)
    t5transfer_date = db.Column(db.Date, nullable=True)
    t6owner_name = db.Column(db.String(200), nullable=True)
    t6transfer_date = db.Column(db.Date, nullable=True)
    t7owner_name = db.Column(db.String(200), nullable=True)
    t7transfer_date = db.Column(db.Date, nullable=True)
    t8owner_name = db.Column(db.String(200), nullable=True)
    t8transfer_date = db.Column(db.Date, nullable=True)
    t9owner_name = db.Column(db.String(200), nullable=True)
    t9transfer_date = db.Column(db.Date, nullable=True)
    t10owner_name = db.Column(db.String(200), nullable=True)
    t10transfer_date = db.Column(db.Date, nullable=True)
    t11owner_name = db.Column(db.String(200), nullable=True)
    t11transfer_date = db.Column(db.Date, nullable=True)
    t12owner_name = db.Column(db.String(200), nullable=True)
    t12transfer_date = db.Column(db.Date, nullable=True)
    remarks = db.Column(db.Text, nullable=True)
    entry_date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Plot {self.plotdetails_uid}>"



# Home route
@app.route('/submit_form_data', methods=['POST', 'GET'])
def submit_form_data():
    if request.method == 'POST':
        try:
            # Log: Start of form submission
            print("Start processing form submission...")

            # Debug: Print form data
            print("This is the form data received:")
            for key, value in request.form.items():
                print(f"{key}: {value}")
            print("Full form data as a dictionary:", request.form.to_dict())

            # Extract form data
            user_name = request.form.get('user_name')
            node_name = request.form.get('node_name')
            sector_no = request.form.get('sector_no')
            block_name = request.form.get('block_name')
            plot_name = request.form.get('plot_name')
            allotment_date = "2024-11-20"
            original_allottee = request.form.get('original_allottee')
            area = 9.5  # Placeholder; ensure this matches your database schema
            use_of_plot = request.form.get('use_of_plot')
            rate = 9.5  # Placeholder; ensure this matches your database schema

            # Extract transfer details (log every step for clarity)


            # Add similar logging for other transfer details...
            t2owner_name = request.form.get('t2owner_name')
            t2transfer_date = "2024-11-20"
            # ...
            remarks = request.form.get('remarks')

            # Log extracted data
            print("Extracted data:")
            print(f"user_name: {user_name}, node_name: {node_name}, sector_no: {sector_no}")
            print(f"block_name: {block_name}, plot_name: {plot_name}, allotment_date: {allotment_date}")
            print(f"original_allottee: {original_allottee}, area: {area}, use_of_plot: {use_of_plot}")
            print(f"rate: {rate}, t2owner_name: {t2owner_name}, t2transfer_date: {t2transfer_date}")
            print(f"remarks: {remarks}")



            # Create a new plot_details record
            new_plot = plot_details(
                user_name=user_name, node_name=node_name, sector_no=sector_no, block_name=block_name,
                plot_name=plot_name, allotment_date=allotment_date, original_allottee=original_allottee,
                area=area, use_of_plot=use_of_plot, rate=rate,
                t2owner_name=t2owner_name, t2transfer_date=t2transfer_date,
                # Add all other transfer details...
                remarks=remarks
            )


            # Debug: Verify the object before adding it to the session
            print("New plot_details object created:", new_plot)

            # Add the record to the database
            db.session.add(new_plot)
            print("Added new_plot to the session.")

            # Commit to the database
            db.session.commit()
            print("Database commit successful.")

            return redirect('/')
        except Exception as e:
            # Log the exact error message for debugging
            print("Error occurred during form submission:")
            print(str(e))
            return f"There was an issue submitting the form: {str(e)}"
    else:
        # Log: GET request handling
        print("Rendering the index.html template.")
        return render_template('index.html')






# Define the model for dropdown_values table
class dropdown_values(db.Model):
    dropdownvalues_uid = db.Column(db.Integer, primary_key=True)
    node_name = db.Column(db.String(255))
    sector = db.Column(db.String(255))
    block_name = db.Column(db.String(255))
    plot_no = db.Column(db.String(255))

    def __repr__(self):
        return f'<DropdownValues {self.node_name}, {self.sector}, {self.block_name}, {self.plot_no}>'



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

    print("Filtered data being sent as JSON response:")
    print(data)

    return jsonify(data)






if __name__ == '__main__':
    app.run(debug=True)
