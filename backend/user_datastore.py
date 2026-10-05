from flask_security import SQLAlchemyUserDatastore
from model import User, Role
from database import db

user_datastore = SQLAlchemyUserDatastore(db, User, Role)