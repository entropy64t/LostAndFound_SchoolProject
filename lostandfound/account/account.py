from flask import redirect, render_template, request, url_for, make_response
from flask_login import current_user, login_required
from sqlalchemy import text

from lostandfound import db
from lostandfound.account import account_bp
from lostandfound.models import Grade, all_grades, get_user, find_by_email, create_user, all_users, Report, get_report, all_matches


@account_bp.route("/", methods=["GET", "POST"])
@login_required
def account():
    if request.method == "POST":
        new_grade = request.form["grade"]
        if new_grade == "":
            current_user.grade = None
        else:
            current_user.grade = new_grade

        new_name = request.form["display_name"]
        if new_name == "":
            return redirect(url_for("account.account"))

        current_user.display_name = new_name
        db.session.commit()

        new_password = request.form["new_password"]
        if new_password != "":
            new_password_repeat = request.form["new_password-repeat"]
            if new_password == new_password_repeat:
                old_password = request.form["password"]
                if current_user.check_password(old_password):
                    current_user.set_password(new_password)
                    db.session.commit()
                else:
                    return redirect(url_for("account.account", msg="wrongpwd"))
            else:
                return redirect(url_for("account.account", msg="pwdnomatch"))

        new_email = request.form["new_email"]
        if new_email != "":
            new_email_repeat = request.form["new_email-repeat"]
            if new_email == new_email_repeat:
                current_user.email = new_email
                db.session.commit()
            else:
                return redirect(url_for("account.account", email_msg="emailnomatch"))

        return redirect(url_for("account.account"))

    user_grade = current_user.grade_obj
    if user_grade != None:
        grade_name = user_grade.name
    else:
        grade_name = "not set"

    grades_from_db = all_grades()
    res = make_response(render_template("account/index.html", grade_id=current_user.grade, grade_name=grade_name, grade_list=grades_from_db))
    res.headers['Cache-Control'] = 'no-store'
    return res


@account_bp.route("/delete", methods=["GET", "POST"])
@login_required
def delete_account():
    if request.method != "POST":
        return render_template("account/delete.html")

    password = request.form["password"]
    if not password:
        return redirect(url_for("account.delete_account"))

    if not current_user.check_password(password):
        return redirect(url_for("account.delete_account", msg="wrongpwd"))

    db.session.delete(current_user)
    db.session.commit()
    return redirect(url_for("index"))
