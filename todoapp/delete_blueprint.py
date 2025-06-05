@bp.route("/<int:id>/delete", methods=("POST","GET"))
@login_required
def delete(id):
    
    get_todo(id)
    db = get_db()
    db.execute("DELETE FROM todo WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("pages.index1"))