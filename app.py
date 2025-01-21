from flask import Flask
from backend.models import db

app = None

def initial_Setup():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///my_app_db.sqlite3"
    db.init_app(app)
    app.app_context().push()
    return


initial_Setup()

from backend.routes import *

if __name__ == "__main__":
    app.run(debug=True)