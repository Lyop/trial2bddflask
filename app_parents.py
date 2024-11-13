# Note we imported request!
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, TextAreaField, BooleanField, RadioField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Length, InputRequired

app = Flask(__name__)
# Il y a une meilleure manière de le faire sans la mettre dans le code
app.config['SECRET_KEY'] ="Clé difficile à deviner"
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_CHECK_DEFAULT'] = False
app.config['WTF_CSRF_SECRET_KEY'] = 'WTF'

# Maintenant, nous allons créer une classe WTForm
# Beaucoup de champs sont disponibles sur:
# http://wtforms.readthedocs.io/en/stable/fields.html
class ParentForm(FlaskForm):
    # create the information that you'll need
    name_par = StringField(label="Name Surname  :")
    pilot = BooleanField(label="Pilot Parent?")

    # you always have to precise the choices that are passed as a list of tuples
    # choices, values associated with the option
    gender = RadioField(label="Gender:",choices=[('M','Masculine'),
        ('F', 'Feminine')], render_kw={
            'class':'pasdepuces'
        },
        validators=[DataRequired(message="Enter gender!")])
    dpt = SelectField("Department", choices=[(None, 'Select one'),
        ('14', 'Calvados'),('61','Orne'), ('50','Manche')], validators=[DataRequired(message="Enter gender!")])
    remarks = TextAreaField(label="Any remarks?")
    send = SubmitField(label="Send")



class CategorieForm(FlaskForm):
    '''
    Cette classe générale reçoit beaucoup de formulaires
    à propos des catégories de jouets
    On va créer trois champs WTForms.
    '''
    nom_cat = StringField('Nom Catégorie:            ', validators=[
        DataRequired(message="Ce champ doit être rempli avec un nom valide"),
        Length(min=3, max=50, message="La longueur doit être entre 3 et 50 caractères")
    ])
    desc_cat = TextAreaField("Description Catégorie: ", validators=[
        InputRequired(message="Ce champ doit être saisi!!!")
    ])
    envoyer = SubmitField('Envoyer')



@app.route('/', methods=['GET', 'POST'])
def index():
    # Mettre nom_cat et desc_cat comme flag,
    # on les utilisera dans les tests. Au début, elles sont inconnues
    nom_cat = None
    desc_cat = None

    # On crée une instance de formulaire.
    form = CategorieForm()
    # Si le formulaire est valide et les données des champs sont acceptées
    # à la soumission, validate_on_submit() renvoie True,
    # sinon, elle renvoie
    if form.validate_on_submit():
        # Récupérer les données sur la catégorie
        nom_cat = form.nom_cat.data
        desc_cat = form.desc_cat.data

        # Rénitialiser les champs du formulaire
        form.nom_cat.data = ''
        form.desc_cat.data = ''
        # return redirect(url_for('index'))
    return render_template('index.html', form=form, nom_cat=nom_cat,
                           desc_cat=desc_cat)


@app.route('/parent', methods=['GET', 'POST'])
def nv_parent():
    #On affiche la page parent.html
    form = ParentForm()
    if form.validate_on_submit():
        ancien_dpt = session['dpt']
        session['name_par'] = form.name_par.data
        session['pilot'] = form.pilot.data
        session['gender'] = form.gender.data
        session['dpt'] = form.dpt.data
        session['remarks'] = form.remarks.data
        # infos = [name_par, pilot, gender, dpt, remarks]
        # return render_template('confirmation.html', infos=infos)
        flash("This is a flash message, success!:")
        if ancien_dpt != None and ancien_dpt != form.dpt.data:
            flash(f"You've chnaged your dpt???????????? Bruh...{session['dpt']}")
        return redirect(url_for('confirmation'))
        print("Form has been validated.")
    return render_template("parent.html", form=form)


@app.route('/confirmation', methods=['GET'])
def confirmation():
    return render_template('confirmation.html')



class Toyinfo(FlaskForm):
    # create the information that you'll need
    toy_no = IntegerField(label="Toy number :")
    toy_categ = SelectField("Category", choices = [('SELECT', None), ('Hammy','1'), ('Hippo', '2'), ('Cookie','3')], validators=[DataRequired(message="Choose a toy type :)!")])
    toy_name = StringField(label="Enter the toy's name: ")
    toy_desc = TextAreaField(label="Enter a description for this toy.")
    age_min = IntegerField(label="Minimum age for this toy:")
    age_max = IntegerField(label="Maximum age for this toy:")
    prix = DecimalField(label="The price of the item")
    send = SubmitField(label="SEND")





@app.route('/informations', methods=['GET', 'POST'])
def toy_information():
    form = Toyinfo()
    if form.validate_on_submit():
        session["toy_no"] = form.toy_no.data
        session["toy_categ"] = form.toy_categ
        session["toy_name"] = form.toy_name
        session["toy_desc"] = form.toy_desc
        flash("This is a flash message, success!:")

        return redirect(url_for('confj.html'))
        print("Form has been validated.")

    return render_template("informations.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)
