@bp.route("/create", methods=["GET","POST"])
@login_required

def create():
    if request.method == "POST":
        title = request.form['title']
        description = request.form["description"]
        
        error = None
        if not title:
            error = "Titulo obrigatório."
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO todo (title, description, user_id) VALUES (?, ?, ?)",
                (title, description, g.user['id']),
            )
            db.commit()
            return redirect(url_for("pages.index1"))
    return render_template("pages/create.html")   