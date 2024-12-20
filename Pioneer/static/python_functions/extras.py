



# Model for storing plot details
class plot_details(db.Model):
    plotdetails_uid = db.Column(db.Integer, primary_key=True)
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
    remarks = db.Column(db.Text, nullable=True)
    front_photo = db.Column(db.LargeBinary)
    left_photo = db.Column(db.LargeBinary)
    back_photo = db.Column(db.LargeBinary)
    right_photo = db.Column(db.LargeBinary)
    plot_sketch = db.Column(db.LargeBinary)
    entry_date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Plot {self.id}>"




# Home route
@app.route('/submit_form_data', methods=['POST', 'GET'])
def submit_form_data():
    if request.method == 'POST':
        print("This is the form data:")
        
        # Print the form fields
        for key, value in request.form.items():
            print(f"{key}: {value}")
        
        # Print the files
        for file_key, file in request.files.items():
            print(f"File - {file_key}: {file.filename}")
        
        # Optional: To print the entire form data as a dictionary
        print("Full form data:")
        print(request.form.to_dict())

        # Get form data
        user_name = request.form['user_name']
        node_name = request.form['node_name']
        sector_no = request.form['sector_no']
        block_name = request.form['block_name']
        plot_name = request.form['plot_name']
        allotment_date = request.form['allotment_date']
        original_allottee = request.form['original_allottee']
        area = "9.5"
        use_of_plot = request.form['use_of_plot']
        rate = "9.5"
        t1owner_name = request.form['t1owner_name']
        t1transfer_date = request.form['t1transfer_date']
        t2owner_name = request.form['t2owner_name']
        t2transfer_date = request.form['t2transfer_date']
        t3owner_name = request.form['t3owner_name']
        t3transfer_date = request.form['t3transfer_date']
        t4owner_name = request.form['t4owner_name']
        t4transfer_date = request.form['t4transfer_date']
        t5owner_name = request.form['t5owner_name']
        t5transfer_date = request.form['t5transfer_date']
        t6owner_name = request.form['t6owner_name']
        t6transfer_date = request.form['t6transfer_date']
        t7owner_name = request.form['t7owner_name']
        t7transfer_date = request.form['t7transfer_date']
        t8owner_name = request.form['t8owner_name']
        t8transfer_date = request.form['t8transfer_date']
        t9owner_name = request.form['t9owner_name']
        t9transfer_date = request.form['t9transfer_date']
        t10owner_name = request.form['t10owner_name']
        t10transfer_date = request.form['t10transfer_date']
        t11owner_name = request.form['t11owner_name']
        t11transfer_date = request.form['t11transfer_date']
        t12owner_name = request.form['t12owner_name']
        t12transfer_date = request.form['t12transfer_date']
        remarks = request.form['remarks']

        # Save uploaded photos
        photos_folder = 'static/uploads'
        os.makedirs(photos_folder, exist_ok=True)

        # front_photo_path = os.path.join(photos_folder, front_photo.filename)
        # left_photo_path = os.path.join(photos_folder, left_photo.filename)
        # back_photo_path = os.path.join(photos_folder, back_photo.filename)
        # right_photo_path = os.path.join(photos_folder, right_photo.filename)
        # plot_sketch_path = os.path.join(photos_folder, plot_sketch.filename)

        # Replace reading from request.files with dummy binary data for testing
        front_photo = b"Dummy binary data for front photo"
        left_photo = b"Dummy binary data for left photo"
        back_photo = b"Dummy binary data for back photo"
        right_photo = b"Dummy binary data for right photo"
        plot_sketch = b"Dummy binary data for plot sketch"


        # Define dummy filenames
        front_photo_path = os.path.join(photos_folder, "front_photo_dummy.jpg")
        left_photo_path = os.path.join(photos_folder, "left_photo_dummy.jpg")
        back_photo_path = os.path.join(photos_folder, "back_photo_dummy.jpg")
        right_photo_path = os.path.join(photos_folder, "right_photo_dummy.jpg")
        plot_sketch_path = os.path.join(photos_folder, "plot_sketch_dummy.jpg")


        # Write the dummy binary data to these files
        with open(front_photo_path, "wb") as f:
            f.write(front_photo)
        with open(left_photo_path, "wb") as f:
            f.write(left_photo)
        with open(back_photo_path, "wb") as f:
            f.write(back_photo)
        with open(right_photo_path, "wb") as f:
            f.write(right_photo)
        with open(plot_sketch_path, "wb") as f:
            f.write(plot_sketch)

        # Log the file paths
        print("Dummy files created:")
        print(f"Front photo: {front_photo_path}")
        print(f"Left photo: {left_photo_path}")
        print(f"Back photo: {back_photo_path}")
        print(f"Right photo: {right_photo_path}")
        print(f"Plot sketch: {plot_sketch_path}")


        # Save photos to the server
        # front_photo.save(front_photo_path)
        # left_photo.save(left_photo_path)
        # back_photo.save(back_photo_path)
        # right_photo.save(right_photo_path)
        # plot_sketch.save(plot_sketch_path)

        # Handle file uploads and convert to binary
        # front_photo = request.files['front_photo'].read()
        # left_photo = request.files['left_photo'].read()
        # back_photo = request.files['back_photo'].read()
        # right_photo = request.files['right_photo'].read()
        # plot_sketch = request.files['plot_sketch'].read()





        # Create a new plot_details record
        new_plot = plot_details(
            user_name=user_name, node_name=node_name, sector_no=sector_no, block_name=block_name,
            plot_name=plot_name, allotment_date=allotment_date, original_allottee=original_allottee,
            area=area, use_of_plot=use_of_plot, rate=rate,
            t1owner_name=t1owner_name, t1transfer_date=t1transfer_date,
            t2owner_name=t2owner_name, t2transfer_date=t2transfer_date,
            t3owner_name=t3owner_name, t3transfer_date=t3transfer_date,
            t4owner_name=t4owner_name, t4transfer_date=t4transfer_date,
            t5owner_name=t5owner_name, t5transfer_date=t5transfer_date,
            t6owner_name=t6owner_name, t6transfer_date=t6transfer_date,
            t7owner_name=t7owner_name, t7transfer_date=t7transfer_date,
            t8owner_name=t8owner_name, t8transfer_date=t8transfer_date,
            t9owner_name=t9owner_name, t9transfer_date=t9transfer_date,
            t10owner_name=t10owner_name, t10transfer_date=t10transfer_date,
            t11owner_name=t11owner_name, t11transfer_date=t11transfer_date,
            t12owner_name=t12owner_name, t12transfer_date=t12transfer_date,
            remarks=remarks, front_photo=front_photo, left_photo=left_photo, back_photo=back_photo,
            right_photo=right_photo, plot_sketch=plot_sketch
        )

        try:
            db.session.add(new_plot)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"There was an issue submitting the form: {e}"

    else:
        return render_template('index.html')
