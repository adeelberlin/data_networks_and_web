from flask import Flask, render_template, flash, redirect
from DBhelper import DBHelper
from add_animal_form import AddAnimalForm
from vote_form import VoteForm
from vs_url_for import vs_url_for

app = Flask(__name__);
db = DBHelper()

app.secret_key = 'hto%s&gw3^!5m+i8b87yoo9!sh1!2$6d^d#uk%*=bvcmj^(df('

@app.route('/')
def home():
    deers = db.get_animals("Deer")
    lions = db.get_animals("Cat")
    snakes = db.get_animals("Snake")
    return render_template("index.html", deers=deers, lions=lions, snakes=snakes);


@app.route('/add_animal', methods=['GET','POST'])
def add_animal():
    form = AddAnimalForm()
    if form.validate_on_submit():
        name = form.name.data
        type = form.type.data
        description = form.description.data
        image_url = form.image_url.data

        db.add_animal(name,type,description,image_url)

        return redirect(vs_url_for('home'))
    return render_template("add_animal.html", form=form)


@app.route('/update_animal/<animal_id>', methods=['GET','POST'])
def update_animal(animal_id):
    animal = db.get_animal(animal_id)
    form = AddAnimalForm()

    form.id.data = animal[0]['_id']
    form.name.data = animal[0]['name']
    form.type.data = animal[0]['type']
    form.description.data = animal[0]['description']
    form.image_url.data = animal[0]['image_url']

    if form.validate_on_submit():
        form = AddAnimalForm()

        id = form.id.data
        name = form.name.data
        type = form.type.data
        description = form.description.data
        image_url = form.image_url.data

        db.update_animal(id,name,type,description,image_url)

        return redirect(vs_url_for('home'))
    return render_template("edit_animal.html", form=form)


@app.route('/animals/<id>', methods=['GET','POST'])
def animal_show(id):
    animal = db.get_animal(id)
    vote = db.get_vote(id)
    form = VoteForm()

    try:
        form.id.data = vote[0]['_id']
        form.votes.data = vote[0]['votes'] + 1
    except (ValueError,IndexError):
        db.add_vote(id,0)

    if form.validate_on_submit():
            db.update_vote(id,form.votes.data)
    return render_template("show_animal.html", animal=animal, form=form, vote=vote)


@app.route('/animals')
def animals():
    animals = db.get_all_animals()
    return render_template("animals.html", animals=animals)


@app.route('/cats')
def cats():
    cats = db.get_animals("Cat")
    return render_template("cats.html", cats=cats)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000);
