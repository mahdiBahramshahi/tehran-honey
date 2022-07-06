from flask import Flask , render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Development


app = Flask(__name__)
app.config.from_object(Development)

db = SQLAlchemy(app)

migrate = Migrate(app , db)


from mod_users import users
app.register_blueprint(users)

from mod_admin import admin
app.register_blueprint(admin)

from mod_uploads import uploads
app.register_blueprint(uploads)

from mod_mahsolat import mahsolat
app.register_blueprint(mahsolat)


from views import app
