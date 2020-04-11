from flask import Blueprint

# Todos los routes '/auth' serán reririgidas a este Blueprint
auth = Blueprint('auth', __name__, url_prefix='/auth')

from . import views