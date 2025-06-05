@bp.route("/<int:id>/delete", methods=("POST","GET"))
@login_required
def complete(id):
    status = True
    
    db = get_db()
    db.execute(
        "UPDATE todo SET status = ? WHERE id = ?",
        (status, id),
    )
    db.commit()
    return redirect(url_for("pages.index1"))
