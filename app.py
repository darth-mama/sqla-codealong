from flask import Flask, request, redirect, render_template
# from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pet_shop_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'shssssssh'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# debug = DebugToolbarExtension(app)ß


with app.app_context():
    connect_db(app)
    # Inside this block, Flask will know that 'app' is the current application
    db.create_all()
app.app_context().push()


@app.route('/')
def list_pets():
    '''shows list of all pets in db'''
    pets = Pet.query.all()
    return render_template('list.html', pets=pets)


@app.route('/', methods=["GET", "Post"])
def create_pet():
    # name = request.args.get("name")
    # species = request.args.get("species")
    # # remember that data from form renders to a string
    # # hunger we want as an int
    # # therefore we have to convert it
    # # remember that our default for hunger=20, need an if statement
    # hunger = request.args.get("hunger")
    name = request.form["name"]
    species = request.form["species"]
    hunger = request.form["hunger"]
    hunger = int(hunger) if hunger else None

    new_pet = Pet(name=name, species=species, hunger=hunger)
    db.session.add(new_pet)
    db.session.commit()
    return redirect(f"/{new_pet.id}")


@app.route('/<int:pet_id>')
def show_pet(pet_id):
    """Show details about a single pet"""
    pet = Pet.query.get_or_404(pet_id)
    return render_template("details.html", pet=pet)
