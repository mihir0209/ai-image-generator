import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '3306')
    DB_NAME = os.environ.get('DB_NAME', 'image_generator')
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
    
    # SQLAlchemy configuration with connection pooling
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'max_overflow': 20
    }
    
    # API
    API_BASE_URL = "https://api.infip.pro"
    API_KEY = os.environ.get('API_KEY')
    
    # AWS
    AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
    USE_S3 = os.environ.get('USE_S3', 'true').lower() == 'true'
    S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
    CLOUDFRONT_DOMAIN = os.environ.get('CLOUDFRONT_DOMAIN', '')
    
    # SNS
    SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN', '')
    
    # CloudWatch
    CLOUDWATCH_NAMESPACE = os.environ.get('CLOUDWATCH_NAMESPACE', 'ImageGenerator/Metrics')
    
    # IAM Role
    USE_IAM_ROLE = os.environ.get('USE_IAM_ROLE', 'false').lower() == 'true'
    
    # Upload
    MEDIA_FOLDER = "media"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
