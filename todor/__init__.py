# ACA IRAN LAS CONFIGURACIONES BASICAS DEL PROYECTO #
from flask import Flask, render_template
#! extension para conectar con la base de datos
from flask_sqlalchemy import SQLAlchemy


# creamos la extension de SQLAlchemy
db = SQLAlchemy()

#! instancias de la app
def create_app():

    app = Flask(__name__)
    
    #* Configuracion del proyecto
    app.config.from_mapping(
        DEBUG = False,
        SECRET_KEY = '@B3t0l3dus',
        SQLALCHEMY_DATABASE_URI = "sqlite:///Todolist.db" #? creamos la base de datos
    )
    
    #! initializamos la conexion de la app con la base de datos
    db.init_app(app)

    #registrar blueprint
    from .import todo
    app.register_blueprint(todo.bp)
    
    from .import auth
    app.register_blueprint(auth.bp)
    
        
    @app.route('/')
    def index():
        return render_template('index.html')
    
    #! creamos la tabla y migramos todos los modelos a la base de datos(solo si falta migrar)
    with app.app_context():
        db.create_all()
    
    return app