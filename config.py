import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'torry'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/torry'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = basedir+'\\app\\static\\upload_folder'
    # UPLOAD_FOLDER = 'app/static/upload_folder'
