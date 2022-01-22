import cloudinary
from os import getenv
from flask import Flask
from dotenv import load_dotenv
from ssims.config import Config
from flaskext.mysql import MySQL

load_dotenv()

cloudinary.config(
            cloud_name=getenv("CLOUD_NAME"),
            api_key=getenv("API_KEY"),
            api_secret=getenv("API_SECRET"),
            secure=getenv("API_SECRET"))

my_sql = MySQL()

def create_app(test_config=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    my_sql.init_app(app)


    from ssims.colleges.routes import college
    from ssims.students.routes import student
    from ssims.courses.routes import course


    app.register_blueprint(college)
    app.register_blueprint(student)
    app.register_blueprint(course)

    return app