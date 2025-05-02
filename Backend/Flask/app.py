import yaml
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

# Flask-App initialisieren
app = Flask(__name__)

# Update CORS configuration with all necessary settings
# Update CORS configuration with all necessary settings
CORS(app, resources={
    r"/*": {
        "origins": ["http://192.168.178.104:8080", "http://localhost:8080"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
        "supports_credentials": True,
        "expose_headers": ["Content-Range", "X-Content-Range"]
    }
})

# Enable CORS pre-flight requests
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin', '*')
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

app.after_request(add_cors_headers)

# Lade Datenbankkonfiguration aus der YAML-Datei
with open('db.yaml', 'r') as file:
    db_config = yaml.safe_load(file)

# Datenbankkonfiguration setzen
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_config['mysql_user']}:{db_config['mysql_password']}@{db_config['mysql_host']}/{db_config['mysql_db']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQLAlchemy-Instanz erstellen
db = SQLAlchemy(app)

# JWT-Konfiguration
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'super-secret-key')
jwt = JWTManager(app)

# Datenbankmodelle definieren
class User(db.Model):
    """Benutzertabelle"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phonenumber = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('kunde', 'admin'), default='kunde')

class Barber(db.Model):
    """Friseurtabelle"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    is_open_tuesday = db.Column(db.Boolean, default=True, nullable=False)
    is_open_thursday = db.Column(db.Boolean, default=True, nullable=False)
    work_start = db.Column(db.Time, default=datetime.strptime("09:00:00", "%H:%M:%S").time(), nullable=False)
    work_end = db.Column(db.Time, default=datetime.strptime("19:00:00", "%H:%M:%S").time(), nullable=False)

class Appointment(db.Model):
    """Termintabelle"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    barber_id = db.Column(db.Integer, db.ForeignKey('barber.id'), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.Enum('gebucht', 'storniert', 'verschoben', 'abgeschlossen'), default='gebucht')
    
    # Add relationships
    barber = db.relationship('Barber', backref=db.backref('appointments', lazy=True))
    user = db.relationship('User', backref=db.backref('appointments', lazy=True))

# Holt die Daten des eingeloggten Nutzers
@app.route('/me', methods=['GET'])
@jwt_required()
def me():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "phonenumber": user.phonenumber,
        "role": user.role
    }), 200

# Neuer Login-Endpunkt mit JWT
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token}), 200

# Beispiel eines geschützten Endpunkts
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    return jsonify({"message": f"Hello user {current_user_id}, you have access to this protected endpoint!"}), 200

# Alle Benutzer abrufen
@app.route('/users', methods=['GET'])
def get_users():
    """Gibt eine Liste aller Benutzer zurück"""
    users = User.query.all()
    user_list = [{"id": user.id, "name": user.name, "email": user.email, "phonenumber": user.phonenumber, "role": user.role} for user in users]
    return jsonify(user_list), 200

# Benutzer registrieren
@app.route('/register', methods=['POST'])
def register():
    """Registriert einen neuen Benutzer"""
    data = request.json
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = User(name=data['name'], email=data['email'], phonenumber=data['phonenumber'], password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User successfully registered"}), 201

# Termin buchen
@app.route('/book_appointment', methods=['POST'])
def book_appointment():
    """Bucht einen Termin für einen Benutzer"""
    data = request.json
    user = User.query.get(data['user_id'])
    barber = Barber.query.get(data['barber_id'])

    if not user or not barber:
        return jsonify({"error": "User or Barber not found"}), 404

    appointment_date = datetime.strptime(data['appointment_date'], "%Y-%m-%d").date()
    appointment_time = datetime.strptime(data['appointment_time'], "%H:%M:%S").time()

    if appointment_date < datetime.today().date():
        return jsonify({"error": "Appointments in the past are not allowed"}), 400

    if appointment_date.weekday() == 1 and not barber.is_open_tuesday:
        return jsonify({"error": "Barber is not available on Tuesday"}), 400
    if appointment_date.weekday() == 3 and not barber.is_open_thursday:
        return jsonify({"error": "Barber is not available on Thursday"}), 400

    if not (barber.work_start <= appointment_time <= barber.work_end):
        return jsonify({"error": "Appointment time is outside barber's working hours"}), 400

    existing_appointment = Appointment.query.filter(
        Appointment.user_id == user.id,
        Appointment.status == 'gebucht',
        Appointment.appointment_date >= datetime.today().date()
    ).first()
    if existing_appointment:
        return jsonify({"error": "You already have an active appointment"}), 400

    overlapping_appointment = Appointment.query.filter_by(barber_id=barber.id, appointment_date=appointment_date, appointment_time=appointment_time, status='gebucht').first()
    if overlapping_appointment:
        return jsonify({"error": "This appointment slot is already booked"}), 400

    new_appointment = Appointment(user_id=user.id, barber_id=barber.id, appointment_date=appointment_date, appointment_time=appointment_time)
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({"message": "Appointment booked successfully"}), 201

@app.route('/appointments', methods=['GET'])
def get_appointments():
    """Gibt alle gebuchten Termine zurück"""
    appointments = Appointment.query.filter_by(status='gebucht').all()
    appointment_list = [
        {
            "id": appointment.id,
            "barber_id": appointment.barber_id,
            "barber_name": appointment.barber.name,
            "appointment_date": appointment.appointment_date.strftime("%Y-%m-%d"),
            "appointment_time": appointment.appointment_time.strftime("%H:%M:%S"),
        }
        for appointment in appointments
    ]
    return jsonify(appointment_list), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
