# image upload handling  ..... image is getting printed in the browser now make it store in such a way that it takes ...
# images and store it in images folder and the name of the file along with the extension should be store in database 



from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
# Update the database URI to MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Akhatri%402023@localhost/plot_details'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable track modifications to save memory
app.config['UPLOAD_FOLDER'] = './uploads'  # Folder to save uploaded files
db = SQLAlchemy(app)


# {}
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




@app.route('/')
def index():
    return render_template('loginForm.html')





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
    ownerNtransferDate = db.Column(db.String(10000), nullable=True)
    remarks = db.Column(db.Text, nullable=True)
    entry_date_created = db.Column(db.DateTime, default=datetime.utcnow)
    front_photo =  db.Column(db.String(500), nullable=True)
    left_photo =  db.Column(db.String(1000), nullable=True)
    back_photo =  db.Column(db.String(1000), nullable=True)
    right_photo =  db.Column(db.String(1000), nullable=True)
    plot_sketch =  db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f"<Plot {self.plotdetails_uid}>"



# Home route
# Route to handle form submission
@app.route('/submit_form_data', methods=['POST', 'GET'])
def submit_form_data():
    if request.method == 'POST':
        try:
            # Extract form data
            user_name = request.form.get('user_name')
            node_name = request.form.get('node_name')
            sector_no = request.form.get('sector_no')
            block_name = request.form.get('block_name')
            plot_name = request.form.get('plot_name')
            allotment_date = request.form.get('allotment_date')
            original_allottee = request.form.get('original_allottee')
            area = request.form.get('area')
            use_of_plot = request.form.get('use_of_plot')
            rate = request.form.get('rate')
            ownerNtransferDate = request.form.get('ownerNtransferDate')
            remarks = request.form.get('remarks')

            # Process uploaded files
            front_photo = request.files.get('front_photo')
            left_photo = request.files.get('left_photo')
            back_photo = request.files.get('back_photo')
            right_photo = request.files.get('right_photo')
            plot_sketch = request.files.get('plot_sketch')

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

            # Create a new plot_details record
            new_plot = plot_details(
                user_name=user_name,
                node_name=node_name,
                sector_no=sector_no,
                block_name=block_name,
                plot_name=plot_name,
                allotment_date=allotment_date,
                original_allottee=original_allottee,
                area=area,
                use_of_plot=use_of_plot,
                rate=rate,
                ownerNtransferDate=ownerNtransferDate,
                remarks=remarks,
                front_photo=front_photo_filename,
                left_photo=left_photo_filename,
                back_photo=back_photo_filename,
                right_photo=right_photo_filename,
                plot_sketch=plot_sketch_filename
            )

            # Save to the database
            db.session.add(new_plot)
            db.session.commit()

            return redirect('/')
        except Exception as e:
            return f"There was an issue submitting the form: {str(e)}"
    else:
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

    # print("Filtered data being sent as JSON response:")
    # print(data)

    return jsonify(data)






if __name__ == '__main__':
    app.run(debug=True)
