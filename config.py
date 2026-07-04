class Config:

    SECRET_KEY = "123456"

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/crud_python"

    SQLALCHEMY_TRACK_MODIFICATIONS = False