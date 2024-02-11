from flask import Flask, send_from_directory, render_template, redirect, url_for, request
from wtforms.validators import ValidationError, StopValidation
from flask_wtf import FlaskForm
from flask import flash
from flask import request, jsonify
from flask_migrate import Migrate
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from cryptography.fernet import Fernet
from flask_login import current_user, login_required, login_user, LoginManager
from flask_login import logout_user
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import re

app = Flask(__name__, static_folder='client/build', template_folder= "templates")
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
cipher_suite = Fernet(Fernet.generate_key())

# Initialize Flask-Limiter
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(500), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    data = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    is_authenticated = db.Column(db.Boolean, default=True)
    is_anonymous = db.Column(db.Boolean, default=False)
    def get_id(self):
        return self.id

    

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
User.notes = db.relationship('Note', backref='user', lazy=True)

class PasswordComplexity(object):
    def __init__(self, message=None):
        if not message:
            message = u'Password must include at least one lowercase letter, one uppercase letter, one digit, and one special character.'
        self.message = message

    def __call__(self, form, field):
        password = field.data
        if not re.search("[a-z]", password):
            raise ValidationError(self.message)
        elif not re.search("[A-Z]", password):
            raise ValidationError(self.message)
        elif not re.search("[0-9]", password):
            raise ValidationError(self.message)
        elif not re.search("[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValidationError(self.message)

def check_common_password(form, field):
    common_passwords = ["password", "123456", "12345678"] # TODO: Add more common passwords to list
    if field.data in common_passwords:
        raise ValidationError("Please use a stronger, less common password.")

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message="Password must be at least 8 characters long."),
        PasswordComplexity(),
        check_common_password
    ])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class NoteForm(FlaskForm):
    note_title = StringField('Title', validators=[DataRequired()])
    note_content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Add Recipe')

def encrypt_data(data):
    return cipher_suite.encrypt(data.encode())

def decrypt_data(encrypted_data):
    return cipher_suite.decrypt(encrypted_data).decode()

with app.app_context():
    db.create_all()
    
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/login"



# Route to handle data requests and responses
@app.route('/api/data')
def get_data():
    return {'data': 'Your data here'}


#Flask route to send data to React
@app.route('/api/sendData')
def send_data():
    return jsonify({'message': 'Data sent successfully'})

@app.route('/')
def home():
    return render_template('landingpage.html')

@app.route('/register', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def register():
    username = request.form.get('username')

    if db.session.query(User).filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password, data='{}')
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute") # If error message does not display, add this to limit() => error_message="Too many attempts, please try again later."
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user) 
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please check username and password.', 'danger')
    return render_template('login.html', form=form)

@limiter.request_filter
def limiter_request_filter():
    # Return True if the limit should not be enforced for the request
    return request.method == 'OPTIONS'

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify(error="Rate limit exceeded. %s" % e.description, 429)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))  # This should redirect to the landing page


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    form = NoteForm()

    if request.method == 'POST' and form.validate_on_submit():
        new_note = Note(title=form.note_title.data, content=form.note_content.data, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()

    return render_template('dashboard.html', form=form, user=current_user)

# Add a new route to handle displaying notes
@app.route('/notes', methods=['GET', 'POST'])
def notes():
    form = NoteForm()
    user = User.query.filter_by(username=current_user.username).first()
    return render_template('notes.html', user=user, form=form)

# Serve React build files in Flask
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

# Flask error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


if __name__ == '__main__':
    app.run(debug=True, port = 3000, host = '0.0.0.0')