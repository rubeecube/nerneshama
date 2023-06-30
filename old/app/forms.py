from wtforms import Form, StringField, IntegerField, SubmitField, DateField, validators, \
    SelectField, EmailField, TelField, BooleanField
import datetime
from pyluach import dates


class AddNeshamaForm(Form):
    debug = True

    name = "Ajouter un rappel pour une neshama"
    id = "form_neshama"
    description = "Rajouter une date dans le calendrier pour les hazcarot:"

    gender = SelectField('Genre', description="Genre", choices=['Homme', 'Femme'], default="Homme" if debug else None)
    email = EmailField('E-Mail', description="Necessaire pour la gestion du compte", default="ruben@bokobza.info" if debug else None)
    phone = TelField("Téléphone", description="Necessaire pour les rappels de dates importantes", default="+972538791892" if debug else None)
    name_fr = StringField("Nom en français", description="Informations du défunt en Français", default="Yaakov Ben David Bokobza" if debug else None)
    name_he = StringField("Nom en hébreu", description="Informations du défunt en Hébreu", default="יעקב בן דוד" if debug else None)
    date_niftar_he_d = IntegerField(
        "Date de déces en hébreu",
        [validators.NumberRange(min=0, max=31)],
        description="Format Jour Mois Année: ex. 02 Tammuz 5783",
        default=19 if debug else None
    )
    date_niftar_he_m = SelectField(
        choices=dates.utils.MONTH_NAMES,
        default="Cheshvan" if debug else None
    )
    date_niftar_he_y = IntegerField([validators.NumberRange(min=0, max=5999)], default=5782 if debug else None)
    date_niftar_fr = DateField(
        "Date de déces en francais",
        default=datetime.datetime.strptime("2021/10/25", "%Y/%m/%d") if debug else None
    )
    erev_niftar = BooleanField("Déces apres la tombée de la nuit", default=False if debug else None)
    date_levaya_he_d = IntegerField(
        "Date d'enterrement en hébreu",
        [validators.NumberRange(min=0, max=31)],
        description="Format Jour Mois Année: ex. 02 Tammuz 5783",
        default=20 if debug else None
    )
    date_levaya_he_m = SelectField(
        choices=dates.utils.MONTH_NAMES,
        default="Cheshvan" if debug else None
    )
    date_levaya_he_y = IntegerField([validators.NumberRange(min=0, max=5999)], default=5782 if debug else None)
    date_levaya_fr = DateField(
        "Date de déces en francais",
        description="Necessaire si moins d'un an.",
        default=datetime.datetime.strptime("2021/10/26", "%Y/%m/%d") if debug else None
    )
    erev_levaya = BooleanField("Enterrement apres la tombée de la nuit", default=False if debug else None)
    opt_in_1 = BooleanField(
        "J'accepte de recevoir des rappels par SMS/Whatsapp/Mail un mois avant la hazcara.",
        default=True if debug else None
    )
    opt_in_2 = BooleanField(
        "J'accepte de recevoir des informations de Alef Tel-Aviv par SMS/Whatsapp/Mail.",
        default=True if debug else None
    )

    submit = SubmitField('Ajouter')
