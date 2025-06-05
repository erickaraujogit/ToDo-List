import sqlite3
import click
from flask import current_app
from flask import g

def get_db():
    '''reusar a conexao se já existir'''
    
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    '''fecha a conexao'''
    db = g.pop("db", None)
    
    if db is not None:
        db.close()
        
def init_db():
    '''exclui tudo e recria a tabela'''
    db = get_db()
    with current_app.open_resource("ddl.sql") as f:
        db.executescript(f.read().decode("utf8"))

@click.command("init-db")
def init_db_command():
    '''exclui tudo e recria a tabela'''
    init_db()
    click.echo("Banco de dados inicializado.")
    
def init_app(app):
    '''registra as funcoes no app'''
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    
    # cria a tabela se não existir
    db = get_db()
    with current_app.open_resource("ddl.sql") as f:
        db.executescript(f.read().decode("utf8"))