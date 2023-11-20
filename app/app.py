from flask import Flask, render_template, request,Response,jsonify, redirect, url_for,flash, session
import os
from predictions import prediction
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import pdfencrypt
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from datetime import timedelta

import smtplib

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime



app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds=2)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'  # Use your database file name
db = SQLAlchemy(app)

# Define a folder to store uploaded images
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

# Define User and Diagnosis models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Diagnosis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('diagnoses', lazy=True))
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    diagnosed_disease = db.Column(db.String(200))
    symptoms = db.Column(db.String(500))
    causes = db.Column(db.String(500))
    precautions = db.Column(db.String(500))
    medications = db.Column(db.String(500))

# Define a Feedback model for the database
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    feedback = db.Column(db.String(500), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Define routes and functions for each page
@app.route('/')
def home():
    return render_template('home.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Logged in successfully.", "success")
            return redirect(url_for("diagnosis"))
        else:
            flash("Login failed. Check your credentials.", "danger")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        # Check if the password and confirm password match
        if password != confirm_password:
            flash("Password and Confirm Password do not match.", "danger")
            return redirect(url_for("signup"))

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists. Please choose a different one.", "danger")
            return redirect(url_for("signup"))

        # Hash the password before storing it in the database
        hashed_password = generate_password_hash(password, method="sha256")

        # Create a new user
        user = User(name=name, username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully. Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route('/diagnosis', methods=['GET', 'POST'])
@login_required
def diagnosis():
    if request.method == 'POST':
        # Handle form submission and prediction here
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']
        height = request.form['height']
        weight = request.form['weight']
        medical_history = request.form['medical_history']

        # Store the email in the session
        session['user_email'] = email  # Store it in the session
        
        global patient_info
        patient_info = {
        'name' : name,
        'email': email,
        'age': age,
        'height':height,
        'weight':weight,
        'medical_history':medical_history
        
        }
        
        # Handle image upload
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                # Save the uploaded image
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
                image.save(image_path)
                # Perform prediction on the image and generate a diagnosis report
                # Replace the following lines with your prediction and report generation logic
                disease,symptoms,causes,precautions,medications = prediction(image_path)
                diagnosed_disease = disease
                symptoms = symptoms
                causes = causes
                precautions = precautions
                medications =medications

                global diagnosis_info
                diagnosis_info = {
                    'diagnosed_disease': diagnosed_disease,
                    'symptoms': symptoms,
                    'causes': causes,
                    'precautions': precautions,
                    'medications': medications
                }

                diagnosis = Diagnosis(user_id=current_user.id, diagnosed_disease=disease, symptoms=symptoms, causes=causes,
                                  precautions=precautions, medications=medications)
                db.session.add(diagnosis)
                db.session.commit()
                # Redirect to the result page with the diagnosis information
                return render_template('result.html', name=name, email=email, age=age, height=height,
                                       weight=weight, medical_history=medical_history, diagnosed_disease=diagnosed_disease,
                                       symptoms=symptoms, causes=causes, precautions=precautions, medications=medications)

    return render_template('diagnosis.html')


from reportlab.lib.pagesizes import letter
from reportlab.lib import pdfencrypt
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

def generate_pdf_report(patient_info, diagnosis_info):
    # Create a BytesIO object to store the PDF data
    buffer = BytesIO()
    
    # Create a PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Register a custom font if needed
    # pdfmetrics.registerFont(TTFont('CustomFont', 'custom_font.ttf'))

    # Define the styles for the PDF content
    styles = getSampleStyleSheet()
    normal_style = styles['Normal']
    heading_style1 = styles['Heading1']
    heading_style2 = styles['Heading2']
    
    # Create the content for the PDF
    content = []
    
    # Add patient's details
    patient_details = [
        Paragraph("Patient's Details:", heading_style1),
        Paragraph(f"Name: {patient_info['name']}", normal_style),
        Paragraph(f"Email: {patient_info['email']}", normal_style),
        Paragraph(f"Age: {patient_info['age']} years", normal_style),
        Paragraph(f"Height: {patient_info['height']} cm", normal_style),
        Paragraph(f"Weight: {patient_info['weight']} kg", normal_style),
        Paragraph(f"Previous Medical History: {patient_info['medical_history']}", normal_style)
    ]
    
    content.extend(patient_details)
    
    # Add diagnosis details
    diagnosis_details = [
        Paragraph("Diagnosis Details:", heading_style1),
        Paragraph("Diagnosed Skin Lesion: ",heading_style2),
        Paragraph(f"{diagnosis_info['diagnosed_disease']}", normal_style)
    ]
    
    # Split the long text into paragraphs and add to content
    symptoms = diagnosis_info['symptoms'].split('\n')
    causes = diagnosis_info['causes'].split('\n')
    precautions = diagnosis_info['precautions'].split('\n')
    medications = diagnosis_info['medications'].split('\n')
    
    # Add the symptoms, causes, precautions, and medications to content
    diagnosis_details.append(Paragraph(f"Symptoms:",heading_style2))
    for text in symptoms:
        diagnosis_details.append(Paragraph(f"{text}", normal_style))
    diagnosis_details.append(Paragraph(f"Causes:",heading_style2))
    for text in causes:
        diagnosis_details.append(Paragraph(f"{text}", normal_style))
    diagnosis_details.append(Paragraph(f"Precautions:",heading_style2))
    for text in precautions:
        diagnosis_details.append(Paragraph(f"{text}", normal_style))
    diagnosis_details.append(Paragraph(f"Medications:",heading_style2))
    for text in medications:
        diagnosis_details.append(Paragraph(f"{text}", normal_style))
    
    content.extend(diagnosis_details)
    
    # Build the PDF document with the content
    doc.build(content)

    # Reset the buffer position to the start of the BytesIO object
    buffer.seek(0)

    return buffer



@app.route('/result')
def result():
    # Display the diagnosis result and provide options for download and email
    return render_template('result.html')


@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        recipient_email = session.get('user_email')

        EMAIL_ADDRESS = os.environ.get('USER_EMAIL')
        EMAIL_PASSWORD = os.environ.get('USER_PASS')

        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = '@SkinAI'  # Replace with your email
        msg['To'] = recipient_email
        msg['Subject'] = 'Diagnosis Report'

        # Email body
        body = 'Here is your diagnosis report.'
        msg.attach(MIMEText(body, 'plain'))


        pdf_buffer = generate_pdf_report(patient_info,diagnosis_info)
        pdf_attachment = MIMEApplication(pdf_buffer.read(), _subtype='pdf')
        pdf_buffer.seek(0)
        pdf_attachment.add_header('Content-Disposition', f'attachment; filename=diagnosis_report.pdf')
        msg.attach(pdf_attachment)

        # Configure the SMTP server and send the email
        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)  # Replace with your email provider's SMTP server
        smtp_server.starttls()
        smtp_server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)  # Replace with your email and password
        smtp_server.sendmail(EMAIL_ADDRESS, recipient_email, msg.as_string())
        smtp_server.quit()

        return jsonify({'message': 'Email sent successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/generate_pdf_report')
def generate_and_download_pdf():
    # Generate the PDF report
    pdf_buffer = generate_pdf_report(patient_info, diagnosis_info)

    # Create a Flask response with the PDF data and specify content type
    response = Response(pdf_buffer.read(), content_type='application/pdf')

    # Set content disposition to force browser to download the PDF
    response.headers['Content-Disposition'] = 'attachment; filename=diagnosis_report.pdf'

    return response

@app.route('/user_history')
@login_required
def user_history():
    user_diagnoses = Diagnosis.query.filter_by(user_id=current_user.id).order_by(Diagnosis.date.desc()).all()
    return render_template('user_history.html', user_diagnoses=user_diagnoses)


@app.route('/admin')
# @login_required  # Add authentication checks for admin access
def admin_panel():
    login_users = User.query.all()
    # # Check if the current user has admin privileges
    # if not current_user.is_admin:  # You need to define 'is_admin' attribute in your User model
    #     return "Access denied. You are not authorized to access the admin panel."
    return render_template('admin_panel.html',login_users=login_users)

@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user_to_delete = User.query.get(user_id)
    if user_to_delete:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User deleted successfully.", "success")
    else:
        flash("User not found.", "danger")
    return redirect(url_for('admin_panel'))


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        feedback = request.form['feedback']

        if not name or not email or not feedback:
            flash('Please fill in all fields', 'error')
        else:
            new_feedback = Feedback(name=name, email=email, feedback=feedback)
            db.session.add(new_feedback)
            db.session.commit()
            flash('Feedback submitted successfully!', 'success')

        flash('Feedback submitted successfully!', 'success')
        return redirect(url_for('feedback'))

    return render_template('feedback.html')

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    with app.app_context():
        db.create_all()
    app.run(debug=True)