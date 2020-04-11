# $ export FLASK_APP=main.py
# $ echo $FLASK_APP
# $ export FLASK_DEBUG=1
# $ export FLASK_ENV="development"

import unittest
from flask import request, make_response, redirect, render_template, session, url_for, flash
from flask_login import login_required, current_user

from app import create_app
from app.forms import TodoForm, DeleteTodoForm, UpdateTodoForm
from app.firestore_service import get_todos, put_todo, delete_todo, update_todo

app = create_app()



@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)


@app.errorhandler(500)
def server_error(error):
    return render_template('500.html', error=error)


# Guardar en cookie
@app.route('/')
def index():
    user_ip = request.remote_addr

    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip

    return response


# Decorador. Path en browser '/hello' para correr funcion
@app.route('/hello', methods=['GET', 'POST'])
@login_required
def hello():
    user_ip = session.get('user_ip')
    username = current_user.id # Obtenermos username

    todo_form = TodoForm() # instancia de TodoForm
    delete_form = DeleteTodoForm() # instancia de DeleteTodoForm
    update_form = UpdateTodoForm() # instancia de UpdateTodoForm

    context = {
        'user_ip': user_ip,
        'todos': get_todos(user_id=username),
        'username': username,
        'todo_form': todo_form,
        'delete_form': delete_form,
        'update_form': update_form,
    }

    if todo_form.validate_on_submit():
        # Crear la tarea en db
        put_todo(user_id=username, description=todo_form.description.data)

        flash('Tu tarea se ha creado con éxito!')

        return redirect(url_for('hello'))

    return render_template('hello.html', **context)


@app.route('/todos/delete/<todo_id>', methods=['POST']) # ruta dinámica <>
def delete(todo_id):
    user_id = current_user.id
    delete_todo(user_id=user_id, todo_id=todo_id)

    return redirect(url_for('hello'))


@app.route('/todos/update/<todo_id>/<int:done>', methods=['POST']) # ruta dinámica <>
def update(todo_id, done):
    user_id = current_user.id

    update_todo(user_id=user_id, todo_id=todo_id, done=done)

    return redirect(url_for('hello'))