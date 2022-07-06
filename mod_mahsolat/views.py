from operator import or_
from . import mahsolat
from flask import session, flash, request, redirect, url_for, render_template
from .forms import MahsolatForms , MahsolgroupForms
from .models import Mahsolat
from sqlalchemy import  or_
from flask_sqlalchemy import get_debug_queries 
from .forms import SearchForm
@mahsolat.route('/')
def index():
    pass


@mahsolat.route('/search')
def search_mahsol():
    search_form = SearchForm()
    search_query = request.args.get('search_query','')
    title_cond = Mahsolat.title.ilike(f'%{search_query}%')
    description_cond = Mahsolat.description.ilike(f'%{search_query}%')
    group_cond = Mahsolat.group.ilike(f'%{search_query}%')
    found_mahsols = Mahsolat.query.filter(or_(
        title_cond,
        description_cond,
        group_cond
    )).all()
    print(found_mahsols)

    if len(found_mahsols) == 0:
        flash(f'محصولی با عنوان {search_query} یافت نشد' , category='bg-warning')
        return(render_template('users/search_form.html', search_form=search_form , found_mahsols=found_mahsols , search_query=search_query , search_mahsolat=found_mahsols))

    return(render_template('users/search_form.html', search_form=search_form , found_mahsols=found_mahsols , search_query=search_query , search_mahsolat=found_mahsols))
