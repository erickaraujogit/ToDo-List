from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from werkzeug.security import abort
from .auth import login_required
from .db import get_db

bp = Blueprint("pages", __name__)

@bp.route("/")

def index():
    """exibe a lista"""
    db = get_db()
    todolist = db.execute(
        "SELECT t.id, t.title, t.description, t.created_by, u.username, t.status"
        " FROM todo t JOIN user u ON t.user_id = u.id"
        "ORDER BY created_by DESC"
        ).fetchall()
    return render_template("pages/index1.html", todolist=todolist)
