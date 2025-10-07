from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    images = db.relationship('Image', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    stats = db.relationship('UserStats', backref='user', uselist=False, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'

class Image(db.Model):
    __tablename__ = 'images'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    prompt = db.Column(db.Text, nullable=False)
    model = db.Column(db.String(50), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    s3_key = db.Column(db.String(500))
    thumbnail_key = db.Column(db.String(500))
    cloudfront_url = db.Column(db.String(500))
    size = db.Column(db.String(20))
    quality = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<Image {self.filename}>'
    
    def to_dict(self):
        """Convert image object to dictionary with safe date handling"""
        # Use current time if created_at is None (shouldn't happen, but safety first)
        if self.created_at:
            created_at_str = self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        else:
            created_at_str = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        
        return {
            'id': self.id,
            'prompt': self.prompt,
            'model': self.model,
            'filename': self.filename,
            'url': self.cloudfront_url or f'/media/{self.filename}',
            'thumbnail': self.thumbnail_key if self.thumbnail_key else None,
            'size': self.size if self.size else '1024x1024',
            'quality': self.quality if self.quality else 'standard',
            'created_at': created_at_str
        }


class UserStats(db.Model):
    __tablename__ = 'user_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    total_generations = db.Column(db.Integer, default=0)
    last_generation = db.Column(db.DateTime)
    total_images = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<UserStats user_id={self.user_id}>'
