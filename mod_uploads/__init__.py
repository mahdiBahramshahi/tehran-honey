from flask import Blueprint


uploads = Blueprint('uploads' , __name__ , url_prefix='/uploads/')

from . import models
