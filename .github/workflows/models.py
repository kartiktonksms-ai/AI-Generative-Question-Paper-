from datetime import datetime, timezone
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(20), nullable=False, default='teacher')
    papers = db.relationship('QuestionPaper', backref='author', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.role}')"


class QuestionPaper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(150), nullable=False)
    topic = db.Column(db.String(150), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    meta = db.Column(db.Text, nullable=True)  # JSON: question-type counts
    date_created = db.Column(db.DateTime, nullable=False,
                             default=lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"QuestionPaper('{self.subject}', '{self.topic}', '{self.date_created}')"
