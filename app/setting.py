import os
DEBUG = True

SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.environ.get('SECRET_KEY')

DATABASE = 'myweb.sqlite'
SQLALCHEMY_DATABASE_URI = "sqlite:///" + \
        os.path.join(os.path.dirname(__file__), DATABASE)