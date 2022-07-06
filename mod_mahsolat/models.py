from sqlalchemy import Column , Integer , String , Text, column, true
from app import db

class Mahsolat(db.Model):
    __tablename__='mahsolat'
    id = Column(Integer , primary_key=True)
    title = Column(String(128) , nullable=False , unique= True)
    description = Column(String(1024) , nullable=False , unique= False)
    royesh_giah = Column(String(128) , nullable=False , unique= False)
    tarigh_masraf = Column(String(128) , nullable=False , unique= False)
    rang_asal = Column(String(128) , nullable=False , unique= False)
    bastebandi = Column(String(128) , nullable=False , unique= False)
    manh_masraf = Column(String(128) , nullable=False , unique= False)
    khavas_darmani = Column(String(128) , nullable=False , unique= False)
    slug = Column(String(128) , nullable=False , unique= True)
    group = Column(String(128) , nullable=False , unique= False)
    price_1kg = Column(String(128) , nullable=False , unique= False)
    price_05kg = Column(String(128) , nullable=False , unique= False)
    image = Column(String(512) , nullable=False , unique=False)
    role = Column(Integer(),nullable=False, default=0)


class Royal(db.Model):
    __tablename__='royal_jelly'
    id = Column(Integer , primary_key=True)
    title = Column(String(128) , nullable=False , unique= True)
    description = Column(String(1024) , nullable=False , unique= False)
    tarigh_masraf = Column(String(128) , nullable=False , unique= False)
    bastebandi = Column(String(128) , nullable=False , unique= False)
    manh_masraf = Column(String(128) , nullable=False , unique= False)
    khavas_darmani = Column(String(128) , nullable=False , unique= False)
    slug = Column(String(128) , nullable=False , unique= True)
    group = Column(String(128) , nullable=False , unique= False)
    price = Column(String(128) , nullable=False , unique= False)
    image = Column(String(512) , nullable=False , unique=False)
    role = Column(Integer(),nullable=False, default=1)



class Baremoom(db.Model):
    __tablename__='Baremoom'
    id = Column(Integer , primary_key=True)
    title = Column(String(128) , nullable=False , unique= True)
    description = Column(String(1024) , nullable=False , unique= False)
    tarigh_masraf = Column(String(128) , nullable=False , unique= False)
    hallal = Column(String(128) , nullable=False , unique= False)
    bastebandi = Column(String(128) , nullable=False , unique= False)
    manh_masraf = Column(String(128) , nullable=False , unique= False)
    khavas_darmani = Column(String(128) , nullable=False , unique= False)
    slug = Column(String(128) , nullable=False , unique= True)
    group = Column(String(128) , nullable=False , unique= False)
    price_100g = Column(String(128) , nullable=False , unique= False)
    price_50g = Column(String(128) , nullable=False , unique= False)
    image = Column(String(512) , nullable=False , unique=False)
    role = Column(Integer(),nullable=False, default=2)



class Garde(db.Model):
    __tablename__='garde_gol'
    id = Column(Integer , primary_key=True)
    title = Column(String(128) , nullable=False , unique= True)
    description = Column(String(1024) , nullable=False , unique= False)
    tarigh_masraf = Column(String(128) , nullable=False , unique= False)
    bastebandi = Column(String(128) , nullable=False , unique= False)
    manh_masraf = Column(String(128) , nullable=False , unique= False)
    khavas_darmani = Column(String(128) , nullable=False , unique= False)
    slug = Column(String(128) , nullable=False , unique= True)
    group = Column(String(128) , nullable=False , unique= False)
    price_100g = Column(String(128) , nullable=False , unique= False)
    price_50g = Column(String(128) , nullable=False , unique= False)
    image = Column(String(512) , nullable=False , unique=False)
    role = Column(Integer(),nullable=False, default=3)






class GiftPack(db.Model):
    __tablename__='gift_pack'
    id = Column(Integer , primary_key=True)
    price= Column(String(128) , nullable=False , unique= False)
    role = Column(Integer(),nullable=False, default=3)


class MahsolGroups(db.Model):
    __tablename__='mahsolgroups'
    id = Column(Integer , primary_key=True)
    title = Column(String(32) , nullable=False , unique= True)
    description = Column(String(64) , nullable=False , unique= False)
    slug = Column(String(32) , nullable=False , unique= True)
    image = Column(String(512) , nullable=False , unique= True)
    image_urlfor=Column(String(512) , nullable=False , unique= False)


class GiftpackRegister(db.Model):
    __tablename__='GiftpackRegister'
    id = Column(Integer , primary_key=True)
    username = Column(String(128),nullable=False, unique=False)
    title_1 = Column(String(128),nullable=False, unique=False)
    title_2 = Column(String(128),nullable=False, unique=False)
    title_3 = Column(String(128),nullable=False, unique=False)
    title_4 = Column(String(128),nullable=False, unique=False)
    title_5 = Column(String(128),nullable=False, unique=False)
    price_1 = Column(String(128),nullable=False, unique=False)
    price_2 = Column(String(128),nullable=False, unique=False)
    price_3 = Column(String(128),nullable=False, unique=False)
    price_4 = Column(String(128),nullable=False, unique=False)
    price_5 = Column(String(128),nullable=False, unique=False)
    image = Column(String(128),nullable=False, unique=False)
    bastebandi_color = Column(String(128) , nullable=False , unique= False)
    slug = Column(String(128) , nullable=False , unique= True)
    role = Column(Integer(),nullable=False, default=4)






