import os

from flask import Flask, render_template, request, flash, redirect, session, g, abort, jsonify
import requests
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import UserAddForm, LoginForm, UserEditForm, AddGameForm
from models import db, connect_db, User, BoardGame

CURR_USER_KEY = "curr_user"

api_key = 'AIzaSyBgMTRBvh9AE3_WRD_z-htK-rlgRAtDadI'
app = Flask(__name__, static_folder='scripts')

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///warbler'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)


@app.before_request
def add_user_to_g():
    """if logged in add current user to Flask global"""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None

def do_login(user):
    """log in user"""

    session[CURR_USER_KEY] = user.id

def do_logout():
    """log in user"""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET","POST"])
def signup():
    """Handle user sign up"""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user= User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                location= form.location.data,
                image_url=form.image_url.data or  User.image_url.default.arg
            )
            db.session.commit()
        except IntegrityError as e:
            flash("username already taken", "danger")
            return render_template("signup.html", form=form)
        
        do_login(user)

        return redirect("/")
    else:
        return render_template("signup.html", form=form)
    


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""
    do_logout()
    flash("Sucessfully logged out.")
    return redirect("/login")



@app.route("/users/<int:userid>")
def user_detail(userid):
    """show user details"""
    user = User.query.get_or_404(userid)
    return render_template('userdetail.html', user=user)


@app.route("/users/<int:userid>/follow", methods=["POST"])
def toggle_follow(userid):
    """follow user if logged in"""
    if g.user:
        user= g.user
        followed_user = User.query.get_or_404(userid)
        if followed_user in  g.user.following:
            g.user.following.remove(followed_user)      
        else:
            user.following.append(followed_user)  
        db.session.commit()
    return redirect("/")

def calculate_distance(origin, destination):
        origin_formatted=""
        destination_formatted =""
        if (origin):
            origin_formatted = origin.replace(' ', '+')
        if (destination):
            destination_formatted = destination.replace(' ', '+')
        url = f'https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin_formatted}&destinations={destination_formatted}&key={api_key}'
        response = requests.get(url)
        data = response.json()
        try:
            if data['status'] == "INVALID_REQUEST":
                return "Unavailable"
            distancetext = data['rows'][0]['elements'][0]['distance']['text']
            distanceint = data['rows'][0]['elements'][0]['distance']['value']
            distance = [distancetext,distanceint]
            return distance
        except KeyError:
            return ['Unknown',999999999]



@app.route('/users/profile', methods=["GET", "POST"])
def profile():
    """Update profile for current user."""
    if g.user:
        user = g.user
        form = UserEditForm(obj=user)
        if form.validate_on_submit():
            if User.authenticate(user.username, form.password.data):
                user.username = form.username.data
                user.email = form.email.data
                user.location = form.location.data
                user.image_url = form.image_url.data or "/static/images/default-pic.png"
                db.session.commit()
                flash("changes successful")
                return redirect("/")
            else:
                flash("incorrect password")
                return redirect("/")
        else:
            return render_template("/edit.html", user = user, form = form)
    else:
        return('/')
    


@app.route('/')
def homepage():
    """Show homepage:

    - anon users: no messages
    - logged in: 100 most recent messages of followed_users
    """
    if g.user:
        following =[f.id for f in g.user.following]
        userinfo= []
        users = User.query.filter(User.id != g.user.id).all()
        for user in users:
            distance = calculate_distance(g.user.location, user.location)
            try:
                int_distance = int(distance[1])
            except ValueError:
                int_distance = 999999999
            userinfo.append([user, distance[0],int_distance])
        sorteduserinfo = sorted(userinfo, key=lambda x: x[2])
        return render_template('home.html',userpairs =  sorteduserinfo, users= users, following = following)

    else:
        return render_template('home-anon.html')



@app.route('/users/<int:user_id>/following')
def show_following(user_id):
    """Show list of people this user is following."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)
    return render_template('following.html', user=user)  



@app.route("/users/add_games", methods=["GET","POST"])
def add_games():
    """See list of games and add or remove them"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    form = AddGameForm()
    if form.validate_on_submit():
        gamename = form.gamename.data
        game = BoardGame.query.filter_by(name=gamename).first()
        if game is None:
            bgame = BoardGame(name=gamename)
            db.session.add(bgame)
            g.user.boardgames.append(bgame)
            db.session.commit()        
        else:
            usergames = g.user.boardgames
            if (game not in usergames):
                g.user.boardgames.append(game)
                db.session.commit()     
        return redirect("/users/add_games")
    return render_template("/add_game.html", user= g.user, form=form)


@app.route("/users/remove_game/<game_id>", methods=["POST"])
def remove_game(game_id):
    """remove game"""
    game = BoardGame.query.get_or_404(game_id)
    g.user.boardgames.remove(game)
    db.session.commit()
    return redirect("/users/add_games")
    