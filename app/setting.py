import os
DEBUG = True

SQLALCHEMY_TRACK_MODIFICATIONS = False
# TODO: Try not hardcode the secret key
SECRET_KEY='A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

DATABASE = 'myweb.sqlite'
SQLALCHEMY_DATABASE_URI = "sqlite:///" + \
        os.path.join(os.path.dirname(__file__), DATABASE)