from app import app
from mod_mahsolat.models import Baremoom, Garde, Mahsolat , MahsolGroups , Royal
from mod_users.models import Slider , Monasebat , Blog

from flask import Flask, url_for, redirect, request , render_template

from suds.client import Client

@app.route('/')
def index():
    all_mahsolat = Mahsolat.query.order_by(Mahsolat.id.desc()).all()
    groups = MahsolGroups.query.order_by(MahsolGroups.id.desc()).all()
    sliders = Slider.query.order_by(Slider.id.desc()).all()
    sliders_1 = Slider.query.first()
    mahsol_13 = all_mahsolat[:13]
    all_blogs = Blog.query.order_by(Blog.id.desc()).all()
    blog_3 = all_blogs[:3]
    royals = Royal.query.order_by(Royal.id.desc()).all()
    baremooms = Baremoom.query.order_by(Baremoom.id.desc()).all()
    garde_gols = Garde.query.order_by(Garde.id.desc()).all()


    monasebat = Monasebat.query.order_by(Monasebat.id.desc()).all()

    

    return render_template('index.html' ,slider_1=sliders_1 ,mahsol_13=mahsol_13 ,   all_mahsolat=all_mahsolat , groups=groups , sliders=sliders , monasebat=monasebat , blog_3=blog_3 , royals=royals , baremooms=baremooms , garde_gols=garde_gols)







MMERCHANT_ID = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'  # Required
ZARINPAL_WEBSERVICE = 'https://www.zarinpal.com/pg/services/WebGate/wsdl'  # Required
amount = 1000  # Amount will be based on Toman  Required
description = u'توضیحات تراکنش تستی'  # Required
email = 'user@userurl.ir'  # Optional
mobile = '09123456789'  # Optional



@app.route('/request/')
def send_request():
    client = Client(ZARINPAL_WEBSERVICE)
    result = client.service.PaymentRequest(MMERCHANT_ID,
                                           amount,
                                           description,
                                           email,
                                           mobile,
                                           str(url_for('verify', _external=True)))
    if result.Status == 100:
        return redirect('https://www.zarinpal.com/pg/StartPay/' + result.Authority)
    else:
        return 'Error'


@app.route('/verify/', methods=['GET', 'POST'])
def verify():
    client = Client(ZARINPAL_WEBSERVICE)
    if request.args.get('Status') == 'OK':
        result = client.service.PaymentVerification(MMERCHANT_ID,
                                                    request.args['Authority'],
                                                    amount)
        if result.Status == 100:
            return 'Transaction success. RefID: ' + str(result.RefID)
        elif result.Status == 101:
            return 'Transaction submitted : ' + str(result.Status)
        else:
            return 'Transaction failed. Status: ' + str(result.Status)
    else:
        return 'Transaction failed or canceled by user'

