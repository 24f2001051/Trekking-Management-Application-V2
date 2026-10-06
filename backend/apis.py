from flask_restful import Resource
from flask import jsonify, make_response,request
from flask_security.utils import hash_password
from user_datastore import user_datastore
from database import db
from model import Trek, Booking, Availability, Trekker_info, Staff_info, User, Role, UserRoles
from flask_security  import utils, auth_token_required, roles_required

class LoginAPI(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return make_response(jsonify({'message': 'Login credentials not provided'}), 400)

        username = data.get('username', None)
        password = data.get('password', None)     
        if not username or not password:
            return make_response(jsonify({'message': 'Username or password not provided'}), 400)

        user = user_datastore.find_user(username=username)

        # 1. Check if the user exists & 2. Check if the password is correct in the database first
        if not user:
            return make_response(jsonify({'message': 'Invalid username'}), 401)

        if not utils.verify_password(password, user.password):
            return make_response(jsonify({'message': 'Wrong password'}), 401)


        auth_token = user.get_auth_token()
        utils.login_user(user)


        return make_response(jsonify({
            'user_detail': {
                'role': [role.name for role in user.roles],
                'id': user.id,
                'username': user.username,
                'fullname': user.fullname,
                'email': user.email
                },
            'auth_token': auth_token,
            'message': 'Login successful',
            }), 200)
    
class LogoutAPI(Resource):
    @auth_token_required
    def post(self):
        utils.logout_user()
        return make_response(jsonify({'message': 'Logout successful'}), 200)
    
class RegisterAPI(Resource):
    def post(self):

        data = request.get_json()
        if not data:
            return make_response(jsonify({
                "message": "Registration credentials not provided" }), 400)
        username = data.get('username', None)
        email = data.get('email', None)
        fullname = data.get('fullname', None)
        password = data.get('password', None)

        if not username or not email or not fullname or not password:
            return make_response(jsonify({
                "message": "Please provide all 4 Registration credentials" }), 400)

        if user_datastore.find_user(username=username):
            if user_datastore.find_user(email=email):   #double verify
                return make_response(jsonify({
                    "message": "Both Username and Email already exists" }), 400)
            
            return make_response(jsonify({
                "message": "Username already exists" }), 400)

        if user_datastore.find_user(email=email):
            return make_response(jsonify({
                "message": "Email already exists" }), 400)
        
        this_role = user_datastore.find_role('trekker')

        user_datastore.create_user( username=username, email=email,
            fullname=fullname, password=hash_password(password), roles=[this_role] )
        db.session.commit()
        
        return make_response(jsonify({ "message": "User Registration successful" }), 201)
    
    def get(self):
        pass
        
    def put(self):
        pass
        
class AddStaffAPI(Resource):
    @auth_token_required
    @roles_required('admin')
    def post(self):
        data = request.get_json()
        if not data:
            return make_response(jsonify({
                "message": "Registration credentials not provided" }), 400)
        username = data.get('username', None)
        email = data.get('email', None)
        fullname = data.get('fullname', None)
        password = data.get('password', None)
        phonenumber = data.get('phonenumber', None)
        experience = data.get('experience', None)
        designation = data.get('designation', None)

        if not username or not email or not fullname or not password or not designation:
            return make_response(jsonify({
                "message": "Please provide all Registration credentials" }), 400)

        if user_datastore.find_user(username=username):
            return make_response(jsonify({
                "message": "Username already exists" }), 400)

        if user_datastore.find_user(email=email):
            return make_response(jsonify({
                "message": "Email already exists" }), 400)
        
        this_role = user_datastore.find_role('staff')

        try:
            new_staff_user = user_datastore.create_user(
                username=username, email=email, fullname=fullname, 
                password=hash_password(password), roles=[this_role]
            )
            # Flush changes to the session so SQLAlchemy generates the new user's ID
            # without fully finalizing the transaction yet.
            db.session.flush()

            new_staff_details = Staff_info(
                staff_id=new_staff_user.id,        # Connects the foreign key relationship
                phone=phonenumber, experience_years=experience, designation=designation
                
            )
            
            db.session.add(new_staff_details)
            db.session.commit()
            
            return make_response(jsonify({ "message": "Staff Registration successful" }), 201)

        except Exception as e:
            db.session.rollback()  # Rollback changes if anything crashes to keep database clean
            return make_response(jsonify({ "message": f"Error saving staff: {str(e)}" }), 500)



class AdminDashboardAPI(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self):
        total_treks = Trek.query.count()
        total_users = User.query.join(User.roles).filter_by(name="trekker").count()
        total_staff = User.query.join(User.roles).filter_by(name="staff").count()
        total_bookings = Booking.query.count()

        recent_bookings =( Booking.query.order_by(Booking.booking_date.desc()).limit(3).all() )
        booking_list = []

        for booking in recent_bookings:
            booking_list.append({
                "id": booking.id,
                "trek": booking.trek.name,
                "trekker": booking.user.fullname,
                "date": booking.booking_date.strftime("%d %b %Y"),
                "status": booking.status
            })

        return make_response(jsonify({
            "total_treks": total_treks,
            "total_users": total_users,
            "total_staff": total_staff,
            "total_bookings": total_bookings,
            "recent_bookings": booking_list,
            }
        ), 200)

class AdminDashboardTreksAPI(Resource):
    @auth_token_required
    @roles_required("admin")
    def get(self):
        treks = Trek.query.all()
        trek_list = []

        for trek in treks:
            trek_list.append({
                "trek_id": trek.trek_id,
                "trek_name": trek.trek_name,
                "location": trek.location,
                "difficulty": trek.difficulty,
                "slots": trek.available_slots,
                "status": trek.status
            })
        return make_response(jsonify(trek_list),200)


class AddTrekAPI(Resource):
    @auth_token_required
    @roles_required('admin')
    def post(self):
        data = request.get_json()
        if not data:
            return make_response(jsonify({
                "message": "Registration credentials not provided" }), 400)
        trek_name = data.get('trek_name', None)
        location = data.get('location', None)
        difficulty = data.get('difficulty', None)
        slots = data.get('slots', None)
        status = data.get('status', None)
        duration = data.get('duration', None)
        designation = data.get('designation', None)

        if not username or not email or not fullname or not password or not designation:
            return make_response(jsonify({
                "message": "Please provide all Registration credentials" }), 400)

        if user_datastore.find_user(username=username):
            return make_response(jsonify({
                "message": "Username already exists" }), 400)

        if user_datastore.find_user(email=email):
            return make_response(jsonify({
                "message": "Email already exists" }), 400)
        
        this_role = user_datastore.find_role('staff')

        try:
            new_staff_user = user_datastore.create_user(
                username=username, email=email, fullname=fullname, 
                password=hash_password(password), roles=[this_role]
            )
            # Flush changes to the session so SQLAlchemy generates the new user's ID
            # without fully finalizing the transaction yet.
            db.session.flush()

            new_staff_details = Staff_info(
                staff_id=new_staff_user.id,        # Connects the foreign key relationship
                phone=phonenumber, experience_years=experience, designation=designation
                
            )
            
            db.session.add(new_staff_details)
            db.session.commit()
            
            return make_response(jsonify({ "message": "Staff Registration successful" }), 201)

        except Exception as e:
            db.session.rollback()  # Rollback changes if anything crashes to keep database clean
            return make_response(jsonify({ "message": f"Error saving staff: {str(e)}" }), 500)

    

class StaffDashboardAPI(Resource):
    pass

class TrekkerDashboardAPI(Resource):
    pass