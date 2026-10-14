from flask_restful import Resource
from flask import jsonify, make_response,request
from flask_security.utils import hash_password
from sqlalchemy import func
from user_datastore import user_datastore
from database import db
from model import Trek, Booking, Availability, Trekker_info, Staff_info, User, Role, UserRoles
from flask_security  import utils, auth_token_required, roles_required, current_user
from datetime import date

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
                "trek_id": trek.id,
                "trek_name": trek.trek_name,
                "location": trek.location,
                "difficulty": trek.difficulty,
                "duration": trek.duration,
                "description": trek.description,
                "assigned_staff_id": trek.assign_staff_id,
                "assigned_staff": (trek.assigned_staff.fullname if trek.assigned_staff else "N/A"),
                "status": trek.status
            })
        return make_response(jsonify(trek_list),200)

class AdminDashboardStaffAPI(Resource):
    @auth_token_required
    @roles_required("admin")
    def get(self):
        staffs = User.query.filter(
            User.roles.any(name="staff")
        ).all()

        staff_list = []

        for staff in staffs:
            staff_info = Staff_info.query.filter_by(
                staff_id=staff.id
            ).first()
            assigned_trek = Trek.query.filter_by(assign_staff_id=staff.id).first()
            staff_list.append({
                "staff_id": staff.id,
                "username": staff.username,
                "email": staff.email,
                "fullname": staff.fullname,
                "designation": (
                    staff_info.designation
                    if staff_info
                    else "N/A"
                ),
                "assigned_trek_id": (assigned_trek.id if assigned_trek else "None" ),
                "assigned_treks": assigned_trek.trek_name if assigned_trek else "N/A",
                "status": staff.active
            })

        return make_response(jsonify(staff_list), 200)


class AdminDashboardUsersAPI(Resource):

    @auth_token_required
    @roles_required('admin')
    def get(self):
        try:
            print("Users API called")

            users = User.query.filter(User.roles.any(name='trekker')).all()

            user_list = []

            for user in users:
                user_list.append({
                    "user_id": user.id,
                    "fullname": user.fullname,
                    "username": user.username,
                    "email": user.email,
                    "status": user.active
                })

            print("Users:", user_list)

            return make_response(jsonify(user_list), 200)

        except Exception as e:
            import traceback
            traceback.print_exc()

            return make_response(jsonify({
                "message": str(e)
            }), 500)


class AdminDashboardBookingsAPI(Resource):
    @auth_token_required
    @roles_required("admin")
    def get(self):
        bookings = Booking.query.order_by(Booking.booking_date.desc()).all()
        booking_list = []

        for booking in bookings:
            booking_list.append({
                "booking_id": booking.id,
                "user": (
                    booking.user.fullname
                    if booking.user else "N/A"
                ),
                "trek": (
                    booking.trek.trek_name
                    if booking.trek else "N/A"
                ),
                "booking_date": (
                    booking.booking_date.strftime("%d-%m-%Y")
                    if booking.booking_date else ""
                ),
                "status": booking.status
            })
        return make_response(jsonify(booking_list),200)

class AdminDashboardReportsAPI(Resource):
    @auth_token_required
    @roles_required("admin")
    def get(self):

        total_treks = Trek.query.count()
        active_treks = Trek.query.filter_by(status="Active").count()
        inactive_treks = Trek.query.filter_by(status="Inactive").count()
        total_users = User.query.filter(User.roles.any(name='trekker')).count()
        total_staff = User.query.filter(User.roles.any(name='staff')).count()
        total_bookings = Booking.query.count()
        confirmed_bookings = Booking.query.filter_by(status="Confirmed").count()
        cancelled_bookings = Booking.query.filter_by(status="Cancelled").count()
       
        return make_response(jsonify({
            "total_treks": total_treks,
            "active_treks": active_treks,
            "inactive_treks": inactive_treks,
            "total_users": total_users,
            "total_staff": total_staff,
            "total_bookings": total_bookings,
            "confirmed_bookings": confirmed_bookings,
            "cancelled_bookings": cancelled_bookings,
            }
        ), 200)


class AdminDeleteUserAPI(Resource):
    @auth_token_required
    @roles_required("admin")
    def delete(self, user_id):
        user = User.query.get(user_id)

        if not user:
            return make_response(
                jsonify({"message": "User not found"}), 404
            )

        # Prevent deleting the admin account or any other non-target role.
        role_names = {role.name for role in user.roles}
        if not role_names.intersection({"trekker", "staff"}):
            return make_response(
                jsonify({
                    "message": "Only trekkers and staff can be deleted"
                }), 400
            )

        # Refuse deletion if bookings reference this user.
        if Booking.query.filter_by(usr_id=user.id).first():
            return make_response(
                jsonify({
                    "message": (
                        "Cannot delete this account because bookings "
                        "are associated with it."
                    )
                }), 409
            )

        # Refuse deletion if this user is assigned to any treks.
        if Trek.query.filter_by(assign_staff_id=user.id).first():
            return make_response(
                jsonify({
                    "message": (
                        "Cannot delete this staff member because "
                        "they are assigned to treks."
                    )
                }), 409
            )

        # Remove the associated profile, if it exists.
        if "trekker" in role_names:
            profile = Trekker_info.query.filter_by(
                trekker_id=user.id
            ).first()
            if profile:
                db.session.delete(profile)

        if "staff" in role_names:
            profile = Staff_info.query.filter_by(
                staff_id=user.id
            ).first()
            if profile:
                db.session.delete(profile)

        # Remove role associations before deleting the user.
        user.roles.clear()
        db.session.delete(user)
        db.session.commit()

        return make_response(
            jsonify({"message": "Account deleted successfully"}), 200
        )

class EditDeleteTrekAPI(Resource):
    @auth_token_required
    @roles_required("admin")

    def put(self, trek_id):

        trek = Trek.query.get_or_404(trek_id)
        if trek is None:
            return make_response(jsonify({"message": "Trek not found"}), 404)

        data = request.get_json()
        trek.trek_name = data.get('trek_name', trek.trek_name)
        trek.location = data.get('location', trek.location)
        trek.difficulty = data.get('difficulty', trek.difficulty)
        trek.duration = data.get('duration', trek.duration)
        trek.description = data.get('description', trek.discription)
        trek.status = data.get('status', trek.status)

        staff_id = data.get('assign_staff_id', trek.assign_staff_id)

        if staff_id is not None:
            staff = User.query.get_or_404(staff_id)
            if staff is None:
                return make_response(jsonify({"message": "Staff not found"}), 404)
            
            existing_trek = Trek.query.filter(Trek.assign_staff_id==staff_id, Trek.id!=trek_id).first()
            if existing_trek is not None:
                return make_response(jsonify({"message": (
                    f"Theis Staff member is already assigned to "
                    f"{existing_trek.trek_name}."
                    )}), 400)
           
            trek.assign_staff_id = staff_id



        try:
            db.session.commit()
            return  make_response(jsonify({"message": "Trek updated successfully"}), 200)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"message": "Error updating trek: " + str(e)}), 500)

    @auth_token_required
    @roles_required("admin")
    def delete(self, trek_id):
        trek = Trek.query.get_or_404(trek_id)

        if not trek:
            return make_response(jsonify({"message": "Trek not found"}), 404)

        try:
            db.session.delete(trek)
            db.session.commit()
            return make_response(jsonify({"message": "Trek deleted successfully"}), 200)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"message": "Error deleting trek: " + str(e)}), 500)

class AdminStaffOptionsAPI(Resource):
    @auth_token_required
    @roles_required("admin")
    def get(self):
        staffs = User.query.filter(User.roles.any(name='staff')).all()
        staff_list = []

        for staff in staffs:
            staff_list.append({
                "staff_id": staff.id,
                "fullname": staff.fullname,
            })
        return make_response(jsonify(staff_list),200)

class AdminStaffStatusAPI(Resource):
    @auth_token_required
    @roles_required("admin")
    def put(self, staff_id):
        staff = User.query.get_or_404(staff_id)
        if staff is None:
            return make_response(jsonify({"message": "Staff not found"}), 404)

        data = request.get_json()
        staff.active = data.get('active', staff.active)

        try:
            db.session.commit()
            return  make_response(jsonify({"message": "Staff Status Updated"}), 200)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"message": "Error updating Status: " + str(e)}), 500)

class AdminUserStatusAPI(Resource):
    @auth_token_required
    @roles_required("admin")
    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        if user is None:
            return make_response(jsonify({"message": "User not found"}), 404)

        data = request.get_json()
        user.active = data.get('active', user.active)

        try:
            db.session.commit()
            return  make_response(jsonify({"message": "User Status Updated"}), 200)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"message": "Error updating Status: " + str(e)}), 500)


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
        assign_staff_id = data.get('assign_staff_id', None)
        status = data.get('status', 'Inactive')
        duration = data.get('duration', None)
        description = data.get('description', None)

        if not all([trek_name, duration, difficulty, location, description]):
            return make_response(jsonify({
                "message": "Missing required fields. Provide trek_name, duration, difficulty, location, and description."
            }), 400)

        if Trek.query.filter_by(trek_name=trek_name).first():
            return make_response(jsonify({
                "message": "A trek with this name already exists" }), 400)

        try:
            new_trek = Trek(
                trek_name = trek_name,
                duration = duration,
                difficulty = difficulty,
                location = location,
                description = description,
                assign_staff_id = assign_staff_id,
                status = status,
            )
            db.session.add(new_trek)
            db.session.commit()
            return make_response(jsonify({ "message": "Trek added successfully" }), 201)

        except Exception as e:
            db.session.rollback()  # Rollback changes if anything crashes to keep database clean
            return make_response(jsonify({ "message": f"Error saving staff: {str(e)}" }), 500)

class AssignTrekToStaffAPI(Resource):

    @auth_token_required
    @roles_required("admin")
    def put(self, staff_id):

        staff = User.query.get_or_404(staff_id)

        if not staff.has_role("staff"):
            return make_response(
                jsonify({"message": "Selected user is not a staff member"}),
                400
            )

        data = request.get_json() or {}
        trek_id = data.get("trek_id")

        # Find the trek currently assigned to this staff member
        current_trek = Trek.query.filter_by(
            assign_staff_id=staff.id
        ).first()

        try:
            # Null means unassign this staff member
            if trek_id is None:
                if current_trek:
                    current_trek.assign_staff_id = None

                db.session.commit()
                return make_response(
                    jsonify({"message": "Trek assignment removed"}),
                    200
                )

            # Validate the selected trek
            selected_trek = Trek.query.get(trek_id)

            if not selected_trek:
                return make_response(
                    jsonify({"message": "Trek not found"}),
                    404
                )

            # Prevent assigning a trek already assigned to another staff member
            if (
                selected_trek.assign_staff_id is not None
                and selected_trek.assign_staff_id != staff.id
            ):
                return make_response(
                    jsonify({
                        "message": "This trek is already assigned to another staff member"
                    }),
                    400
                )

            # Remove the staff member's previous assignment
            if current_trek and current_trek.id != selected_trek.id:
                current_trek.assign_staff_id = None

            # Assign the selected trek
            selected_trek.assign_staff_id = staff.id

            db.session.commit()

            return make_response(
                jsonify({"message": "Trek assigned successfully"}),
                200
            )

        except Exception as e:
            db.session.rollback()
            return make_response(
                jsonify({"message": "Error assigning trek: " + str(e)}),
                500
            )










class StaffDashboardAPI(Resource):
    @auth_token_required
    @roles_required("staff")
    def get(self):
        trek = Trek.query.filter_by(assign_staff_id=current_user.id).first()

        if not trek:
            return make_response(jsonify({"message": "Trek not found"}), 404)

        today = date.today()
        total_participants = (
            db.session.query(
                func.count(func.distinct(Booking.usr_id))
            )
            .filter(
                Booking.trek_id == trek.id,
                Booking.usr_id.isnot(None),
                Booking.status != "Cancelled"
            )
            .scalar()
        ) or 0       

        availabilities = (
            Availability.query
            .filter_by(trek_id = trek.id)
            .order_by(Availability.start_date.asc())
            .all()
        )

        upcoming_treks = []
        upcoming_trek_count = None
        for availability in availabilities:
            start_date = availability.start_date.strftime('%d %b %Y')
            end_date = availability.end_date.strftime('%d %b %Y')

            schedule = {
                'trek_id': trek.id,
                'availability_id': availability.id,
                'trek_name': trek.trek_name,
                'participants': total_participants,
                "dates": f'{start_date} - {end_date}',
                "start_date": start_date,
                "end_date": end_date,
                'avail_slot': availability.avail_slot,
                'status': availability.status or 'Not Scheduled',
                'progress_status': availability.progress_status,
            }

            if ( availability.start_date >= today ) and (availability.status == 'Open'):
                upcoming_treks.append(schedule)
        
        trek = Trek.query.filter_by(assign_staff_id = current_user.id).first()
        upcoming_trek_count = len(upcoming_treks)

        return {
            'trek': 1,
            'assigned_trek': trek.trek_name,
            'total_participants': total_participants,
            'upcoming_treks': upcoming_treks,
            'upcoming_trek_count': upcoming_trek_count

        }, 200


class StaffDashboardMyTrekAPI(Resource):
    @auth_token_required
    @roles_required("staff")
    def get(self):
        treks = Trek.query.filter_by(assign_staff_id=current_user.id).first()

        if not treks:
            return make_response(jsonify({"message": "Trek not found"}), 404)

        availabilities = (Availability.query.filter_by(trek_id = treks.id).order_by(Availability.start_date.asc()).all())

        schedules = []

        for availability in availabilities:
            start_date = availability.start_date.strftime('%d %b %Y')
            end_date = availability.end_date.strftime('%d %b %Y')

            schedules.append({
                "availability_id": availability.id,
                "trek_id": treks.id,
                "trek_name": treks.trek_name,
                "dates": f'{start_date} - {end_date}',
                "total_slot": availability.total_slot,
                "avail_slot": availability.avail_slot,
                "status": availability.status or 'Not Scheduled',
                "progress_status": availability.progress_status
            })

        return make_response(jsonify({
            "trek": {
                "trek_id": treks.id,
                "trek_name": treks.trek_name,
                "location": treks.location,
                "difficulty": treks.difficulty,
                "duration": treks.duration,
                "description": treks.description,
                "status": treks.status,
                "assign_staff_id": treks.assign_staff_id,
            },
            "schedules": schedules
        }),200)


class StaffUpdateAvailabilityAPI(Resource):
    @auth_token_required
    @roles_required("staff")
    def put(self, availability_id):
        availability = Availability.query.get_or_404(availability_id)
        trek = Trek.query.filter_by(assign_staff_id=current_user.id, id=availability.trek_id).first()

        if not trek:
            return make_response(jsonify({"message": "Trek not found"}), 403)

        if not availability:
            return make_response(jsonify({"message": "Availability not found"}), 404)

        data = request.get_json(silent=True) or {}
        if not data:
            return make_response(jsonify({"message": "No data provided"}), 400)


        if "avail_slot" in data:
            try:
                slots = int(data["avail_slot"])
            except (TypeError, ValueError):
                return make_response(jsonify({"message": "Invalid Available Slot"}), 400)

            if slots < 0 or slots > availability.total_slot:
                return make_response(jsonify({"message": ( f"Available Slots must be between 0 and {availability.total_slot}")}), 400)
            
            availability.avail_slot = slots

        if "status" in data:
            status = data["status"]
            if status not in ["Open", "Closed"]:
                return make_response(jsonify({"message": "Invalid status"}), 400)
            if status == "Open" and availability.avail_slot <= 0:
                return make_response(jsonify({"message": "Available Slots cannot be zero if status is Open"}), 400)

            availability.status = status

        if "progress_status" in data:
            progress = data["progress_status"]
            allowed_progress = ["Not Started", "Started", "Ongoing", "Completed"]

            if progress not in allowed_progress:
                return make_response(jsonify({"message": "Invalid trek progress status"}), 400)
            availability.progress_status = progress

        db.session.commit()

        return make_response(jsonify({
            "message": "Schedule updated successfully",
            "availability_id": availability.id,
            "avail_slot": availability.avail_slot,
            "status": availability.status,
            "progress_status": availability.progress_status
            }),200)

class StaffDashboardParticipantsAPI(Resource):
    @auth_token_required
    @roles_required("staff")
    def get(self):
        trek = Trek.query.filter_by(assign_staff_id=current_user.id).first()

        if not trek:
            return make_response(jsonify({"message": "Trek not found"}), 403)

        bookings = (Booking.query.filter(
            Booking.trek_id == trek.id,
            Booking.usr_id.isnot(None),
            Booking.status != "Cancelled"
            ).order_by(Booking.booking_date.desc()).all())

        participants = {}

        for booking in bookings:
            user = booking.user

            if not user or user.id in participants:
                continue

            info = Trekker_info.query.filter_by(trekker_id=user.id).first()

            participants[user.id] ={
                "user_id": user.id,
                "fullname": user.fullname,
                "username": user.username,
                "email": user.email,
                "phone": (
                    str(info.phone) if info and info.phone is not None else ""
                ),
                "booking_date": (
                    booking.booking_date.strftime("%d-%m-%Y") if booking.booking_date else ""
                ),
                "booking_status": booking.status
            }

        participant_list = list(participants.values())

        return make_response(jsonify({
            "trek": trek.trek_name,
            "participants": participant_list,
            "total_participants": len(participant_list)
        }),200)

class StaffDashboardProfileAPI(Resource):
    @auth_token_required
    @roles_required("staff")
    def get(self):

        staff = User.query.get_or_404(current_user.id)

        info = Staff_info.query.filter_by(staff_id=staff.id).first()
        trek = Trek.query.filter_by(assign_staff_id=staff.id).first()


        return make_response(jsonify({
            "staff_id": staff.id,
            "fullname": staff.fullname,
            "username": staff.username,
            "email": staff.email,
            "active": staff.active,
            "designation": (info.designation if info else "N/A"),
            "experience_years": (info.experience_years if info else None),
            "phone": (str(info.phone) if info and info.phone is not None else ""),
            "address": info.address if info else "",
            "assigned_trek": (trek.trek_name if trek else "N/A")
        }),200)



class TrekkerDashboardAPI(Resource):
    pass