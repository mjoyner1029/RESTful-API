from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
ma = Marshmallow(app)

# MySQL Database connection
def create_connection():
    """Create and return a MySQL database connection."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='your_username',
            password='your_password',
            database='fitness_center'
        )
        if connection.is_connected():
            print("Connected to the database.")
            return connection
    except Error as e:
        print(f"Error: {e}")
    return None

# Define Member Schema
class MemberSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'age')

# Define WorkoutSession Schema
class WorkoutSessionSchema(ma.Schema):
    class Meta:
        fields = ('session_id', 'member_id', 'session_date', 'session_time', 'activity')

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)
workout_session_schema = WorkoutSessionSchema()
workout_sessions_schema = WorkoutSessionSchema(many=True)

if __name__ == '__main__':
    app.run(debug=True)
