from flask_login import UserMixin

from .firestore_service import get_user 

class UserData:
    def __init__(self, username, password):
        self.username = username
        self.password = password


class UserModel(UserMixin):
    def __init__(self, user_data):
        '''
        ;param user_data = UserData
        '''
        self.id = user_data.username
        self.password = user_data.password

    # Hace un query en la base de datos del usuario y entrega su username y password
    @staticmethod
    def query(user_id):
        user_doc = get_user(user_id) # busca en la base datos
        user_data = UserData( #convierte el user en una instancia
            username=user_doc.id,
            password=user_doc.to_dict()['password']
        )
        return UserModel(user_data)