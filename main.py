import os.path
import string
import sys

from flask import Flask, render_template, request, jsonify, json, redirect
from wtforms import Form, StringField, validators
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, NoneOf, ValidationError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'THEKEY'

storage_file = "data/users.json"


def _get_content():
    default_content = {"users": [], "motorcycles": []}

    if not os.path.isfile(storage_file):
        return default_content

    storage = open(storage_file, "r")
    content = json.load(storage)
    storage.close()

    if not content:
        return default_content

    if type(content) is not dict or type(content['users']) is not list or type(content['motorcycles']) is not list:
        raise Exception("Invalid file structure in %s" % storage_file)

    return content


def _set_content(content):
    storage = open(storage_file, "w")
    json.dump(content, storage, indent=4)
    storage.close()

    return True


def get_users():
    content = _get_content()

    if "users" not in content:
        return []

    return content['users']


def storage_save_users(users_list):
    # Открыть файл
    # В хранимом json заменить список пользователей
    # Сохранить изменения
    # Закрыть файл

    data = _get_content()
    data['users'] = users_list

    result = _set_content(data)

    return result


def user_save(user):
    # Получить список пользователей
    # В конец списка пользователей добавить пользователя
    # Сохранить изменения в системе хранения

    users_list = get_users()
    users_list.append(user)
    storage_save_users(users_list)

    return True


# def input_validation(user_input):
#     if (user_input == '') or (user_input.isalpha and len(user_input) == 1) or (len(user_input) > 32):
#         return False
#     else:
#         return user_input



@app.route("/")
def index():
    a = {"app": "Мое первое приложение на Python", "python": sys.version}
    return jsonify(a)


@app.route("/v1/users/")
def users():
    users_list = get_users()
    return {"data": users_list}


# @app.route("/v1/users/", methods=['POST'])
# def user_add():
#     # Добавить пользователя в систему хранения пользователей.
#     # Вывести сообщение о результате выполнения.
#
#     if input_validation(request.form["name"]) == False:
#         return redirect("/form/user-add/")
#
#     else:
#         user = {"username": request.form["name"]}
#         result = user_save(user)
#         return {
#             "result": result,
#             "message": "Добавлен новый пользователь %s" % user['username']
#     }


@app.route("/form/user-add/")
def page_user_add():
    return render_template("user_add_form.html")


@app.route("/wtf/user-add/", methods=['GET', 'POST'])
def wt_user_add():
    form = LoginForm()

    if form.validate_on_submit():
        user = {"username": form.username.data}
        user_save(user)
        return f'Добавлен пользователь с именем {form.username.data}'

    return render_template("user_add_wtform.html", form=form)


def validate_name(form, username):
    if len(username.data) > 32:
        raise ValidationError('Имя не должно быть длинее 32 символов')
    elif username.data.isalpha() and len(username.data.strip()) == 1:
        raise ValidationError('Имя не может состоять из одной буквы')
    elif username.data.isspace():
        raise ValidationError('Имя не может быть пустым')
    elif username.data.strip() != username.data:
        raise ValidationError('Имя не должно содержать пробелов в начале и в конце')


class LoginForm(FlaskForm):
    username = StringField('Name', validators=[InputRequired("Пожалуйста, введите имя пользователя"), validate_name])


if __name__ == "__main__":
    app.run(debug=True)
