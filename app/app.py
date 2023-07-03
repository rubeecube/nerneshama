import enum
import io
import json
import os
from base64 import b64encode

import flask
import hdate
import jewish
import qrcode

from babel.dates import format_date
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from pyluach import hebrewcal, dates
from sqlalchemy import Integer
from sqlalchemy.sql import func

from forms import *

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = os.urandom(32)
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join('app', 'db', 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

Bootstrap(app)

debug = False
groups = None
users = None


class GenderEnum(enum.Enum):
    male = 1
    female = 2


class UserDB(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    email = db.Column(db.String(80))
    phone = db.Column(db.String(80))


class NeshamaDB(db.Model):
    __tablename__ = 'neshama'
    id = db.Column(db.Integer, primary_key=True)
    name_he = db.Column(db.String(100), nullable=False)
    name_fr = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.Enum(GenderEnum), nullable=False)
    date_niftar_he = db.Column(db.String(100), nullable=False)
    date_levaya_he = db.Column(db.String(100))
    opt_in_alert = db.Column(db.Boolean())
    opt_in_news = db.Column(db.Boolean())
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())


class CreatorDB(db.Model):
    __tablename__ = 'creator'
    id = db.Column(db.Integer, primary_key=True)
    neshama_id = db.Column(Integer, db.ForeignKey("neshama.id"))
    user_id = db.Column(Integer, db.ForeignKey("user.id"))
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())


def default_params(
        form_neshama=AddNeshamaForm(),
        error=None
):
    return {
        'form_neshama': form_neshama,
        'error': error
    }


def change_date(d: hebrewcal.HebrewDate):
    return jewish.JewishDate.from_date(d.to_greg().to_pydate())


def get_neshamot():
    months_id_hdate_inv = {v: i for i, v in enumerate(dates.utils.MONTH_NAMES)}

    date_today = datetime.datetime.now()
    today_heb = dates.GregorianDate(date_today.year, date_today.month, date_today.day).to_heb()

    neshamot = NeshamaDB.query.all()
    neshamot_to_render = []

    for neshama in neshamot:
        date_niftar_he_db = neshama.date_niftar_he.split("-")
        date_niftar_he = dates.HebrewDate(
            int(date_niftar_he_db[0]),
            months_id_hdate_inv[date_niftar_he_db[1]],
            int(date_niftar_he_db[2])
        )

        date_niftar = date_niftar_he

        less_than_1year = False
        if neshama.date_levaya_he is None:
            if today_heb < date_niftar_he.add(0, 11):
                # Can't compute
                continue
            else:
                less_than_1year = False
        else:
            date_levaya_he_db = neshama.date_levaya_he.split("-")
            date_levaya_he = dates.HebrewDate(
                int(date_levaya_he_db[0]),
                months_id_hdate_inv[date_levaya_he_db[1]],
                int(date_levaya_he_db[2])
            )
            date_levaya = date_levaya_he
            date_hazcara11 = date_levaya_he.add(0, 11)
            date_hazcara11_adar = date_levaya_he.add(0, 11, adar1=True)

            if today_heb < date_hazcara11 or today_heb < date_hazcara11_adar:
                less_than_1year = True
            else:
                less_than_1year = False

        date_hazcara1 = date_niftar.add(today_heb.year - date_niftar.year)
        date_hazcara1_adar = date_niftar.add(today_heb.year - date_niftar.year, adar1=True)

        if date_hazcara1.to_greg().to_pydate() < datetime.datetime.now().date():
            date_hazcara1 = date_hazcara1.add(1)
            date_hazcara1_adar = date_hazcara1_adar.add(1, adar1=True)

        if less_than_1year:
            show_adar = date_hazcara11 != date_hazcara11_adar
        else:
            show_adar = date_hazcara1 != date_hazcara1_adar

        date_niftar_g = format_date(date_niftar.to_pydate(), format='long', locale='fr_FR').title()
        date_niftar = change_date(date_niftar).__str__()

        if less_than_1year:
            date_sort = datetime.datetime.combine(date_hazcara11.to_pydate(), datetime.datetime.min.time()).timestamp()
            date_hazcara_g = format_date(date_hazcara11.to_pydate(), format='full', locale='fr_FR').title()
            date_hazcara = change_date(date_hazcara11).__str__()
            if show_adar:
                date_hazcara_g += " - "
                date_hazcara_g += format_date(date_hazcara11_adar.to_pydate(), format='full', locale='fr_FR').title()
                date_hazcara += " - "
                date_hazcara += change_date(date_hazcara11_adar).__str__()
        else:
            date_sort = datetime.datetime.combine(date_hazcara1.to_pydate(), datetime.datetime.min.time()).timestamp()
            date_hazcara_g = format_date(date_hazcara1.to_pydate(), format='full', locale='fr_FR').title()
            date_hazcara = change_date(date_hazcara1).__str__()
            if show_adar:
                date_hazcara_g += " - "
                date_hazcara_g += format_date(date_hazcara1_adar.to_pydate(), format='full', locale='fr_FR').title()
                date_hazcara += " - "
                date_hazcara += change_date(date_hazcara1_adar).__str__()

        neshamot_to_render += [
            {
                'nom_francais': neshama.name_fr,
                'nom_hebreu': neshama.name_he,
                'date_niftar_g': date_niftar_g,
                'date_niftar': date_niftar,
                'date_sort': date_sort,
                'date_hazcara_g': date_hazcara_g
            }
        ]

    neshamot_to_render.sort(key=lambda x: x['date_sort'])

    return neshamot_to_render


@app.route('/ajax_data/', methods=['GET'])
def run_ajax_data():
    start = 0
    json_output = False
    html_skeleton = False
    html_skeleton_ratio = None

    try:
        if 'start' in flask.request.args.keys():
            start = int(flask.request.args['start'])
    except Exception:
        pass

    try:
        if 'json_output' in flask.request.args.keys():
            json_output = True
    except Exception:
        pass

    try:
        if 'html_skeleton' in flask.request.args.keys() and 'ratio' in flask.request.args.keys() and flask.request.args['ratio'] in ['1', '2']:
            html_skeleton = True
            html_skeleton_ratio = int(flask.request.args['ratio'])
    except Exception:
        pass

    if json_output:
        return json.dumps(get_neshamot())
    elif html_skeleton and html_skeleton_ratio:
        return render_template(
            'html_skeleton.html',
            ratio=html_skeleton_ratio
        )
    else:
        return render_template(
            'ajax_table.html',
            neshamot=get_neshamot(),
            start=start,
            screens=[('2/4', '2/4'), ('1', '1'), ('2', '1'), ('3', '1'), ('1', '2'), ('1', '3')]
        )


@app.route('/', methods=['GET'])
def index(error=None):
    db.create_all()

    c = hdate.Location(
        "Tel Aviv",
        latitude=32.06990618721521,
        longitude=34.77919324232795,
        altitude="35")

    date_today = datetime.datetime.now()
    today_heb = dates.GregorianDate(date_today.year, date_today.month, date_today.day).to_heb()

    z = hdate.Zmanim(date=date_today, location=c, hebrew=False)
    times = {k: v.strftime("%H:%M") for k, v in z.zmanim.items()}
    h = hdate.HDate(date_today, hebrew=False)

    image_io = io.BytesIO()
    qr_object = qrcode.QRCode(version=2, box_size=5, border=0)
    qr_object.add_data('https://localhost:5000/neshama_add')
    qr_object.make()
    image = qr_object.make_image()
    image.save(image_io, 'PNG')
    qrcode_url = 'data:image/png;base64,' + b64encode(image_io.getvalue()).decode('ascii')

    return render_template(
        'index.html',
        zmanim=times,
        now=format_date(date_today, format='full', locale='fr_FR').title(),
        nowH=change_date(today_heb),
        nowH2=h,
        parasha=h.parasha,
        upcoming=h.upcoming_yom_tov.holiday_description,
        upcoming_date=change_date(
            dates.GregorianDate(
                h.upcoming_yom_tov.gdate.year,
                h.upcoming_yom_tov.gdate.month,
                h.upcoming_yom_tov.gdate.day
            ).to_heb()
        ),
        upcoming_date_g=format_date(dates.GregorianDate(
                h.upcoming_yom_tov.gdate.year,
                h.upcoming_yom_tov.gdate.month,
                h.upcoming_yom_tov.gdate.day
            ).to_pydate(), format='full', locale='fr_FR').title(),
        neshamot=get_neshamot(),
        qrcode_url=qrcode_url,
        location=c
    )


@app.route('/neshama_add', methods=['GET', 'POST'])
def run_neshama_add():
    form_neshama = AddNeshamaForm(flask.request.form)
    months_id_hdate_inv = {v: i for i, v in enumerate(dates.utils.MONTH_NAMES)}

    if flask.request.method == 'POST':
        gender = form_neshama.gender.data
        email = form_neshama.email.data
        phone = form_neshama.phone.data
        name_fr = form_neshama.name_fr.data
        name_he = form_neshama.name_he.data

        if form_neshama.date_niftar_he_y.data and form_neshama.date_niftar_he_m.data and form_neshama.date_niftar_he_d.data:
            date_niftar_he = dates.HebrewDate(
                form_neshama.date_niftar_he_y.data,
                months_id_hdate_inv[form_neshama.date_niftar_he_m.data],
                form_neshama.date_niftar_he_d.data
            )
        else:
            date_niftar_fr = form_neshama.date_niftar_fr.data
            erev_niftar = form_neshama.erev_niftar.data
            if erev_niftar:
                date_niftar_fr += datetime.timedelta.days
            date_niftar_he = dates.GregorianDate(date_niftar_fr.year, date_niftar_fr.month, date_niftar_fr.day).to_heb()

        if form_neshama.date_levaya_he_y.data and form_neshama.date_levaya_he_m.data and form_neshama.date_levaya_he_d.data:
            date_levaya_he = dates.HebrewDate(
                form_neshama.date_levaya_he_y.data,
                months_id_hdate_inv[form_neshama.date_levaya_he_m.data],
                form_neshama.date_levaya_he_d.data
            )
        else:
            date_levaya_fr = form_neshama.date_levaya_fr.data
            erev_levaya = form_neshama.erev_levaya.data
            if erev_levaya:
                date_levaya_fr += datetime.timedelta.days
            date_levaya_he = dates.GregorianDate(date_levaya_fr.year, date_levaya_fr.month, date_levaya_fr.day).to_heb()

        opt_in_1 = form_neshama.opt_in_1.data
        opt_in_2 = form_neshama.opt_in_2.data

        new_neshama = NeshamaDB(
            name_he=name_he,
            name_fr=name_fr,
            gender="male" if gender == "Homme" else 'female',
            date_niftar_he=f'{date_niftar_he:%Y-%B-%d}',
            date_levaya_he=f'{date_levaya_he:%Y-%B-%d}',
            opt_in_alert=opt_in_1,
            opt_in_news=opt_in_2,
        )
        db.session.add(new_neshama)
        db.session.commit()

        return render_template(
            'neshama_add_ok.html',
            title="Date de la neshama ajoutée avec succès",
            **default_params()
        )
    else:
        return render_template(
            'neshama_add.html',
            title="Ajouter une date",
            **default_params()
        )


if __name__ == '__main__':
    debug = True
    app.run(debug=True, port=5000)
