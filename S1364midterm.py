#** Nunez,Priscilla 
#** Fall 2018
#** SI364 midterm

#** Import statements 
import os
import json
import requests

#**  New ** Import used to calculate current time stamp
import time


#** New ** Provide hashing mechanism for strings - used in blockchain!
import hashlib

#** New ** Serialize json to dictionary
import ast

from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, ValidationError                   #** New ** Introduced HiddenField

from wtforms.validators import Required 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import JSON                                                            #** New ** Introduced JSON
from flask_login import LoginManager, login_user, login_required, logout_user, current_user  #** Introduced new library - pip install - flask_login and login credentials w/out password requirements
from flask_script import Manager, Shell

#** App setup code
app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'hardtoguessstringfromsi364thisisnotsupersecurebutitsok'

#** Updated database URI
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://priscillamnunez@localhost:5432/mid-term"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.debug = True

#** Statements for db setup (and manager setup if using Manager)
db = SQLAlchemy(app)


@login_manager.user_loader
def load_user(name):
    return Name.query.filter_by(name = name).first()                                         #** Database login manager

def is_valid_year(form, field):
    if field.data and field.data.isdigit():
        if int(field.data) >=1990 and int(field.data) <=2019:                                #** User cannot enter year past 2019
            return True
    raise ValidationError('Please Enter a valid year between 1990 and 2019')     




############################################
#** 4 MODELS • Name, Search, Like, Bookmark 
############################################

class Name(db.Model):
    __tablename__ = "names"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))

    def __repr__(self):
        return "{} (ID: {})".format(self.name, self.id)
    
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    
    def get_id(self):
        return str(self.name)

class Search(db.Model):
    __tablename__ = "searches"
    id = db.Column(db.Integer,primary_key=True)
    nameId = db.Column(db.Integer, db.ForeignKey('names.id'))
    searchStartYear = db.Column(db.String(64))

class Like(db.Model):
    __tablename__ = "likes"
    id = db.Column(db.Integer,primary_key=True)
    nameId = db.Column(db.Integer, db.ForeignKey('names.id'))

                                                                    #** New ** JSON datatype - Postgres gives opportunity to save JSON objects in the database 
    comic = db.Column(JSON)                                         #** Example: in Bookmarks database you will be able to view the datatype information saved!

class Bookmark(db.Model):
    __tablename__ = "bookmarks"
    id = db.Column(db.Integer,primary_key=True)
    nameId = db.Column(db.Integer, db.ForeignKey('names.id'))
    comic = db.Column(JSON)


###########################################################
#** 4 FORMS • NameForm, SearchForm, LikeForm, BookmarkForm
###########################################################

class NameForm(FlaskForm):
    name = StringField("Please enter your name.",validators=[Required()])
    submit = SubmitField()

class SearchForm(FlaskForm):
    searchStartYear = StringField("Please enter a search start year for marvels comic collections.",validators=[Required(), is_valid_year])
    submit = SubmitField()

class LikeForm(FlaskForm):
    comic = HiddenField("hidden")                      #** New ** HiddenField - form recieves data, the user will be able to click like and secretly pass the liked comic w/out viewing a form. 
    submit = SubmitField("Like")

class BookmarkForm(FlaskForm):
    comic = HiddenField("hidden")                      #** New ** HiddenField - form recieves data, the user will be able to click bookmark and secretly pass the bookmarked comic w/out viewing a form. 
    submit = SubmitField("bookmark")

#######################
#**VIEW FXNS ##########
#######################

@app.route('/', methods = ["POST", "GET"])
def home():
    if hasattr(current_user, 'name'):                  #** On the homepage - if user is already logged in the user is redirected to search page. User does not need to enter a password but can select to logout (later on). Please reference Name Model and NameForm Class.
        return redirect(url_for('search'))
    form = NameForm()                                  #** User should be able to enter name after name and each one will be saved, even if it's a duplicate! Sends data with GET
    if form.validate_on_submit():
        name = form.name.data
        newname = Name.query.filter_by(name = name).first()
        if not newname:
            newname = Name(name=name)
            db.session.add(newname)                    #** If login_user does not exists the user will be added and redirected to homepage.
            db.session.commit()
            newname = Name.query.filter_by(name = name).first()
        login_user(newname)
        return redirect(url_for('all_names'))          #** Midterm requirement
    return render_template('index.html', form=form)


@app.route('/search', methods = ["POST", "GET"])
@login_required
def search():                                         #** 3 forms created • search, like and bookmark
    results = []
    form = SearchForm()                               #** User should be able to enter name and each one will be saved, even if it's a duplicate! Sends data with GET
    form2 = LikeForm()
    form3 = BookmarkForm()

    if form.validate_on_submit():
        searchStartYear = form.searchStartYear.data            #** Communicating with years searched if not already searched code enables year to be added 
        newsearchStartYear = Search.query.filter_by(searchStartYear = searchStartYear).first()
        if not newsearchStartYear:
            newsearchStartYear = Search(searchStartYear=searchStartYear, nameId=current_user.id)
            db.session.add(newsearchStartYear)
            db.session.commit()
        
        baseUrl = 'https://gateway.marvel.com:443/v1/public'     #** Communicating with API

        ts= time.time();                                         #** New ** imported time library
        publicKey = 'b5d493b7c3c88ab7de81562a4478702c'           #** publicKey provided by API
        privateKey = 'b49c0f9c09df1d78105d0abea0dbcda4b7146141'  #** privateKey provided by API
        hash = hashlib.md5(('{}{}{}').format(ts,privateKey, publicKey).encode('utf-8')).hexdigest() #** New ** Hashing public and private key with hashlib.md5
        comics = requests.get('{}/comics'.format(baseUrl), 
            params= {                                            #** Time stamp order
                "startYear": searchStartYear,
                "orderBy": "onsaleDate",
                "apikey": publicKey,
                "hash": hash,
                "ts": ts,
                "offset": 0
            })
        json_format = json.loads(comics.text)
        results = json_format['data']['results']
    errors = [v for v in form.errors.values()]                   #** Error values
    if len(errors) > 0:
        print(len(errors))
        flash("!!!! ERRORS IN FORM SUBMISSION - " + str(errors)) #** Flashes error
    
    return render_template('search.html', form=form , form2=form2, form3=form3, results=results)


@app.route('/like', methods = ["POST"])
@login_required                                                  #** logged into the system before performing requests
def like_comic():
    username = current_user.name                        
    form = LikeForm()
    comic = form.comic.data
    newlike = Like(comic=comic, nameId=current_user.id)
    db.session.add(newlike)
    db.session.commit()
    return redirect(url_for('user_likes'))

@app.route('/bookmark', methods = ["POST"])
@login_required
def bookmark_comic():
    username = current_user.name
    form = BookmarkForm()
    comic = form.comic.data
    newbookmark = Bookmark(comic=comic, nameId=current_user.id)
    db.session.add(newbookmark)
    db.session.commit()
    return redirect(url_for('user_bookmarks'))                   #** Made sure function is subscriptable


@app.route('/names')
@login_required
def all_names():
    username =current_user.name
    names = Name.query.all()
    return render_template('name_example.html',names=names, username=username)

@app.route('/bookmarks')
@login_required
def user_bookmarks():                 
    bookmarks = Bookmark.query.filter_by(nameId = current_user.id).all()
    results =  list(bookmarks)
    for items in results:
        try:
            items.comic = ast.literal_eval(items.comic)            #** New ** ast serialize JSON before passing bookmarked comics. 
        except ValueError:
            pass
    return render_template('bookmarked_comics.html', results=results)

@app.route('/likes')
@login_required
def user_likes():
    likes = Like.query.filter_by(nameId = current_user.id).all()
    results =  list(likes)
    for items in results:
        try:
            items.comic = ast.literal_eval(items.comic)           #** New ** ast serialize JSON before passing liked comics. 
        except ValueError:
            pass
    return render_template('liked_comics.html',results=results)

@app.route('/searches')
def all_searches():
    searches = Search.query.filter_by(nameId = current_user.id).all()
    return render_template('searches.html',searches=searches)

@app.route("/logout")            #** Logouts decorator
@login_required                  #** Logs out user 
def logout():                    
    logout_user()
    return "Logged out"          



@app.errorhandler(401)                                            #** Required error handler decorators used to render assigned error templates
def unauthorized(e):
    return render_template('401.html'), 401

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

                                                                  #** Included the code needed to initialize the database structure when running the application.
if __name__=='__main__':
    db.create_all()
    app.run(debug = True)
    manager.run()
