from app import db
from app import login

from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin

from sqlalchemy import ForeignKey, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Column, DDL
import sqlalchemy.dialects.postgresql

""" injection of raw DDL added to alembic migration file :
../migrations/versions/79b9a7b13064_create_db_and_trigger.py 
row->
creating trigger_delete_expired
to delete obsolete entries after each insertion"""

class Users(UserMixin, db.Model):
    """user accounts table for granting access"""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Datafiles(db.Model):
    """data stored by user"""

    last_commit = None

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    filename = db.Column(db.String(120), index=True)
    datafile = db.Column(db.LargeBinary)
    expire = db.Column(db.DateTime)


@login.user_loader
def load_user(id):
    return Users.query.get(int(id))
