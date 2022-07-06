from flask import Blueprint

mahsolat = Blueprint('mahsolat',__name__,url_prefix='/mahsolat/')

from . import views


