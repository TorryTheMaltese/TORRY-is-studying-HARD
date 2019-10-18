class Config:
    SECRET_KEY = 'torry'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/torry'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # UPLOAD_FOLDER = 'app/static/upload_folder'
