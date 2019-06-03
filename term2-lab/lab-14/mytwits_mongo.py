from flask import Flask, request
from flask import render_template
from flask import redirect, url_for
import pymongo
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import HiddenField
from wtforms import SubmitField
from wtforms import validators
from vs_url_for import vs_url_for
from bson import ObjectId



class addTwitForm(FlaskForm):
    twit = StringField('twit', validators = [validators.DataRequired()])
    user = StringField('user', validators = [validators.DataRequired()])
    submit = SubmitField('submit', [validators.DataRequired()])




class editTwitForm(FlaskForm):
    twit = StringField('twit', validators = [validators.DataRequired()])
    user = HiddenField('user')
    twit_id = HiddenField('twit_id')
    submit = SubmitField('submit', [validators.DataRequired()])





class DBHelper:

    def __init__(self):
        client = pymongo.MongoClient()
        self.db = client['mytwits']

    def get_all_twits(self):
        return self.db.twits.find().sort('created_at',pymongo.DESCENDING)

    def get_twit(self,twit_id):
        return self.db.twits.find({'_id': ObjectId(twit_id)})

    def update_twit(self,twit,user,twit_id):
        return self.db.twits.update({'_id': ObjectId(twit_id)}, {'twit':twit,'username':user})

    def add_twit(self,twit,user):
        return self.db.twits.insert({'twit':twit,'username':user,'created_at': datetime.datetime.utcnow()})

    def delete_twit(self,twit_id):
        return self.db.twits.remove({'_id': ObjectId(twit_id)})



app = Flask(__name__)
db = DBHelper()
app.secret_key = 'hto%s&gw3^!5m+i8b87yoo9!sh1!2$6d^d#uk%*=bvcmj^(df('


@app.route('/')
def index():
    twits = db.get_all_twits()
    return render_template("mytwits_mongo.html", twits=twits)



@app.route('/add_twit', methods = ['GET', 'POST'])
def add_twit():
    form = addTwitForm()
    if form.validate_on_submit():
        twit = form.twit.data
        user = form.user.data

        db.add_twit(twit,user)
        return redirect(vs_url_for('index'))
    return render_template('add_twit_mongo.html',form=form)

@app.route('/edit_twit', methods = ['GET', 'POST'])
def edit_twit():
    form = editTwitForm()
    if request.args.get('id'):
        twit_id = request.args.get('id')
        twit = db.get_twit(twit_id)
        form.twit.data = twit[0]['twit']
        form.user.data = twit[0]['username']
        form.twit_id.data = twit_id
        return render_template('edit_twit_mongo.html',form=form,twit=twit)
    if form.validate_on_submit():
        twit = form.twit.data
        user = form.user.data
        twit_id = form.twit_id.data
        db.update_twit(twit,user,twit_id)
        return redirect(vs_url_for('index'))
    return render_template('edit_twit_mongo.html',form=form)

@app.route('/delete_twit', methods = ['GET', 'POST'])
def delete_twit():
    if request.args.get('id'):
        twit_id = request.args.get('id')
        twit = db.delete_twit(str(twit_id))
    return redirect(vs_url_for('index'))

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8000)
