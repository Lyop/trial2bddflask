# Note we imported request!
from flask import Flask, render_template, request, g, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, InputRequired


app = Flask(__name__)
# Configurer une clé secrete
# Il y a une meilleure manière de le faire sans la mettre dans le code
app.config['SECRET_KEY'] ="Clé difficile à deviner"
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_CHECK_DEFAULT'] = False
app.config['WTF_CSRF_SECRET_KEY'] = 'WTF'

# Maintenant, nous allons créer une classe WTForm
# Beaucoup de champs sont disponibles sur:
# http://wtforms.readthedocs.io/en/stable/fields.html
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


#On spécifie dans la route les méthodes acceptées par HTTP: POST et GET
#Si les méthodes ne sont pas ajoutées, c'est GET par défaut
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



if __name__ == '__main__':
    app.run(debug=True)
