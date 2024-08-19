# app.py
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Member Model
class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)

# Member Schema
class MemberSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Member
        sqla_session = db.session

# WorkoutSession Model
class WorkoutSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    member = db.relationship('Member', backref=db.backref('workout_sessions', lazy=True))

# WorkoutSession Schema
class WorkoutSessionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WorkoutSession
        sqla_session = db.session

# Initialize the database and create tables
with app.app_context():
    db.create_all()

# CRUD Operations for Members
@app.route('/members', methods=['POST'])
def add_member():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')

    if not all([name, email, phone]):
        return jsonify({"error": "Missing data"}), 400
    
    new_member = Member(name=name, email=email, phone=phone)
    db.session.add(new_member)
    db.session.commit()
    
    member_schema = MemberSchema()
    return member_schema.jsonify(new_member), 201

@app.route('/members', methods=['GET'])
def get_members():
    members = Member.query.all()
    member_schema = MemberSchema(many=True)
    return member_schema.jsonify(members), 200

@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    member = Member.query.get(id)
    if not member:
        return jsonify({"error": "Member not found"}), 404
    member_schema = MemberSchema()
    return member_schema.jsonify(member), 200

@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    member = Member.query.get(id)
    if not member:
        return jsonify({"error": "Member not found"}), 404

    data = request.get_json()
    member.name = data.get('name', member.name)
    member.email = data.get('email', member.email)
    member.phone = data.get('phone', member.phone)

    db.session.commit()
    member_schema = MemberSchema()
    return member_schema.jsonify(member), 200

@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    member = Member.query.get(id)
    if not member:
        return jsonify({"error": "Member not found"}), 404
    
    db.session.delete(member)
    db.session.commit()
    return '', 204

# CRUD Operations for Workout Sessions
@app.route('/workout_sessions', methods=['POST'])
def add_workout_session():
    data = request.get_json()
    date = data.get('date')
    time = data.get('time')
    member_id = data.get('member_id')

    if not all([date, time, member_id]):
        return jsonify({"error": "Missing data"}), 400
    
    new_session = WorkoutSession(date=date, time=time, member_id=member_id)
    db.session.add(new_session)
    db.session.commit()
    
    workout_session_schema = WorkoutSessionSchema()
    return workout_session_schema.jsonify(new_session), 201

@app.route('/workout_sessions/<int:id>', methods=['GET'])
def get_workout_session(id):
    session = WorkoutSession.query.get(id)
    if not session:
        return jsonify({"error": "Workout session not found"}), 404
    
    workout_session_schema = WorkoutSessionSchema()
    return workout_session_schema.jsonify(session), 200

@app.route('/workout_sessions', methods=['GET'])
def get_workout_sessions():
    workout_sessions = WorkoutSession.query.all()
    workout_session_schema = WorkoutSessionSchema(many=True)
    return workout_session_schema.jsonify(workout_sessions), 200

@app.route('/workout_sessions/<int:id>', methods=['PUT'])
def update_workout_session(id):
    session = WorkoutSession.query.get(id)
    if not session:
        return jsonify({"error": "Workout session not found"}), 404

    data = request.get_json()
    session.date = data.get('date', session.date)
    session.time = data.get('time', session.time)
    session.member_id = data.get('member_id', session.member_id)

    db.session.commit()
    workout_session_schema = WorkoutSessionSchema()
    return workout_session_schema.jsonify(session), 200

@app.route('/members/<int:id>/workout_sessions', methods=['GET'])
def get_member_workout_sessions(id):
    member = Member.query.get(id)
    if not member:
        return jsonify({"error": "Member not found"}), 404

    workout_sessions = WorkoutSession.query.filter_by(member_id=id).all()
    workout_session_schema = WorkoutSessionSchema(many=True)
    return workout_session_schema.jsonify(workout_sessions), 200

if __name__ == "__main__":
    app.run(debug=True)
