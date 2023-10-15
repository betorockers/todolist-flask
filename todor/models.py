from todor import db
# ACA IRAN LOS MODELOS #

#* modelo para usuario
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    
    #* creamos nuestro constructor
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
    #* creamos una funcion de representacion
    def __repr__(self):
        return f'<User: {self.username}>'
    
#* modelo para TodoList (este usuario tendra varias tareas)
class Todo(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) #? armamos la relacion con User
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    state = db.Column(db.Boolean, default = False)
    
    #* creamos nuestro constructor
    def __init__(self, created_by, title, description, state = False):
        self.created_by = created_by
        self.title = title
        self.description = description
        self.state = state
        
    #* creamos una funcion de representacion
    def __repr__(self):
        return f'<Todo: {self.title}>'
    