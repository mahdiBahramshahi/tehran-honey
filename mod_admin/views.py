from crypt import methods

from pymysql import IntegrityError
from . import admin
from .utils import admin_only_view
from flask import render_template , session , flash , redirect , url_for , request
from mod_mahsolat.models import Mahsolat , MahsolGroups , Royal , Garde , Baremoom , GiftPack
from mod_mahsolat.forms import MahsolatForms , MahsolgroupForms , RoyalForms , BaremoomForms , GardeForm , GiftpackForm
from app import db
from werkzeug.utils import secure_filename
import uuid
from mod_users.models import User
from unidecode import unidecode
from mod_users.models import Slider , Monasebat , Blog , Card
from mod_users.forms import SliderForm , MonasebatForm , BlogForm
from .date import ShowTodayFull



@admin.route('/')
@admin_only_view
def index():
    return render_template('admin/index.html')


@admin.route('/mahsolat/' ,methods=['GET', 'POST'])
@admin_only_view
def mahsolat():
    form = MahsolatForms()    
    all_mahsolat = Mahsolat.query.order_by(Mahsolat.id.desc()).all()
    groups = MahsolGroups.query.order_by(MahsolGroups.id).all()
    # .filter(Mahsolat.username == session.get('username'))
    return render_template('admin/mahsolat.html' , form = form , all_mahsolat = all_mahsolat , groups=groups)



@admin.route('/create_mahsol/' , methods=['GET', 'POST'])
@admin_only_view
def create_mahsol():
    form = MahsolatForms() 
    if request.method == 'POST':
        if not session.get('email'):
            flash(' شما حساب کاربری ندارید. ابتدا در این صفحه وارد حساب کاربری تان شوید', category='bg-danger')
            return redirect(url_for('users.login')) 
        
        old_title = Mahsolat.query.filter(Mahsolat.title.ilike(form.mahsol_title.data)).first()
        if old_title:
            flash('نام محصول تکراری میباشد' , 'bg-danger')
            return redirect(url_for('admin.mahsolat'))

        session['mahsol_title'] = request.form.get('mahsol_title')    
        session['mahsol_category'] = request.form.get('mahsol_category')
        session['mahsol_price_1kg'] = request.form.get('mahsol_price_1kg')
        session['mahsol_price_0.5kg'] = request.form.get('mahsol_price_0.5kg')
    
        print(session.get('mahsol_title'))
        print(session.get('mahsol_category'))
        print(session.get('mahsol_price_1kg'))
        print(session.get('mahsol_price_0.5kg'))

        if not session.get('mahsol_title'):
            flash('لطفا فرم را کامل پر کنید', category='bg-danger')
            return render_template('admin/mahsolat.html' , form = form)
    
        if not session.get('mahsol_category'):
            flash('لطفا فرم را کامل پر کنید', category='bg-danger')
            return render_template('admin/mahsolat.html' , form = form)

    
        if not session.get('mahsol_price_1kg'):
            flash('لطفا فرم را کامل پر کنید', category='bg-danger')
            return render_template('admin/mahsolat.html' , form = form)
        
        if not session.get('mahsol_price_0.5kg'):
            flash('لطفا فرم را کامل پر کنید', category='bg-danger')
            return render_template('admin/mahsolat.html' , form = form)
        
    all_mahsolat = Mahsolat.query.order_by(Mahsolat.id.desc()).all()
    groups = MahsolGroups.query.order_by(MahsolGroups.id.desc()).all()
     



    return render_template('admin/create_mahsol.html' , form = form , all_mahsolat = all_mahsolat , groups=groups)



@admin.route('/register_mahsol/', methods=['GET', 'POST'])
@admin_only_view
def register_mahsol():
    form = MahsolatForms()
    if request.method == 'POST':
        if not session.get('email'):
            flash(' شما حساب کاربری ندارید. ابتدا در این صفحه وارد حساب کاربری تان شوید', category='bg-danger')
            return redirect(url_for('users.login')) 
        old_title = Mahsolat.query.filter(Mahsolat.title.ilike(form.mahsol_title.data)).first()
        if old_title:
            flash('نام محصول تکراری میباشد' , 'bg-danger')
            return render_template('admin/mahsolat.html', form=form)

        filename=f"{uuid.uuid1()}_{secure_filename(form.mahsol_image.data.filename)}"
        file_url = f'uploads/{filename}'

        price_1 = unidecode(form.mahsol_price_1kg.data)
        price_05 = unidecode(form.mahsol_price_05kg.data)


        new_mahsol = Mahsolat()
        new_mahsol.title = form.mahsol_title.data
        new_mahsol.description = form.mahsol_description.data
        new_mahsol.group = form.mahsol_category.data
        new_mahsol.price_1kg = price_1
        new_mahsol.price_05kg = price_05
        new_mahsol.image = file_url
        new_mahsol.slug = form.mahsol_title.data
        new_mahsol.royesh_giah = form.royesh_giah.data
        new_mahsol.rang_asal = form.rang_asal.data
        new_mahsol.bastebandi = form.bastebandi.data
        new_mahsol.manh_masraf = form.manh_masraf.data
        new_mahsol.khavas_darmani = form.khavas_darmani.data
        new_mahsol.tarigh_masraf = form.tarigh_masraf.data

        db.session.add(new_mahsol)
        db.session.commit()
        print(form.mahsol_image.data)

        form.mahsol_image.data.save(f"static/uploads/{filename}")    

        flash('محصول با موفقیت ثبت شد', category='bg-success')
        return redirect(url_for('admin.mahsolat'))

    return render_template('admin/create_mahsol.html' , form = form)




@admin.route('/<string:slug>' , methods=['GET' , 'POST'])
@admin_only_view
def single_mahsol(slug):
    form = MahsolatForms()
    mahsol = Mahsolat.query.filter(Mahsolat.slug == slug).first_or_404()
    if request.method == 'POST':
        if not session.get('email'):
            flash(' شما حساب کاربری ندارید. ابتدا در این صفحه وارد حساب کاربری تان شوید', category='bg-danger')
            return redirect(url_for('users.login')) 
        # old_title = Mahsolat.query.filter(Mahsolat.title.ilike(form.mahsol_title.data)).first()
        # if old_title:
        #     flash('نام محصول تکراری میباشد' , 'bg-danger')
        #     return render_template('admin/mahsolat.html', form=form)


        price_1 = unidecode(form.mahsol_price_1kg.data)
        price_05 = unidecode(form.mahsol_price_05kg.data)
        mahsol.title = form.mahsol_title.data
        mahsol.description = form.mahsol_description.data
        mahsol.group = form.mahsol_category.data
        mahsol.price_1kg = price_1
        mahsol.price_05kg = price_05


        if form.mahsol_image.data.filename:
            filename=f"{uuid.uuid1()}_{secure_filename(form.mahsol_image.data.filename)}"
            file_url = f'uploads/{filename}'
            mahsol.image = file_url
        else:
            mahsol.image = mahsol.image


        mahsol.slug = form.mahsol_title.data
        mahsol.royesh_giah = form.royesh_giah.data
        mahsol.rang_asal = form.rang_asal.data
        mahsol.bastebandi = form.bastebandi.data
        mahsol.manh_masraf = form.manh_masraf.data
        mahsol.khavas_darmani = form.khavas_darmani.data
        mahsol.tarigh_masraf = form.tarigh_masraf.data
        try:
            db.session.commit()
        except IntegrityError:
            flash('نام محصول تکراری میباشد' , category='bg-danger')

        if form.mahsol_image.data.filename:
            form.mahsol_image.data.save(f"static/uploads/{filename}")

        flash('محصول با موفقیت ثبت شد', category='bg-success')
        return redirect(url_for('admin.mahsolat'))
    return render_template('admin/single_mahsol.html' , mahsol=mahsol )








@admin.route('/mahsolat/delete/<int:mahsol_id>' , methods=['GET' , 'POST'])
@admin_only_view
def delete_mahsol(mahsol_id):
    # mahsol= Mahsolat.query.filter(Mahsolat.id == mahsol_id).first()
    mahsol_id= Mahsolat.query.get_or_404(mahsol_id)
    # mahsol_card = Card.query.filter(Card.mahsol_title == mahsol.title).first()
    # card_id= mahsol_card.id

    # db.session.delete(card_id)
    db.session.delete(mahsol_id)
    db.session.commit()
    flash('محصول با موفقیت حذف شد.' , 'bg-success')
    return redirect(url_for('admin.mahsolat'))




























@admin.route('/royal_jelly/' ,methods=['GET', 'POST'])
@admin_only_view
def royal():
    form = RoyalForms()    
    all_mahsolat = Royal.query.order_by(Royal.id.desc()).all()
    groups = MahsolGroups.query.order_by(MahsolGroups.id).all()
    # .filter(Mahsolat.username == session.get('username'))
    return render_template('admin/royal_jelly.html' , form = form , all_mahsolat = all_mahsolat , groups=groups)



@admin.route('/create_Royal/' , methods=['GET', 'POST'])
@admin_only_view
def create_royal():
    form = RoyalForms() 
    if request.method == 'POST':
        old_title = Royal.query.filter(Royal.title.ilike(form.mahsol_title.data)).first()
        if old_title:
            flash('نام محصول تکراری میباشد' , 'bg-danger')
            return redirect(url_for('admin.royal'))

        session['mahsol_title'] = request.form.get('mahsol_title')    
        session['mahsol_category'] = request.form.get('mahsol_category')
        session['mahsol_price'] = request.form.get('mahsol_price')

        if not session.get('mahsol_title'):
            flash('لطفا فرم را کامل پر کنید', category='bg-danger')
            return render_template('admin/royal_jelly.html' , form = form)
    
        if not session.get('mahsol_category'):
            flash('لطفا فرم را کامل پر کنید', category='bg-danger')
            return render_template('admin/royal_jelly.html' , form = form)


    
        if not session.get('mahsol_price'):
            flash('لطفا فرم را کامل پر کنید', category='bg-danger')
            return render_template('admin/royal_jelly.html' , form = form)


        
    all_mahsolat = Royal.query.order_by(Royal.id.desc()).all()
    groups = Royal.query.order_by(Royal.id.desc()).all()
     



    return render_template('admin/create_royal.html' , form = form , all_mahsolat = all_mahsolat , groups=groups)



@admin.route('/register_royal/', methods=['GET', 'POST'])
@admin_only_view
def register_royal():
    form = RoyalForms()
    if request.method == 'POST':
        old_title = Royal.query.filter(Royal.title.ilike(form.mahsol_title.data)).first()
        if old_title:
            flash('نام محصول تکراری میباشد' , 'bg-danger')
            return redirect(url_for('admin.royal'))

        filename=f"{uuid.uuid1()}_{secure_filename(form.mahsol_image.data.filename)}"
        file_url = f'uploads/{filename}'

        price = unidecode(form.mahsol_price.data)


        new_mahsol = Royal()
        new_mahsol.title = form.mahsol_title.data
        new_mahsol.description = form.mahsol_description.data
        new_mahsol.group = form.mahsol_category.data
        new_mahsol.price = price
        new_mahsol.image = file_url
        new_mahsol.slug = form.mahsol_title.data
        new_mahsol.bastebandi = form.bastebandi.data
        new_mahsol.manh_masraf = form.manh_masraf.data
        new_mahsol.khavas_darmani = form.khavas_darmani.data
        new_mahsol.tarigh_masraf = form.tarigh_masraf.data

        db.session.add(new_mahsol)
        db.session.commit()

        form.mahsol_image.data.save(f"static/uploads/{filename}")    

        flash('محصول با موفقیت ثبت شد', category='bg-success')
        return redirect(url_for('admin.royal'))

    return render_template('admin/create_Royal.html' , form = form)




@admin.route('/royal_jelly/<string:slug>' , methods=['GET' , 'POST'])
@admin_only_view
def single_royal(slug):
    form = RoyalForms()
    mahsol = Royal.query.filter(Royal.slug == slug).first_or_404()
    if request.method == 'POST':


        price = unidecode(form.mahsol_price.data)

        mahsol.title = form.mahsol_title.data
        mahsol.description = form.mahsol_description.data
        mahsol.group = form.mahsol_category.data
        mahsol.price = price


        if form.mahsol_image.data.filename:
            filename=f"{uuid.uuid1()}_{secure_filename(form.mahsol_image.data.filename)}"
            file_url = f'uploads/{filename}'
            mahsol.image = file_url
        else:
            mahsol.image = mahsol.image


        mahsol.slug = form.mahsol_title.data
        mahsol.bastebandi = form.bastebandi.data
        mahsol.manh_masraf = form.manh_masraf.data
        mahsol.khavas_darmani = form.khavas_darmani.data
        mahsol.tarigh_masraf = form.tarigh_masraf.data
        try:
            db.session.commit()
        except IntegrityError:
            flash('نام محصول تکراری میباشد' , category='bg-danger')

        if form.mahsol_image.data.filename:
            form.mahsol_image.data.save(f"static/uploads/{filename}")

        flash('محصول با موفقیت ثبت شد', category='bg-success')
        return redirect(url_for('admin.royal'))
    return render_template('admin/single_royal.html' , mahsol=mahsol )








@admin.route('/royal/delete/<int:mahsol_id>' , methods=['GET' , 'POST'])
@admin_only_view
def delete_royal(mahsol_id):
    mahsol_id= Royal.query.get_or_404(mahsol_id)
    db.session.delete(mahsol_id)
    db.session.commit()
    flash('محصول با موفقیت حذف شد.' , 'bg-success')
    return redirect(url_for('admin.royal'))
































@admin.route('/baremoom/' ,methods=['GET', 'POST'])
@admin_only_view
def baremoom():
    form = BaremoomForms()    
    all_mahsolat = Baremoom.query.order_by(Baremoom.id.desc()).all()
    groups = MahsolGroups.query.order_by(MahsolGroups.id).all()
    # .filter(Mahsolat.username == session.get('username'))
    return render_template('admin/baremoom.html' , form = form , all_mahsolat = all_mahsolat , groups=groups)



@admin.route('/create_baremoom/' , methods=['GET', 'POST'])
@admin_only_view
def create_baremoom():
    form = BaremoomForms() 
    if request.method == 'POST': 
        
        old_title = Baremoom.query.filter(Baremoom.title.ilike(form.mahsol_title.data)).first()
        if old_title:
            flash('نام محصول تکراری میباشد' , 'bg-danger')
            return redirect(url_for('admin.baremoom'))

        session['mahsol_title'] = request.form.get('mahsol_title')    
        session['mahsol_category'] = request.form.get('mahsol_category')
        session['mahsol_price_100g'] = request.form.get('mahsol_price_100g')
        session['mahsol_price_50g'] = request.form.get('mahsol_price_50g')
    

        if not session.get('mahsol_title'):
            flash('لطفا فرم را کامل پر کنید', category='bg-danger')
            return render_template('admin/baremoom.html' , form = form)
    
        if not session.get('mahsol_category'):
            flash('لطفا فرم را کامل پر کنید', category='bg-danger')
            return render_template('admin/baremoom.html' , form = form)
    
        if not session.get('mahsol_price_100g'):
            flash('لطفا فرم را کامل پر کنید', category='bg-danger')
            return render_template('admin/baremoom.html' , form = form)
        
        if not session.get('mahsol_price_50g'):
            flash('لطفا فرم را کامل پر کنید', category='bg-danger')
            return render_template('admin/baremoom.html' , form = form)
       
    all_mahsolat = Mahsolat.query.order_by(Mahsolat.id.desc()).all()
    baremooms = Baremoom.query.order_by(Baremoom.id.desc()).all()
    groups = MahsolGroups.query.order_by(MahsolGroups.id.desc()).all()
     



    return render_template('admin/create_baremoom.html' , form = form , all_mahsolat = all_mahsolat , groups=groups , baremooms=baremooms)



@admin.route('/register_baremoom/', methods=['GET', 'POST'])
@admin_only_view
def register_baremoom():
    form = BaremoomForms()
    if request.method == 'POST':

        old_title = Baremoom.query.filter(Baremoom.title.ilike(form.mahsol_title.data)).first()
        if old_title:
            flash('نام محصول تکراری میباشد' , 'bg-danger')
            return render_template('admin/baremoom.html', form=form)

        filename=f"{uuid.uuid1()}_{secure_filename(form.mahsol_image.data.filename)}"
        file_url = f'uploads/{filename}'

        price_100g = unidecode(form.mahsol_price_100g.data)
        price_50g = unidecode(form.mahsol_price_50g.data)


        new_mahsol = Baremoom()
        new_mahsol.title = form.mahsol_title.data
        new_mahsol.description = form.mahsol_description.data
        new_mahsol.group = form.mahsol_category.data
        new_mahsol.price_100g = price_100g
        new_mahsol.price_50g = price_50g
        new_mahsol.image = file_url
        new_mahsol.slug = form.mahsol_title.data
        new_mahsol.hallal = form.hallal.data
        new_mahsol.bastebandi = form.bastebandi.data
        new_mahsol.manh_masraf = form.manh_masraf.data
        new_mahsol.khavas_darmani = form.khavas_darmani.data
        new_mahsol.tarigh_masraf = form.tarigh_masraf.data

        db.session.add(new_mahsol)
        db.session.commit()
        print(form.mahsol_image.data)

        form.mahsol_image.data.save(f"static/uploads/{filename}")    

        flash('محصول با موفقیت ثبت شد', category='bg-success')
        return redirect(url_for('admin.baremoom'))

    return render_template('admin/create_baremoom.html' , form = form)




@admin.route('/baremoom/<string:slug>' , methods=['GET' , 'POST'])
@admin_only_view
def single_baremoom(slug):
    form = BaremoomForms()
    mahsol = Baremoom.query.filter(Baremoom.slug == slug).first_or_404()
    if request.method == 'POST':

        # old_title = Mahsolat.query.filter(Mahsolat.title.ilike(form.mahsol_title.data)).first()
        # if old_title:
        #     flash('نام محصول تکراری میباشد' , 'bg-danger')
        #     return render_template('admin/mahsolat.html', form=form)


        price_100g = unidecode(form.mahsol_price_100g.data)
        price_50g = unidecode(form.mahsol_price_50g.data)
        mahsol.title = form.mahsol_title.data
        mahsol.description = form.mahsol_description.data
        mahsol.group = form.mahsol_category.data
        mahsol.price_100g = price_100g
        mahsol.price_50g = price_50g


        if form.mahsol_image.data.filename:
            filename=f"{uuid.uuid1()}_{secure_filename(form.mahsol_image.data.filename)}"
            file_url = f'uploads/{filename}'
            mahsol.image = file_url
        else:
            mahsol.image = mahsol.image


        mahsol.slug = form.mahsol_title.data
        mahsol.hallal = form.hallal.data
        mahsol.bastebandi = form.bastebandi.data
        mahsol.manh_masraf = form.manh_masraf.data
        mahsol.khavas_darmani = form.khavas_darmani.data
        mahsol.tarigh_masraf = form.tarigh_masraf.data
        try:
            db.session.commit()
        except IntegrityError:
            flash('نام محصول تکراری میباشد' , category='bg-danger')

        if form.mahsol_image.data.filename:
            form.mahsol_image.data.save(f"static/uploads/{filename}")

        flash('تغییرات با موفقیت اعمال شد', category='bg-success')
        return redirect(url_for('admin.baremoom'))
    return render_template('admin/single_baremoom.html' , mahsol=mahsol)











@admin.route('/baremoom/delete/<int:mahsol_id>' , methods=['GET' , 'POST'])
@admin_only_view
def delete_baremoom(mahsol_id):
    mahsol_id= Baremoom.query.get_or_404(mahsol_id)
    db.session.delete(mahsol_id)
    db.session.commit()
    flash('محصول با موفقیت حذف شد.' , 'bg-success')
    return redirect(url_for('admin.baremoom'))





























@admin.route('/garde_gol/' ,methods=['GET', 'POST'])
@admin_only_view
def garde_gol():
    form = GardeForm()    
    all_mahsolat = Garde.query.order_by(Garde.id.desc()).all()
    groups = MahsolGroups.query.order_by(MahsolGroups.id).all()
    # .filter(Mahsolat.username == session.get('username'))
    return render_template('admin/garde_gol.html' , form = form , all_mahsolat = all_mahsolat , groups=groups)



@admin.route('/create_garde/' , methods=['GET', 'POST'])
@admin_only_view
def create_garde():
    form = GardeForm() 
    if request.method == 'POST': 
        
        old_title = Garde.query.filter(Garde.title.ilike(form.mahsol_title.data)).first()
        if old_title:
            flash('نام محصول تکراری میباشد' , 'bg-danger')
            return redirect(url_for('admin.garde_gol'))

        session['mahsol_title'] = request.form.get('mahsol_title')    
        session['mahsol_category'] = request.form.get('mahsol_category')
        session['mahsol_price_100g'] = request.form.get('mahsol_price_100g')
        session['mahsol_price_50g'] = request.form.get('mahsol_price_50g')
    

        if not session.get('mahsol_title'):
            flash('لطفا فرم را کامل پر کنید', category='bg-danger')
            return render_template('admin/garde_gol.html' , form = form)
    
        if not session.get('mahsol_category'):
            flash('لطفا فرم را کامل پر کنید', category='bg-danger')
            return render_template('admin/garde_gol.html' , form = form)

        if not session.get('mahsol_price_100g'):
            flash('لطفا فرم را کامل پر کنید', category='bg-danger')
            return render_template('admin/garde_gol.html' , form = form)
        
        if not session.get('mahsol_price_50g'):
            flash('لطفا فرم را کامل پر کنید', category='bg-danger')
            return render_template('admin/garde_gol.html' , form = form)
       
    all_mahsolat = Mahsolat.query.order_by(Mahsolat.id.desc()).all()
    garde_gols = Garde.query.order_by(Garde.id.desc()).all()
    groups = MahsolGroups.query.order_by(MahsolGroups.id.desc()).all()
     



    return render_template('admin/create_garde.html' , form = form , all_mahsolat = all_mahsolat , groups=groups , garde_gols=garde_gols)



@admin.route('/register_garde/', methods=['GET', 'POST'])
@admin_only_view
def register_garde():
    form = GardeForm()
    if request.method == 'POST':

        old_title = Garde.query.filter(Garde.title.ilike(form.mahsol_title.data)).first()
        if old_title:
            flash('نام محصول تکراری میباشد' , 'bg-danger')
            return render_template('admin/garde_gol.html', form=form)

        filename=f"{uuid.uuid1()}_{secure_filename(form.mahsol_image.data.filename)}"
        file_url = f'uploads/{filename}'

        price_100g = unidecode(form.mahsol_price_100g.data)
        price_50g = unidecode(form.mahsol_price_50g.data)


        new_mahsol = Garde()
        new_mahsol.title = form.mahsol_title.data
        new_mahsol.description = form.mahsol_description.data
        new_mahsol.group = form.mahsol_category.data
        new_mahsol.price_100g = price_100g
        new_mahsol.price_50g = price_50g
        new_mahsol.image = file_url
        new_mahsol.slug = form.mahsol_title.data
        new_mahsol.bastebandi = form.bastebandi.data
        new_mahsol.manh_masraf = form.manh_masraf.data
        new_mahsol.khavas_darmani = form.khavas_darmani.data
        new_mahsol.tarigh_masraf = form.tarigh_masraf.data

        db.session.add(new_mahsol)
        db.session.commit()
        print(form.mahsol_image.data)

        form.mahsol_image.data.save(f"static/uploads/{filename}")    

        flash('محصول با موفقیت ثبت شد', category='bg-success')
        return redirect(url_for('admin.garde_gol'))

    return render_template('admin/garde_gol.html' , form = form)




@admin.route('/garde_gol/<string:slug>' , methods=['GET' , 'POST'])
@admin_only_view
def single_garde(slug):
    form = GardeForm()
    mahsol = Garde.query.filter(Garde.slug == slug).first_or_404()
    if request.method == 'POST':

        # old_title = Mahsolat.query.filter(Mahsolat.title.ilike(form.mahsol_title.data)).first()
        # if old_title:
        #     flash('نام محصول تکراری میباشد' , 'bg-danger')
        #     return render_template('admin/mahsolat.html', form=form)


        price_100g = unidecode(form.mahsol_price_100g.data)
        price_50g = unidecode(form.mahsol_price_50g.data)
        mahsol.title = form.mahsol_title.data
        mahsol.description = form.mahsol_description.data
        mahsol.group = form.mahsol_category.data
        mahsol.price_100g = price_100g
        mahsol.price_50g = price_50g


        if form.mahsol_image.data.filename:
            filename=f"{uuid.uuid1()}_{secure_filename(form.mahsol_image.data.filename)}"
            file_url = f'uploads/{filename}'
            mahsol.image = file_url
        else:
            mahsol.image = mahsol.image


        mahsol.slug = form.mahsol_title.data
        mahsol.bastebandi = form.bastebandi.data
        mahsol.manh_masraf = form.manh_masraf.data
        mahsol.khavas_darmani = form.khavas_darmani.data
        mahsol.tarigh_masraf = form.tarigh_masraf.data
        try:
            db.session.commit()
        except IntegrityError:
            flash('نام محصول تکراری میباشد' , category='bg-danger')

        if form.mahsol_image.data.filename:
            form.mahsol_image.data.save(f"static/uploads/{filename}")

        flash('تغییرات با موفقیت اعمال شد', category='bg-success')
        return redirect(url_for('admin.garde_gol'))
    return render_template('admin/single_garde.html' , mahsol=mahsol)











@admin.route('/garde_gol/delete/<int:mahsol_id>' , methods=['GET' , 'POST'])
@admin_only_view
def delete_garde(mahsol_id):
    mahsol_id= Garde.query.get_or_404(mahsol_id)
    db.session.delete(mahsol_id)
    db.session.commit()
    flash('محصول با موفقیت حذف شد.' , 'bg-success')
    return redirect(url_for('admin.garde_gol'))








































@admin.route('/mahsol_groups' , methods=['GET', 'POST'])
@admin_only_view
def mahsol_group():
    groups = MahsolGroups.query.order_by(MahsolGroups.id.desc()).all()
    form = MahsolgroupForms()
    if not session.get('email'):
        flash(' شما حساب کاربری ندارید. ابتدا در این صفحه وارد حساب کاربری تان شوید', category='bg-danger')
        return redirect(url_for('users.login')) 

    
    return render_template('admin/mahsol_group.html' , groups=groups , form=form)





@admin.route('/create_mahsol_groups' , methods=['GET', 'POST'])
@admin_only_view
def create_mahsol_group():
    form = MahsolgroupForms() 


    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('مقادیر وارد شده صحیح نیست', category='bg-danger')
            return redirect(url_for('admin.mahsol_group'))             


        old_title = MahsolGroups.query.filter(MahsolGroups.title.ilike(form.group_name.data)).first()
        if old_title:
            flash('نام دسته بندی تکراری میباشد' , 'bg-danger')
            return redirect(url_for('admin.mahsol_group'))

        filename=f"{uuid.uuid1()}_{secure_filename(form.group_image.data.filename)}"
        file_url = f'uploads/{filename}'

        new_group = MahsolGroups()
        new_group.title = request.form.get('group_name')
        new_group.slug = request.form.get('group_name')
        new_group.description = request.form.get('group_description')
        new_group.image= filename
        new_group.image_urlfor = file_url

        print(new_group.image)

        db.session.add(new_group)
        db.session.commit()

        form.group_image.data.save(f"static/uploads/{filename}")

        flash('دسته بندی با موفقیت ثبت شد', category='bg-success')
        return redirect(url_for('admin.mahsol_group'))

    

    return render_template('admin/mahsol_group.html')


@admin.route('/mahsol_groups/delete/<int:mahsolgroup_id>' , methods=['GET' , 'POST'])
@admin_only_view
def delete_mahsolgroup(mahsolgroup_id):
    mahsol_group= MahsolGroups.query.get_or_404(mahsolgroup_id)
    db.session.delete(mahsol_group)
    db.session.commit()
    flash('دسته بندی با موفقیت حذف شد.' , 'bg-success')
    return redirect(url_for('admin.mahsol_group'))



@admin.route('/<string:slug>/')
@admin_only_view
def single_group(slug):
    all_group = MahsolGroups.query.filter(MahsolGroups.title == slug).first_or_404()
    return render_template('admin/single_group.html' , all_group=all_group )





@admin.route('/list_users')
@admin_only_view
def list_users():
    users = User.query.order_by(User.id.desc()).all()
    return render_template('admin/list_users.html' , users=users)


@admin.route('/sliders')
@admin_only_view
def sliders():
    form = SliderForm()
    sliders = Slider.query.order_by(Slider.id.desc()).all()
    
    return render_template('admin/sliders.html' , sliders=sliders , form=form)



@admin.route('/create_slider' , methods=['GET' , 'POST'])
@admin_only_view
def create_slider():
    form = SliderForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('مقادیر وارد شده صحیح نیست', category='bg-danger')
            return redirect(url_for('admin.sliders'))
        
        old_title = Slider.query.filter(Slider.title.ilike(form.slider_title.data)).first()
        if old_title:
            flash('نام اسلایدر تکراری میباشد' , 'bg-danger')
            return redirect(url_for('admin.sliders'))

        filename=f"{uuid.uuid1()}_{secure_filename(form.slider_image.data.filename)}"
        file_url = f'uploads/{filename}'

        new_slider = Slider()
        new_slider.title = request.form.get('slider_title')
        new_slider.link = request.form.get('slider_link')
        new_slider.image= file_url


        db.session.add(new_slider)
        db.session.commit()

        form.slider_image.data.save(f"static/uploads/{filename}")

        flash('اسلایدر با موفقیت ثبت شد', category='bg-success')
        return redirect(url_for('admin.sliders'))



@admin.route('/sliders/delete/<int:slider_id>' , methods=['GET' , 'POST'])
@admin_only_view
def delete_slider(slider_id):
    slider= Slider.query.get_or_404(slider_id)
    db.session.delete(slider)
    db.session.commit()
    flash('اسلایدر با موفقیت حذف شد.' , 'bg-success')
    return redirect(url_for('admin.sliders'))



@admin.route('/monasebatha')
@admin_only_view
def monasebat():
    form = MonasebatForm()
    monasebat = Monasebat.query.order_by(Monasebat.id.desc()).all()
    
    return render_template('admin/monasebat.html' , monasebat=monasebat , form=form)



@admin.route('/create_monasebat' , methods=['GET' , 'POST'])
@admin_only_view
def create_monasebat():
    form = MonasebatForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('مقادیر وارد شده صحیح نیست', category='bg-danger')
            return redirect(url_for('admin.monasebat'))
        
        old_title = Monasebat.query.filter(Monasebat.title.ilike(form.monasebat_title.data)).first()
        if old_title:
            flash('نام مناسبت تکراری میباشد' , 'bg-danger')
            return redirect(url_for('admin.monasebat'))


        filename=f"{uuid.uuid1()}_{secure_filename(form.monasebat_image.data.filename)}"
        file_url = f'uploads/{filename}'

        new_monasebat = Monasebat()
        new_monasebat.title = request.form.get('monasebat_title')
        new_monasebat.link = request.form.get('monasebat_link')
        new_monasebat.image= file_url


        db.session.add(new_monasebat)
        db.session.commit()

        form.monasebat_image.data.save(f"static/uploads/{filename}")

        flash('مناسبت با موفقیت ثبت شد', category='bg-success')
        return redirect(url_for('admin.monasebat'))


@admin.route('/monasebat/delete/<int:monasebat_id>' , methods=['GET' , 'POST'])
@admin_only_view
def delete_monasebat(monasebat_id):
    monasebat= Monasebat.query.get_or_404(monasebat_id)
    db.session.delete(monasebat)
    db.session.commit()
    flash('اسلایدر با موفقیت حذف شد.' , 'bg-success')
    return redirect(url_for('admin.monasebat'))



@admin.route('/blogs/' ,methods=['GET', 'POST'])
@admin_only_view
def blogs():
    form = BlogForm()
    # all_mahsolat = Mahsolat.query.order_by(Mahsolat.id.desc()).all()
    all_blogs = Blog.query.order_by(Blog.id.desc()).all()
    groups = MahsolGroups.query.order_by(MahsolGroups.id).all()
    return render_template('admin/blogs.html' , form = form , all_blogs=all_blogs , groups=groups)



@admin.route('/create_blog/', methods=['GET', 'POST'])
@admin_only_view
def create_blog():
    form = BlogForm() 
    all_blogs = Blog.query.order_by(Blog.id.desc()).all()
    groups = MahsolGroups.query.order_by(MahsolGroups.id).all()
    if request.method == 'POST':
        if not session.get('email'):
            flash(' شما حساب کاربری ندارید. ابتدا در این صفحه وارد حساب کاربری تان شوید', category='bg-danger')
            return redirect(url_for('users.login')) 
        
        old_title = Blog.query.filter(Blog.title.ilike(form.blog_title.data)).first()
        if old_title:
            flash('عنوان مقاله تکراری میباشد' , 'bg-danger')
            return redirect(url_for('admin.blogs'))
        session['blog_title'] = request.form.get('blog_title')    
        session['blog_writer'] = request.form.get('blog_writer')
        session['blog_group_mortabet'] = request.form.get('blog_group_mortabet')

    
    
        if not session.get('blog_title'):
            flash('لطفا فرم را کامل پر کنید', category='bg-danger')
            return render_template('admin/blogs.html' , form = form , all_blogs=all_blogs , groups=groups)
    
        if not session.get('blog_writer'):
            flash('لطفا فرم را کامل پر کنید', category='bg-danger')
            return render_template('admin/blogs.html' , form = form , all_blogs=all_blogs , groups=groups)

        
        if not session.get('blog_group_mortabet'):
            flash('لطفا فرم را کامل پر کنید', category='bg-danger')
            return render_template('admin/blogs.html' , form = form , all_blogs=all_blogs , groups=groups)

        if session.get('blog_title') and session.get('blog_writer') and session.get('blog_group_mortabet'):
            return render_template('admin/create_blog.html')
        print(session.get('blog_title'))

        return render_template('admin/create_blog.html' , form = form , all_blogs=all_blogs , groups=groups)


@admin.route('/register_blog/', methods=['GET', 'POST'])
@admin_only_view
def register_blog():
    form = BlogForm()
    if request.method == 'POST':
        old_title = Blog.query.filter(Blog.title.ilike(form.blog_title.data)).first()
        if old_title:
            flash('عنوان مقاله تکراری میباشد' , 'bg-danger')
            return render_template('admin/blogs.html', form=form)


        filename=f"{uuid.uuid1()}_{secure_filename(form.blog_image.data.filename)}"
        file_url = f'uploads/{filename}'


        

        new_blog = Blog()
        new_blog.title = form.blog_title.data
        new_blog.slug = form.blog_title.data
        new_blog.image = file_url
        new_blog.metacontent = form.blog_metacontent.data
        new_blog.group_mortabet = form.blog_group_mortabet.data
        new_blog.content = form.blog_content.data
        new_blog.writer = form.blog_writer.data
        new_blog.date = ShowTodayFull()
        db.session.add(new_blog)    
        db.session.commit()
        
        form.blog_image.data.save(f"static/uploads/{filename}")
        flash('مقاله با موفقیت ثبت شد', category='bg-success')
        return redirect(url_for('admin.blogs'))
    
    return render_template('admin/create_mahsol.html' , form = form)



@admin.route('/ادمین/<string:slug>' , methods=['GET' , 'POST'])
@admin_only_view
def single_blog(slug):
    form = BlogForm()
    blog = Blog.query.filter(Blog.slug == slug).first_or_404()

    if request.method == 'POST':

        blog.title = form.blog_title.data
        blog.slug = form.blog_title.data

        if form.blog_image.data.filename:
            filename=f"{uuid.uuid1()}_{secure_filename(form.blog_image.data.filename)}"
            file_url = f'uploads/{filename}'
            blog.image = file_url
        else:
            blog.image = blog.image


        blog.metacontent = form.blog_metacontent.data
        blog.group_mortabet = form.blog_group_mortabet.data
        blog.content = form.blog_content.data
        blog.writer = form.blog_writer.data
        blog.date = ShowTodayFull()

        try:
            db.session.commit()
        except IntegrityError:
            flash('نام وبلاگ تکراری میباشد' , category='bg-danger')

        if form.blog_image.data.filename:
            form.blog_image.data.save(f"static/uploads/{filename}")


        flash('تغییرات با موفقیت ثبت شد', category='bg-success')
        return redirect(url_for('admin.blogs'))


            

    return render_template('admin/single_blog.html' , blog=blog )


@admin.route('/blog/delete/<int:blog_id>' , methods=['GET' , 'POST'])
@admin_only_view
def delete_blog(blog_id):
    blog= Blog.query.get_or_404(blog_id)
    db.session.delete(blog)
    db.session.commit()
    flash('وبلاگ با موفقیت حذف شد.' , 'bg-success')
    return redirect(url_for('admin.blogs'))














@admin.route('/gift_pack/' ,methods=['GET', 'POST'])
@admin_only_view
def gift_pack():
    form = GiftpackForm()  
    gift_pack = GiftPack.query.first()  
    return render_template('admin/gift_pack.html' , form = form , gift_pack=gift_pack)



@admin.route('/register_gift_pack_price/', methods=['GET', 'POST'])
@admin_only_view
def register_gift_pack():
    form = GiftpackForm()
    gift_packs = GiftPack.query.order_by(GiftPack.id.desc()).all()
    gift_pack = GiftPack.query.first()

    if request.method == 'POST':
        # print(len(gift_packs))

        if len(gift_packs) < 1:
            new_price = GiftPack()
            new_price.price = form.price.data
            db.session.add(new_price)    
            db.session.commit()
        elif len(gift_packs) <= 1:
            gift_pack.price = form.price.data
            db.session.commit()

            


        
        flash('مقاله با موفقیت ثبت شد', category='bg-success')
        return redirect(url_for('admin.gift_pack'))
    
    return render_template('admin/gift_pack.html' , form = form)
















