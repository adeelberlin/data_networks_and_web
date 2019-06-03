from flask import Flask, request
from flask import render_template
from flask import redirect, url_for
from flask import session, flash, abort
from vs_url_for import vs_url_for
from forms import addTwitForm, editTwitForm, loginForm
from flask_login import LoginManager, login_required
from flask_login import login_user, logout_user
# importing current_user from flask-login
# so that we can access the user object of the currently logged in user
# at any point (including in templates)
from flask_login import current_user
## import the sqlalchemy database and the users & twits db classes
from models import db,Users,Twits
## import the passwordhelper class to do password hashing / checking
from passwordhelper import PasswordHelper

login_manager = LoginManager()

app = Flask(__name__)
# configure the sqlalchenmy database URI that is used for the connection
# see http://flask-sqlalchemy.pocoo.org/2.3/config/
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mytwits_user:mytwits_password@localhost/mytwits'
app.config['SQLALCHEMY_ECHO'] = False
# initialise the sqlalchemy database connection
db.init_app(app)
# initialise flask-login
login_manager.init_app(app)

app.secret_key = 'hto%s&gw3^!5m+i8b87yoo9!sh1!2$6d^d#uk%*=bvcmj^(df('

# instantiate a password helper object
ph = PasswordHelper()

#---- the callback function for flask-login
@login_manager.user_loader
def load_user(user_id):
    # we don't use sql any longer to get the user id; we access it through the
    # User object provided by sqlalchemy
    return Users.query.get(int(user_id))

@app.route('/')
def index():
    # we don't use sql any longer to get the twits; we access them through the
    # Twits object provided by sqlalchemy
    twits = Twits.query.order_by(Twits.created_at.desc()).all() 
    return render_template("mytwits_mysql.html", twits=twits)

@app.route('/<username>')
def timeline(username):
    # instead of having to think in terms of selecting twits using sql queries
    # e.g. 
    # "select twit from twits where user_id = (select user_id from users where username = 'dan1' );"
    # we can just use the objects provided by sqlalchemy
    twits = Users.query.filter_by(username=username).first().twits
    return render_template('timeline.html',twits=twits)

@app.route('/add_twit', methods = ['GET', 'POST'])
@login_required
def add_twit():
    form = addTwitForm()
    if form.validate_on_submit():
        twit = form.twit.data
        user_id = current_user.user_id
        # SQLAlchemy adds an implicit constructor to all model classes which
        # accepts keyword arguments for all its columns and relationships.
        # We can use this to create our new twit
        new_twit = Twits(twit=twit, user_id=user_id)
        # As explained in http://flask-sqlalchemy.pocoo.org/2.3/queries/
        # we need to add the object to the flask-sqlalchemy session
        # and then commit our changes
        # for it to be inserted in to the database
        db.session.add(new_twit)
        db.session.commit()
        return redirect(vs_url_for('index'))
    return render_template('add_twit_mysql.html',form=form)

@app.route('/edit_twit', methods = ['GET', 'POST'])
@login_required
def edit_twit():
    user_id = current_user.user_id
    form = editTwitForm()
    if request.args.get('id'):
        twit_id = request.args.get('id')
        # again, we don't use sql to get the twit
        # but instead we use the Twits class 
        # and the query attribute provided by flask-sqlalchemy
        # see also
        # http://flask-sqlalchemy.pocoo.org/2.3/queries/#querying-records
        twit = Twits.query.filter_by(twit_id = twit_id).first()
        # note that the query object is over all records
        # to get the specific twit we use the first() methods
        # having obtained the twits object we can access the text as 
        # the attribute twit.twit
        form.twit.data = twit.twit
        form.twit_id.data = twit_id
        return render_template('edit_twit_mysql.html',form=form)
    if form.validate_on_submit():
        # get the twit_id back from the form
        twit_id = form.twit_id.data
        # load that twit
        twit = Twits.query.filter_by(twit_id = twit_id).first()
        # change the twit text to the text submitted in the form
        twit.twit = form.twit.data
        # commit the change
        db.session.commit()
        # so in summary, the way to update db entries is
        # 1. retrieve the object you want to change
        # 2. change the attribute
        # 3. commit the session
        # see also
        # https://stackoverflow.com/questions/6699360/flask-sqlalchemy-update-a-rows-information#6701188
        return redirect(vs_url_for('index'))
    return render_template('edit_twit_mysql.html',form=form)

@app.route('/delete_twit', methods = ['GET', 'POST'])
@login_required
def delete_twit():
    if request.args.get('id'):
        twit_id = request.args.get('id')
        twit_for_deletion = Twits.query.filter_by(twit_id = twit_id).first()
        # deleting records is simple
        # instead of add() use delete()
        # see http://flask-sqlalchemy.pocoo.org/2.3/queries/#deleting-records
        db.session.delete(twit_for_deletion)
        db.session.commit()
    return redirect(vs_url_for('index'))
   
@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        password = form.password.data	
        username = form.username.data
        # get the user object via sqlalchemy 
        user = Users.query.filter_by(username=username).first()
        # use the password helper to validate the password
        if ph.validate_password(password,user.salt,user.hashed):
            login_user(user)
            return redirect(vs_url_for('index'))
        else:
            flash('please try again')
    return render_template('login.html',form=form)

      
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    logout_user()
    return redirect(vs_url_for('index'))

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8000)
