from flask import Flask, render_template, request, redirect, url_for, abort
from markupsafe import escape
from enum import Enum
from flask_login import LoginManager, login_required, login_user, logout_user
from user import User, get_user, find_by_username, create_user, _USERS

app = Flask(__name__)
app.secret_key = "Bda4L_rbDg2nMbE0Z3ZALk-zK2ODy5eCXyAfTCObtjg"
login_manager = LoginManager(app)
login_manager.login_view = "login"

class ItemType(Enum):
    UMBRELLA = "Umbrella"
    COAT = "Coat / Jacket"
    PHONE = "Phone"
    OTHER = "Other"
    
class ItemColour(Enum):
    BLACK = "black"
    WHITE = "white"
    BEIGE = "beige"
    RED = "red"
    BLUE = "royalblue"
    GREEN = "green"
    LIGHT_BLUE = "skyblue"
    PINK = "pink"
    
@app.route("/new", methods=["GET", "POST"])
@login_required
def new():
    if request.method == "POST":
        title = request.form['title']
        item_type = ItemType(request.form['item-type'])
        item_color = ItemColour(request.form['item-color'])
        post_content = request.form['post-content']
        
        # TODO - update db
        
        return redirect(url_for("index"))
        
    return render_template("new.html", item_types=ItemType, item_colors=ItemColour)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = find_by_username(username)
        if user is None:
            # user does not exist
            return redirect(url_for("create_account", username=username))
        if not user.check_password(password):
            return redirect(url_for("index"))
        login_user(user)

        next = request.args.get("next")
        #if not url_has_allowed_host_and_scheme(next, request.host):
        #    return abort(400)

        return redirect(next or url_for("index"))
    return render_template("login.html")

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return render_template("index.html")

@app.route("/create_account", methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_repeat = request.form["password-repeat"]
        if password != password_repeat:
            return render_template("create_account.html")
        user = create_user(username, "", password)
        login_user(user)

        next = request.args.get("next")
        #if not url_has_allowed_host_and_scheme(next, request.host):
        #    return abort(400)

        return redirect(next or url_for("index"))
    return render_template("create_account.html")

@app.route("/account", methods=["GET", "POST"])
def account():
    return "nothing here"

@app.route("/")
def index():
    # TODO - pull from db
    
    return render_template("index.html", users=_USERS.values())

@app.route("/lost")
def lost():
    # TODO - pull from db
    
    return render_template("lost.html")

@app.route("/found")
def found():
    # TODO - pull from db
    
    return render_template("found.html")

@login_manager.user_loader
def load_user(user_id: str):
    return get_user(user_id)