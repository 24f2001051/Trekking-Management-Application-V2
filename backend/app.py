from flask import Flask
from flask_security import Security
from flask_restful import Api, Resource
from flask_security.utils import hash_password
from flask_cors import CORS

from database import db
from model import User, Role, UserRoles, Trek, Booking, Availability, Trekker_info, Staff_info
from config import Config
from user_datastore import user_datastore

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    
    security = Security(app, user_datastore)
    app.app_context().push()

    api = Api(app, prefix='/api')



    # login_manager.init_app(app)
    # login_manager.login_view = 'login'  # Redirect to 'login' view if not logged in
    return app, api

app, api = create_app()

CORS(
app,
resources={
r"/api/*": {
"origins": [
"http://localhost:5173",
"http://127.0.0.1:5173"
]
}
},
allow_headers=[
"Content-Type",
"Authentication-Token",
"Authorization"
],
methods=[
"GET",
"POST",
"PUT",
"PATCH",
"DELETE",
"OPTIONS"
]
)


class Index(Resource):
    def get(self):
        return {'message': 'Hello, World!'}

from apis import LoginAPI, LogoutAPI, RegisterAPI
from apis import AdminDashboardAPI, AdminDashboardTreksAPI, AdminDashboardStaffAPI, AdminDashboardUsersAPI, AdminDashboardBookingsAPI, AdminDashboardReportsAPI
from apis import AddStaffAPI, AddTrekAPI, EditDeleteTrekAPI, AssignTrekToStaffAPI,AdminDeleteUserAPI ,AdminStaffOptionsAPI, AdminStaffStatusAPI , AdminUserStatusAPI

from apis import  StaffDashboardAPI, TrekkerDashboardAPI, AddTrekAPI



# api.add_resource(Index, '/')
api.add_resource(LoginAPI, '/login')
api.add_resource(LogoutAPI, '/logout')
api.add_resource(RegisterAPI, '/register')

api.add_resource(AdminDashboardAPI, '/admin_dashboard') #Admin dashboard
api.add_resource(AdminDashboardTreksAPI, '/admin_dashboard/treks')
api.add_resource(AdminDashboardStaffAPI, '/admin_dashboard/staff')
api.add_resource(AdminDashboardUsersAPI, '/admin_dashboard/users')
api.add_resource(AdminDashboardBookingsAPI, '/admin_dashboard/bookings')
api.add_resource(AdminDashboardReportsAPI, '/admin_dashboard/reports')

api.add_resource(AddTrekAPI, '/admin_dashboard/treks/add_trek')
api.add_resource(AddStaffAPI, '/admin_dashboard/staff/add_staff')
api.add_resource(EditDeleteTrekAPI, '/admin_dashboard/treks/<int:trek_id>')
api.add_resource(AdminDeleteUserAPI, '/admin_dashboard/users/<int:user_id>')
api.add_resource(AssignTrekToStaffAPI, '/admin_dashboard/staff/<int:staff_id>/assigned_trek')

api.add_resource(AdminStaffOptionsAPI, '/admin_dashboard/staff_options')
api.add_resource(AdminStaffStatusAPI, '/admin_dashboard/staff/<int:staff_id>/status')
api.add_resource(AdminUserStatusAPI, '/admin_dashboard/users/<int:user_id>/status')

api.add_resource(StaffDashboardAPI, '/staff_dashboard')
api.add_resource(TrekkerDashboardAPI, '/trekker_dashboard')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        
        admin_role = user_datastore.find_or_create_role(name="admin", description="employer,administrator")
        staff_role = user_datastore.find_or_create_role(name="staff", description="employees, trek staff")
        trekker_role = user_datastore.find_or_create_role(name="trekker", description="client, trekkers")
        db.session.commit()
        
        if not user_datastore.find_user(username="admin"):
            user_datastore.create_user(
                username="admin",
                email="administrator@admin.com",
                fullname="Adminstrator",
                password=hash_password("admin"),
                roles=[admin_role])
            db.session.commit()
            
            # user_datastore.add_role_to_user(user_datastore.find_user(username="admin"), admin_role)
            # user_datastore.add_role_to_user(user_datastore.find_user(username="admin"), staff_role)
            # user_datastore.add_role_to_user(user_datastore.find_user(username="admin"), trekker_role)
        

    app.run(debug=True)