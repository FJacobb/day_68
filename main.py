from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from hash import Pwd_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

##CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

@app.route('/')
def home():
    return render_template("index.html",logged_in=current_user.is_authenticated)


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if request.form.get("email").lower() == User.query.filter_by(email=request.form.get("email").lower()).first().email:
            error = "This email is signed up already in the database, please login instead"
            return redirect(url_for("login", error=error))
        else:
            c = Pwd_hash()
            new_user = User(email=request.form.get("email"), name=request.form.get('name'), password=c.passindata(request.form.get("password")))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for("secrets"))
    return render_template("register.html", logged_in=current_user.is_authenticated)


@app.route('/login', methods=["POST","GET"])
def login():
    if request.args.get("error") == None:
        error = None
    else:
        error = request.args.get("error")
    if request.method == "POST":
        email = request.form.get('email').lower()

        password = request.form.get('password')

        # Find user by email entered.
        user = User.query.filter_by(email=email).first()
        if user == None:
            error = f"ERROR: this \'{request.form.get('email')}\'  dose not exist, please try another email."

        # Check stored password hash against entered password hashed.
        else:
            if Pwd_hash().passindata(password) == user.password:
                login_user(user)
                return redirect(url_for('secrets'))
            else:
                error = "ERROR: your password is incorrect!"

    # if request.method == "POST":

        # db = User()
        # data = db.search(request.form.get("email"))
        # c = Pwd_hash()
        # user = User()
        # if c.passindata(request.form.get("password")) == data["password"]:
        #     login_user(user)
        #     return redirect(url_for("secrets"))
    return render_template("login.html", error=error, logged_in=current_user.is_authenticated)


@app.route('/secrets')
@login_required
def secrets():
    print(current_user.name)
    return render_template("secrets.html", name=current_user.name, logged_in=True)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/download')
@login_required
def download():
    return send_from_directory("static/files","cheat_sheet.pdf", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
