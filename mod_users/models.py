import email
from email.mime import image
from app import db
from sqlalchemy import Column , Integer , String
from werkzeug.security import generate_password_hash , check_password_hash


class User(db.Model):
    __tablename__='users'
    id = Column(Integer(), primary_key=True)
    username = Column(String(128),nullable=False, unique=True)
    email = Column(String(128),nullable=False, unique=False)
    password = Column(String(128),nullable=False, unique=False)
    role = Column(Integer(),nullable=False, default=0)
    
    def set_password(self,password):
        self.password = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password ,password)

    def is_admin(self):
        return self.role == 1



class Slider(db.Model):
    __tablename__='sliders'
    id = Column(Integer(), primary_key=True)
    title = Column(String(128),nullable=False, unique=False)
    image = Column(String(512) , nullable=False , unique= True)
    link = Column(String(128),nullable=False, unique=False)


class Card(db.Model):
    __tablename__='card'
    id = Column(Integer(), primary_key=True)
    username = Column(String(128),nullable=False, unique=False)
    email = Column(String(128),nullable=False, unique=False)
    mahsol_title = Column(String(128) , nullable=False , unique=False)
    mahsol_count = Column(String(128) , nullable=False , unique=False)
    mahsol_card_id = Column(String(16), nullable=True , unique=False)
    mahsol_description = Column(String(256) , nullable=False , unique= False)
    mahsol_slug = Column(String(128) , nullable=False , unique= False)             
    mahsol_group = Column(String(128) , nullable=False , unique= False)                
    mahsol_price = Column(String(128) , nullable=False , unique= False)                
    mahsol_image = Column(String(128) , nullable=False , unique=False)
    mahsol_role =  Column(Integer(),nullable=False, unique=False)


class Monasebat(db.Model):
    __tablename__ = 'monasebat'
    id = Column(Integer(), primary_key=True)
    title = Column(String(128) , nullable=False , unique=False)
    image = Column(String(128) , nullable=False , unique=False)
    link = Column(String(128),nullable=False, unique=False)


class Blog(db.Model):
    __tablename__='blogs'
    id = Column(Integer(), primary_key=True)
    title = Column(String(128),nullable=False, unique=True)
    image = Column(String(512) , nullable=False , unique= False)
    slug = Column(String(128) , nullable=False , unique= True)
    group_mortabet = Column(String(512) , nullable=True , unique= False)
    content = Column(String(3000), nullable=False, unique=False)
    metacontent = Column(String(128), nullable=False, unique=False)
    writer = Column(String(128) , nullable=False , unique= False)
    date = Column(String(32) , nullable=False , unique= False)
