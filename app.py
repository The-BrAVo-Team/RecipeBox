from flask import Flask, send_from_directory, render_template, redirect, url_for, request, flash
from flask_wtf import FlaskForm
from flask import request, jsonify
from flask_migrate import Migrate
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from cryptography.fernet import Fernet
from flask_login import current_user, login_required
from flask_login import login_user, login_manager
from flask_login import LoginManager
import os

app = Flask(__name__, static_folder='client/build', template_folder= "templates")
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
cipher_suite = Fernet(Fernet.generate_key())

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(500), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    data = db.Column(db.Text, nullable=True)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
User.notes = db.relationship('Note', backref='user', lazy=True)

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
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
    form = LoginForm()
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
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

if __name__ == '__main__':
    app.run(debug=True, port = 3000)