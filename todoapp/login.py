@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)).fetchone()
        if user is None:
            error = "Username inválido."
        elif not check_password_hash(user["password"], password):
            error = "Password inválido."
        
        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("pages.index1"))
        flash(error)
    return render_template("auth/login.html")