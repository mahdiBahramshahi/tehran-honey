from ast import Break
from crypt import methods
from unittest import result
from flask import request , render_template , flash , session , abort , redirect , url_for
from . import users
from .models import User 
from .forms import RegisterForm , LoginForm
from app import db
from mod_users.models import User , Card , Blog
from sqlalchemy import or_
from mod_mahsolat.models import Baremoom, Garde, MahsolGroups , Mahsolat, Royal , GiftpackRegister
from mod_users.forms import CardForm
from .utils import user_only_view
from pymysql import IntegrityError


@users.route('/')
def index():
    return redirect(url_for('index'))



@users.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('لطفا تمامی فیلد ها را پر کنید' , 'bg-danger')
            return render_template('users/register.html', form=form)
        if not form.password.data == form.confirm_password.data:
            flash('گذرواژه و تکرار گذرواژه مطابقت ندارد' , 'bg-danger')
            return render_template('users/register.html', form=form)

        old_username = User.query.filter(User.username.ilike(form.username.data)).first()
        if old_username:
            flash('نام کاربری تکراری میباشد' , 'bg-danger')
            return render_template('users/register.html', form=form)

        old_user = User.query.filter(User.email.ilike(form.email.data)).first()
        if old_user:
            flash('ایمیل تکراری می باشد' , 'bg-danger')
            return render_template('users/register.html', form=form)

        

        new_user = User()
        new_user.username = form.username.data
        new_user.email = form.email.data
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        print(form.username.data)
        flash('ثبت نام با موفقیت انجام شد' , 'bg-success')
        return redirect(url_for('users.login'))
        # except IntegrityError:
        #     db.session.rollback()
        #     flash('Email is in use.' , 'bg-danger')
    return render_template('users/register.html', form=form)






@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('لطفا تمامی فیلدها را پر کنید' , 'bg-danger')
            return render_template('users/login.html', form=form)
            
        user = User.query.filter(User.email.ilike(f"{form.email.data}")).first()

        if not user:
            flash("نام کاربری / گذرواژه نادرست است", category='bg-danger')
            return render_template('users/login.html', form=form)

        if not user.check_password(form.password.data):
            flash("نام کاربری / گذرواژه نادرست است", category='bg-danger')
            return render_template('users/login.html', form=form)
        
        # if user:
        #     flash("شما از قبل وارد شده اید", category='bg-danger)
        #     return(redirect(url_for('index')))
        
        session['email'] = user.email
        session['user_id'] = user.id
        session['username'] = user.username
        session['role'] = user.role
        

        if user.role == 1:
            flash("ورود با موفقیت انجام شد", category='bg-success')
            return redirect(url_for('admin.index'))

        # return redirect(url_for('index'))
    
    if session.get('role') == 1:
        flash("ورود با موفقیت انجام شد", category='bg-success')
        return redirect(url_for('admin.index'))
    
    if session.get('email') is not None:
        flash("ورود با موفقیت انجام شد", category='bg-success')
        return redirect(url_for('index'))
    

    return render_template('users/login.html', form=form)



@users.route('/<string:slug>')
def single_mahsol(slug):
    mahsol = Mahsolat.query.filter(Mahsolat.slug == slug).first_or_404()
    # mahsol_name = File.query.filter(File.project_name == project.project_name)
    all_mahsolat = Mahsolat.query.order_by(Mahsolat.id.desc()).all()
    groups = MahsolGroups.query.order_by(MahsolGroups.id.desc()).all()
    return render_template('users/single_mahsol.html' , mahsol=mahsol , all_mahsolat=all_mahsolat , groups=groups)



@users.route('/royal_jelly/<string:slug>')
def single_royal(slug):
    mahsol = Royal.query.filter(Royal.slug == slug).first_or_404()
    # mahsol_name = File.query.filter(File.project_name == project.project_name)
    all_mahsolat = Mahsolat.query.order_by(Mahsolat.id.desc()).all()
    royals = Royal.query.order_by(Royal.id.desc()).all()
    groups = MahsolGroups.query.order_by(MahsolGroups.id.desc()).all()
    return render_template('users/single_royal.html' , mahsol=mahsol , all_mahsolat=all_mahsolat , groups=groups , royals=royals)


@users.route('/baremoom/<string:slug>')
def single_baremoom(slug):
    mahsol = Baremoom.query.filter(Baremoom.slug == slug).first_or_404()
    # mahsol_name = File.query.filter(File.project_name == project.project_name)
    all_mahsolat = Mahsolat.query.order_by(Mahsolat.id.desc()).all()
    baremooms = Baremoom.query.order_by(Baremoom.id.desc()).all()
    groups = MahsolGroups.query.order_by(MahsolGroups.id.desc()).all()
    return render_template('users/single_baremoom.html' , mahsol=mahsol , all_mahsolat=all_mahsolat , groups=groups , baremooms=baremooms)


@users.route('/garde_gol/<string:slug>')
def single_garde(slug):
    mahsol = Garde.query.filter(Garde.slug == slug).first_or_404()
    # mahsol_name = File.query.filter(File.project_name == project.project_name)
    all_mahsolat = Mahsolat.query.order_by(Mahsolat.id.desc()).all()
    garde_gols = Garde.query.order_by(Garde.id.desc()).all()
    groups = MahsolGroups.query.order_by(MahsolGroups.id.desc()).all()
    return render_template('users/single_garde.html' , mahsol=mahsol , all_mahsolat=all_mahsolat , groups=groups , garde_gols=garde_gols)



@users.route('/<string:slug>/')
def single_group(slug):
    group = MahsolGroups.query.filter(MahsolGroups.title == slug).first_or_404()
    mahsolat= Mahsolat.query.filter(Mahsolat.group == slug).order_by(Mahsolat.id.desc()).all()
    royals = Royal.query.filter(Royal.group == slug).order_by(Royal.id.desc()).all()
    baremooms = Baremoom.query.filter(Baremoom.group == slug).order_by(Baremoom.id.desc()).all()
    garde_gols = Garde.query.filter(Garde.group == slug).order_by(Garde.id.desc()).all()
    groups = MahsolGroups.query.order_by(MahsolGroups.id.desc()).all()

    return render_template('users/single_group.html' , group=group , all_mahsolat=mahsolat , royals=royals , baremooms=baremooms , garde_gols=garde_gols , groups=groups)





@users.route('/add_to_card/' , methods=['GET','POST'])
@user_only_view
def add_to_card():
    form = CardForm() 
    if request.method == 'POST':
        
        # old_mahsol = Card.query.filter(Card.mahsol_title.ilike(form.mahsol_title.data)).first()
        # if old_mahsol:
        #     flash('این محصول قبلا به سبد شما افزوده شده است!' , 'bg-danger')
            
            

        # session['mahsol_title'] = request.form.get('mahsol_title')    
        # session['mahsol_count'] = request.form.get('mahsol_count')

        add_mahsol = Card()
        add_mahsol.username = session.get('username')
        add_mahsol.email = session.get('email')
        add_mahsol.mahsol_title = request.form.get('mahsol_title')
        add_mahsol.mahsol_card_id = request.form.get('id') 
        add_mahsol.mahsol_description = request.form.get('description') 
        add_mahsol.mahsol_slug = request.form.get('slug') 
        add_mahsol.mahsol_group = request.form.get('group') 
        add_mahsol.mahsol_price = request.form.get('price') 
        add_mahsol.mahsol_image = request.form.get('image') 
        add_mahsol.mahsol_count = request.form.get('mahsol_count')
        add_mahsol.mahsol_role = request.form.get('role')

        if int(add_mahsol.mahsol_count) < 1:
            flash('حداقل مقدار سفارش ۱ میباشد.' ,  category='bg-danger')
            
            return render_template('users/shopping_card.html')


        db.session.add(add_mahsol)
        db.session.commit()
    
        flash('محصول با موفقت به سبد خرید افزوده شد' , 'bg-success')
        return redirect(url_for('users.shopping_card'))

        
    return render_template('users/shopping_card.html')






@users.route('/modify_card/<string:slug>' , methods=['GET' , 'POST'])
def modify_card(slug):
    form = CardForm()
    mahsol = Card.query.filter(Card.mahsol_slug == slug).first_or_404()

    if request.method == 'POST':

        # old_title = Mahsolat.query.filter(Mahsolat.title.ilike(form.mahsol_title.data)).first()
        # if old_title:
        #     flash('نام محصول تکراری میباشد' , 'bg-danger')
        #     return render_template('admin/mahsolat.html', form=form)


        mahsol.email =  mahsol.email
        mahsol.mahsol_title =  mahsol.mahsol_title
        mahsol.mahsol_card_id =  mahsol.mahsol_card_id
        mahsol.mahsol_description =  mahsol.mahsol_description
        mahsol.mahsol_slug =  mahsol.mahsol_slug
        mahsol.mahsol_group =  mahsol.mahsol_group
        mahsol.mahsol_price =  mahsol.mahsol_price 
        mahsol.mahsol_image =  mahsol.mahsol_image
        mahsol.mahsol_role = mahsol.mahsol_role

        mahsol.mahsol_count = request.form.get('mahsol_count')

        try:
            db.session.commit()
        except IntegrityError:
            flash('نام محصول تکراری میباشد' , category='bg-danger')


        # flash('تغییرات با موفقیت اعمال شد', category='bg-success')
        return redirect(url_for('users.shopping_card'))

    return render_template('users/shopping_card.html' , mahsol=mahsol)









@users.route('/shopping_card')
@user_only_view
def shopping_card(): 

    
    user_mahsols = Card.query.filter(Card.username == session.get('username')) 
    groups = MahsolGroups.query.order_by(MahsolGroups.id.desc()).all()


    price_list = []

    from unidecode import unidecode

    for mahsol in user_mahsols:
        mahsol_price = unidecode(mahsol.mahsol_price) 
        mahsol_count = unidecode(mahsol.mahsol_count)
        result_mahsol_price = int(mahsol_price) * int(mahsol_count)

        price_list.append(result_mahsol_price)
    
    mahsol_card_count = Card.query.filter(Card.username == session.get('username'))
    card_count = len(list(mahsol_card_count))



    result_en_price = sum(price_list)
    # result_pricee = convert_numbers.english_to_persian(result_en_price)
    result_price = f"{result_en_price: ,}"

    price_list = []
    return render_template('users/shopping_card.html' , user_mahsols = user_mahsols , result_price=result_price , card_count=card_count , groups=groups)


@users.route('/shopping_card/delete/<int:mahsol_id>' , methods=['GET' , 'POST'])
@user_only_view
def delete_mahsol(mahsol_id):
    mahsol= Card.query.get_or_404(mahsol_id)
    db.session.delete(mahsol)
    db.session.commit()
    flash('محصول از سبد خرید حذف شد.' , 'bg-success')
    return redirect(url_for('users.shopping_card'))


@users.route('/mahsolat')
def all_mahsolat():
    all_mahsolat = Mahsolat.query.order_by(Mahsolat.id.desc()).all()
    groups = MahsolGroups.query.order_by(MahsolGroups.id.desc()).all()
    royals = Royal.query.order_by(Royal.id.desc()).all()
    baremooms = Baremoom.query.order_by(Baremoom.id.desc()).all()
    garde_gols = Garde.query.order_by(Garde.id.desc()).all()
    return render_template('users/all_mahsolat.html' , all_mahsolat=all_mahsolat , royals=royals , baremooms=baremooms , garde_gols=garde_gols , groups=groups)




@users.route('/blog/<string:slug>/')
def single_blog(slug):
    blog = Blog.query.filter(Blog.slug == slug).first_or_404()
    all_blogs = Blog.query.order_by(Blog.id.desc()).all()
    all_groups = MahsolGroups.query.order_by(MahsolGroups.id.desc()).all()
    return render_template('users/single_blog.html' , blog=blog , all_blogs=all_blogs , groups=all_groups)


@users.route('/honeys')
def asalha():
    all_mahsolat = Mahsolat.query.order_by(Mahsolat.id.desc()).all()
    return render_template('users/asalha.html' , all_mahsolat=all_mahsolat)


@users.route('/gift_pack')
def gift_pack():
    gift_packs = GiftpackRegister.query.order_by(GiftpackRegister.id.desc()).all()
    all_mahsolat = Mahsolat.query.order_by(Mahsolat.id.desc()).all()
    return render_template('users/gift_pack.html' , gift_packs=gift_packs , all_mahsolat=all_mahsolat)




