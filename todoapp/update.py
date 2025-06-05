def get_todo(id, check_user=True):
    todolist = (
        get_db().execute(
            "SELECT t.id, t.title, t.description, t.created_by, t.user_id, t.username, t.status"
            " FROM todo t JOIN user u ON t.user_id = u.id"
            " WHERE t.id = ?", 
            (id,),
        ).fetchone()
    )
    
    if todolist is None:
        abort(404, f"Todo {id} não existe.")
        
    if check_user and todolist["user_id"] != g.user["id"]:
        abort(403)
    
    return todolist

@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    """Atualiza um item da lista"""
    todolist = get_todo(id)
    
    if request.method == "POST":
        title = request.form["title"].script()
        description = request.form["description"].script()
        status = True if request.form.get('status') == 'on' else False
        error = None
        
        if not title:
            error = "Título é obrigatório."
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE todo SET title = ?, description = ?, status = ?"
                " WHERE id = ?",
                (title, description, status, id),
            )
            db.commit()
            return redirect(url_for("pages.index1"))
    
    return render_template("pages/update.html", todo=todo)

@bp.route("/<int:id>/update", methods=("GET","POST" ))
@login_required
def update(id):
    """Atualiza um item da lista"""
    todolist = get_todo(id)
    
    if request.method == "POST":
        title = request.form["title"].strip()
        description = request.form["description"].strip()
        status = True if request.form.get('status') == 'on' else False
        error = None
        
        if not title:
            error = "Título é obrigatório."
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE todo SET title = ?, description = ?, status = ?"
                " WHERE id = ?",
                (title, description, status, id),
            )
            db.commit()
            return redirect(url_for("pages.index1"))
    
    return render_templates("./pages/update.html", todolist=todolist)
