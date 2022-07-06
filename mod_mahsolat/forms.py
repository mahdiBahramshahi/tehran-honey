from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import FileField , SelectField , StringField , BooleanField , SubmitField
from mod_mahsolat.models import MahsolGroups

class MahsolatForms(FlaskForm):
    mahsol_title = StringField(validators=[DataRequired()])
    description = StringField(validators=[DataRequired()])


    @property
    def groups(self):
        return MahsolGroups.query.order_by(MahsolGroups.id.desc()).all()

        
    mahsol_category = SelectField(u'mahsol category', choices=[('-', '-'),('', '')])
    mahsol_price_1kg = StringField(validators=[DataRequired()])
    mahsol_price_05kg = StringField(validators=[DataRequired()])
    mahsol_description = StringField(validators=[DataRequired()])
    mahsol_image = StringField(validators=[DataRequired()])
    
    royesh_giah = StringField(validators=[DataRequired()])
    tarigh_masraf = StringField(validators=[DataRequired()])
    rang_asal = StringField(validators=[DataRequired()])
    bastebandi = StringField(validators=[DataRequired()])
    manh_masraf = StringField(validators=[DataRequired()])
    khavas_darmani = StringField(validators=[DataRequired()])





class RoyalForms(FlaskForm):
    mahsol_title = StringField(validators=[DataRequired()])
    description = StringField(validators=[DataRequired()])


    @property
    def groups(self):
        return MahsolGroups.query.order_by(MahsolGroups.id.desc()).all()

        
    mahsol_category = SelectField(u'mahsol category', choices=[('-', '-'),('', '')])
    mahsol_price = StringField(validators=[DataRequired()])
    mahsol_description = StringField(validators=[DataRequired()])
    mahsol_image = StringField(validators=[DataRequired()])
    tarigh_masraf = StringField(validators=[DataRequired()])
    bastebandi = StringField(validators=[DataRequired()])
    manh_masraf = StringField(validators=[DataRequired()])
    khavas_darmani = StringField(validators=[DataRequired()])




class BaremoomForms(FlaskForm):
    mahsol_title = StringField(validators=[DataRequired()])
    description = StringField(validators=[DataRequired()])


    @property
    def groups(self):
        return MahsolGroups.query.order_by(MahsolGroups.id.desc()).all()

    
    mahsol_category = SelectField(u'mahsol category', choices=[('-', '-'),('', '')])
    hallal= StringField(validators=[DataRequired()])
    mahsol_price_100g = StringField(validators=[DataRequired()])
    mahsol_price_50g = StringField(validators=[DataRequired()])
    mahsol_description = StringField(validators=[DataRequired()])
    mahsol_image = StringField(validators=[DataRequired()])
    tarigh_masraf = StringField(validators=[DataRequired()])
    bastebandi = StringField(validators=[DataRequired()])
    manh_masraf = StringField(validators=[DataRequired()])
    khavas_darmani = StringField(validators=[DataRequired()])


class GardeForm(FlaskForm):
    mahsol_title = StringField(validators=[DataRequired()])
    description = StringField(validators=[DataRequired()])


    @property
    def groups(self):
        return MahsolGroups.query.order_by(MahsolGroups.id.desc()).all()

        
    mahsol_category = SelectField(u'mahsol category', choices=[('-', '-'),('', '')])
    mahsol_price_100g = StringField(validators=[DataRequired()])
    mahsol_price_50g = StringField(validators=[DataRequired()])
    mahsol_description = StringField(validators=[DataRequired()])
    mahsol_image = StringField(validators=[DataRequired()])
    tarigh_masraf = StringField(validators=[DataRequired()])
    bastebandi = StringField(validators=[DataRequired()])
    manh_masraf = StringField(validators=[DataRequired()])
    khavas_darmani = StringField(validators=[DataRequired()])


class GiftpackForm(FlaskForm):
    price = StringField(validators=[DataRequired()])



class MahsolgroupForms(FlaskForm):
    group_name = StringField(validators=[DataRequired()])
    group_image = FileField(validators=[DataRequired()])
    group_description =StringField(validators=[DataRequired()])




class SearchForm(FlaskForm):
    search_query = StringField(validators=[DataRequired()])
