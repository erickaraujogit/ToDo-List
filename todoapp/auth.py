import functools
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from .db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")

def login_required(view):
    """Decorator to require login for a view."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view

@bp.before_app_request
def load_logged_in_user():
    """Load the logged-in user from the session."""
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        db = get_db()
        g.user = db.execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()

@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username =  request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        
        if not username:
            error = "Username Obrigatorio."
        
        elif not password:
            error = "Password Obrigatorio."
        
        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} already exists."
            else:
                return redirect(url_for("auth.login"))
        flash(error)
    return render_template("auth/register.html")