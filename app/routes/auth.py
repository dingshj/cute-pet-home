from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user

from app import db
from app.models import User

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user, remember=True)
            next_url = request.args.get("next")
            return redirect(next_url or url_for("main.dashboard"))
        flash("用户名或密码错误", "danger")
    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))
