from database import db
from flask_security import UserMixin, RoleMixin
from datetime import datetime, date

class User(db.Model, UserMixin):       ## User Model ##
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    fullname = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False) # required for flask_security_too

    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    fs_token_uniquifier = db.Column(db.String(255), unique=True, nullable=True)
    # relationship
    roles = db.relationship('Role', secondary='user_role', backref='users')
    bookings = db.relationship('Booking', back_populates='user', cascade='all, delete-orphan')
    assigned_treks = db.relationship('Trek', back_populates='assigned_staff', foreign_keys='Trek.assign_staff_id')
    staff_info = db.relationship('Staff_info', back_populates='staff', uselist=False, cascade='all, delete-orphan')
    trekker_info = db.relationship('Trekker_info', back_populates='trekker', uselist=False, cascade='all, delete-orphan')

class Role(db.Model, RoleMixin):        ## Role Model ##
    __tablename__='role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True) # {admin, staff, trekker}
    description = db.Column(db.String())

class UserRoles(db.Model):              ## User Role Model ##
    __tablename__='user_role'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))


class Trek(db.Model):                   ## Trek Model ##
    __tablename__ = 'trek'
    id = db.Column(db.Integer, primary_key=True)
    trek_name = db.Column(db.String(), unique=True, nullable=False)
    duration = db.Column(db.String(), nullable=False)
    difficulty = db.Column(db.String(), nullable=False)
    # Beginner (Explorer), Intermediate (Adventurer), Advanced (Trailblazer)

    location = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    assign_staff_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    status = db.Column(db.String(), nullable=False, default='Inactive')    #(Active, Inactive)
    # relationship                                     
    bookings = db.relationship('Booking', back_populates='trek', cascade='all, delete-orphan')
    assigned_staff = db.relationship('User', back_populates='assigned_treks', foreign_keys=[assign_staff_id])


class Availability(db.Model):              ## Availability Model ##
    __tablename__='availability'
    id = db.Column(db.Integer,  primary_key=True)
    trek_id = db.Column(db.Integer, db.ForeignKey(Trek.id), nullable=False)
    start_date = db.Column(db.Date(), nullable=False)
    end_date = db.Column(db.Date(), nullable=False)

    total_slot = db.Column(db.Integer(), nullable=False)
    avail_slot = db.Column(db.Integer(), nullable=False)
    status = db.Column(db.String(), default='Open')

    __table_args__ = (
        db.UniqueConstraint('trek_id', 'start_date', name='unique_trek_date'),
    )


class Booking(db.Model):                ## Booking Model ##
    __tablename__='booking'
    id = db.Column(db.Integer,  primary_key=True)
    usr_id = db.Column(db.Integer, db.ForeignKey(User.id))
    trek_id = db.Column(db.Integer, db.ForeignKey(Trek.id))
    booking_date = db.Column(db.Date(), nullable=False)
    status = db.Column(db.String(), nullable=False) #(Booked/Completed/Cancelled)
    
    user = db.relationship('User', back_populates='bookings')
    trek = db.relationship('Trek', back_populates='bookings')


class Staff_info(db.Model):               ## Staff Info Model ##
    __tablename__='staff_info'
    id = db.Column(db.Integer,  primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey(User.id), unique=True)

    dob = db.Column(db.Date())
    gender = db.Column(db.String())
    address = db.Column(db.String())
    phone = db.Column(db.Integer())

    designation = db.Column(db.String(50))      # Guide, Coordinator, Driver
    experience_years = db.Column(db.Integer())
    joining_date = db.Column(db.Date(), default=date.today, nullable=False) # Automatically gets the date of account created by admin
    # relationship
    staff = db.relationship('User', back_populates='staff_info')


class Trekker_info(db.Model):               ## Trekker Info Model ##
    __tablename__='trekker_info'
    id = db.Column(db.Integer,  primary_key=True)
    trekker_id = db.Column(db.Integer, db.ForeignKey(User.id), unique=True)

    dob = db.Column(db.Date())
    gender = db.Column(db.String(1))
    phone = db.Column(db.Integer())
    address = db.Column(db.String())
    # relationship
    trekker = db.relationship('User', back_populates='trekker_info')
