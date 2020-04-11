import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Comunicar con la firestore ($ glcoud auth application-default login)
credential = credentials.ApplicationDefault()
firebase_admin.initialize_app(credential)

# Inicializar una instancia de firestore
db = firestore.client()

#########
# USERs #
#########

def get_users():
    return db.collection('users').get()

# Obtener usuario en db
def get_user(user_id):
    return db.collection('users').document(user_id).get()

# Registrar usuario en db
def user_put(user_data):
    user_ref = db.collection('users').document(user_data.username)
    user_ref.set({'password': user_data.password})

#########
# TODOs #
#########

# Obtener los todos
def get_todos(user_id):
    return db.collection('users').document(user_id).collection('todos').get()

# Anadir todo
def put_todo(user_id, description):
    todos_collection_ref = db.collection('users').document(user_id).collection('todos')
    todos_collection_ref.add({'description': description, 'done': False})

# Borrar todo
def delete_todo(user_id, todo_id):
    todo_ref = _get_todo_ref(user_id, todo_id) # invoca funcion privada
    todo_ref.delete()

# Update todo
def update_todo(user_id, todo_id, done):
    todo_done = not bool(done) # convertir a booleano
    todo_ref = _get_todo_ref(user_id, todo_id) # invoca funcion privada
    todo_ref.update({'done': todo_done})


# funcion privada: obtener todo_ref
def _get_todo_ref(user_id, todo_id):
    # todo_ref = db.collection('users').document(user_id).collection('todos').document(todo_id)
    return db.document('users/{}/todos/{}'.format(user_id, todo_id))