import secrets
import string
from urllib.parse import urlparse

from flask import abort, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from lostandfound import db
from lostandfound.config import USER_EMAIL_DOMAIN
from lostandfound.email.email import send_otp, send_pwreset, verify_domain
from lostandfound.models import Grade
from lostandfound.user import create_user, find_by_email

from . import auth_bp


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if email == "" or password == "":
            return redirect(url_for("auth.login"))
        user = find_by_email(email)
        if user is None:
            return redirect(
                url_for(
                    "auth.create_account", email=email, next=request.args.get("next")
                )
            )
        if not user.check_password(password):
            return redirect(
                url_for(
                    "auth.login",
                    email=email,
                    msg="wrongpwd",
                    next=request.args.get("next"),
                )
            )
        login_user(user)

        next_url = request.args.get("next")
        if next_url and urlparse(next_url).netloc:
            return abort(400)

        return redirect(next_url or url_for("index"))
    return render_template("login.html")


@auth_bp.route("/reset", methods=["GET", "POST"])
def reset_password():
    if request.method == "POST":
        receiver_address = request.form["email"]
        user = find_by_email(receiver_address)
        if user is not None:
            otp_plaintext = "".join(
                secrets.choice(string.digits + string.ascii_letters) for _ in range(16)
            )
            pw_reset_url = url_for(
                "auth.check_pwreset",
                otp=otp_plaintext,
                email=receiver_address,
                next=request.args.get("next"),
                _external=True,
            )
            user.set_pwreset(otp_plaintext)
            db.session.commit()
            send_pwreset(receiver_address, user, pw_reset_url)
        return redirect(url_for("auth.reset_password", msg="sent"))

    return render_template("pwreset/index.html")


@auth_bp.route("/reset/link", methods=["GET", "POST"])
def check_pwreset():
    if request.method == "POST":
        next_url = request.args.get("next")
        email = request.args.get("email")
        otp = request.args.get("otp")
        password = request.form["password"]
        password_repeat = request.form["password-repeat"]
        if password == "" or password != password_repeat:
            return redirect(
                url_for(
                    "auth.check_pwreset",
                    msg="pwdnomatch",
                    email=email,
                    otp=otp,
                    next=next_url,
                )
            )
        user = find_by_email(email)
        if user is None:
            return redirect(url_for("auth.reset_password"))
        if not user.check_pwreset(otp):
            return redirect(url_for("auth.reset_password", msg="wrongotp"))
        user.set_password(password)
        user.set_pwreset(None)
        db.session.commit()
        login_user(user)
        return redirect(next_url or url_for("index"))

    return render_template("pwreset/check.html")


@auth_bp.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@auth_bp.route("/create_account", methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        email = request.form["email"]
        if email == "":
            return redirect(url_for("auth.create_account"))
        display_name = request.form["display_name"]
        if display_name == "":
            return redirect(url_for("auth.create_account"))
        password = request.form["password"]
        if password == "":
            return redirect(url_for("auth.create_account"))
        password_repeat = request.form["password-repeat"]
        grade = request.form["grade"] or None
        if password != password_repeat:
            return redirect(
                url_for(
                    "auth.create_account",
                    msg="pwdnomatch",
                    email=email,
                    grade=request.form["grade"],
                    display_name=display_name,
                    next=request.args.get("next"),
                )
            )

        if find_by_email(email) is not None:
            return redirect(
                url_for(
                    "auth.create_account",
                    msg="existent",
                    email=email,
                    grade=request.form["grade"],
                    display_name=display_name,
                    next=request.args.get("next"),
                )
            )
        user = create_user(email, display_name, password, grade)
        login_user(user)

        next_url = request.args.get("next")
        if next_url and urlparse(next_url).netloc:
            return abort(400)

        return redirect(next_url or url_for("index"))

    grades_from_db = Grade.query.all()
    return render_template("create_account.html", grade_list=grades_from_db)


@auth_bp.route("/verification/", methods=["GET", "POST"])
@login_required
def verify_account():
    if request.method == "POST":
        receiver_address = request.form["verif_mail"]
        if receiver_address == "":
            return redirect(url_for("auth.verify_account"))
        if not verify_domain(receiver_address):
            return redirect(url_for("auth.verify_account", msg="wrongdomain"))

        otp_plaintext = "".join(secrets.choice(string.digits) for _ in range(6))
        current_user.set_otp(otp_plaintext)
        db.session.commit()
        send_otp(receiver_address, current_user, otp_plaintext)
        return redirect(url_for("auth.check_verification"))

    prefill = current_user.email if verify_domain(current_user.email) else ""
    return render_template(
        "verification/index.html",
        prefill=prefill,
        email_domain=USER_EMAIL_DOMAIN,
    )


@auth_bp.route("/verification/check", methods=["GET", "POST"])
@login_required
def check_verification():
    if request.method == "POST":
        received_otp = request.form["otp"]
        if received_otp == "" or not current_user.check_otp(received_otp):
            return redirect(url_for("auth.check_verification", msg="wrongotp"))

        current_user.account_verified = True
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("verification/check.html")
