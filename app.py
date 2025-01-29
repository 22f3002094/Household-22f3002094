from flask import Flask
from flask_login import LoginManager
from backend.models import db,User,ServiceCategory,Booking
import os

app = None

def initial_Setup():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///my_app_db.sqlite3"
    app.config["SECRET_KEY"] = "xyshhfjf"
    login_manager = LoginManager(app)
    @login_manager.user_loader
    def load_user(user_email):
        return db.session.query(Admin).filter_by(email = user_email).first()  or \
             db.session.query(User).filter_by(email = user_email).first() or \
              db.session.query(Professional).filter_by(email = user_email).first()


    db.init_app(app)
    with app.app_context():
        if not os.path.exists("my_app_db.sqlite3"):
            db.create_all()
    
    app.app_context().push()

    return


initial_Setup()

from backend.routes import *
# Customer1 = User(name = "Himanshu",email="Himanshu@gmail.com",password="xyz",status = "Active")

# db.session.add(Customer1)
# db.session.commit()
# booking1 = Booking(   professional_id=1 , customer_id = 1)
# db.session.add(booking1)
# db.session.commit()

# Customer1 = db.session.query(User).filter_by(id = 1).first()
# print(Customer1.sent_booking[1].prof.name)

if __name__ == "__main__":
    app.run(debug=True)