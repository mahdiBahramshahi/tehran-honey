from flask import session , abort , flash , redirect , url_for
from functools import wraps


def user_only_view(func):
    @wraps(func)
    def decorator(*args,**kwargs):
        if not session.get('email'):
            flash(' شما حساب کاربری ندارید. ابتدا در این صفحه وارد حساب کاربری تان شوید', category='bg-danger')
            return redirect(url_for('users.login')) 

        return func(*args,**kwargs)
    return decorator