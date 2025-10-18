from flask import Flask, render_template, request, redirect, url_for, flash, Response, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///student_management.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'admin-secret-key-2024'

db = SQLAlchemy(app)

# Admin credentials (in production, use proper authentication)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# Student Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15))
    course_interested = db.Column(db.String(100))
    inquiry_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='New Inquiry')
    
    def __repr__(self):
        return f"<Student {self.name} - {self.email}>"

# Followup Model
class Followup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    followup_date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
    next_followup = db.Column(db.DateTime)
    status = db.Column(db.String(50), default='Pending')
    
    student = db.relationship('Student', backref='followups')
    
    def __repr__(self):
        return f"<Followup for Student {self.student_id}>"

# Admission Model
class Admission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    admission_date = db.Column(db.DateTime, default=datetime.utcnow)
    course_enrolled = db.Column(db.String(100))
    total_fees = db.Column(db.Float)
    fees_paid = db.Column(db.Float, default=0.0)
    
    student = db.relationship('Student', backref='admission')
    
    def __repr__(self):
        return f"<Admission for Student {self.student_id}>"
if __name__ == '__main__':
    app.run(debug=True)