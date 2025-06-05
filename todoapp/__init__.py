import os
from flask import Flask

def create_app(test_config=Nome):
    #cria instancia do app flask
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        
        DATABASE=os.path.join(app.instance_path, "todolist.sqlite"),
    )
    
    #pega pasta da instancia
    try: 
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    #registra o BD
    from.import db
    db.init_app(app)
    
    #blueprints da aplicação
    from.import auth
    app.register_blueprint(auth.bp)
    
    from.import todo
    app.register_blueprint(todo).bp
    
    '''rota principal'''
    app.add_url_rule("/", endpoint="pages.index")
    
    return app