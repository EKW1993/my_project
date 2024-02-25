import os

class Config: 
    DEBUG = True 
    SECRET_KEY = 'super-secret-key' 
    SQLALCHEMY_DATABASE_URI = 'sqlite:///blog.db' 
    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin") 
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "change-me")
