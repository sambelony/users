import os.path
import sys

from flask import Flask, render_template, request, jsonify, json

app = Flask(__name__)

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


@app.route("/")
def index():
    a = {"app": "Мое первое приложение на Python", "python": sys.version}
    return jsonify(a)


@app.route("/v1/users/")
def users():
    users_list = get_users()
    return {"data": users_list}


@app.route("/v1/users/", methods=['POST'])
def user_add():
    # Добавить пользователя в систему хранения пользователей.
    # Вывести сообщение о результате выполнения.

    user = {"username": request.form["name"]}
    result = user_save(user)

    return {
        "result": result,
        "message": "Добавлен новый пользователь %s" % user['username']
    }


@app.route("/form/user-add/")
def page_user_add():
    return render_template("user_add_form.html")


if __name__ == "__main__":
    app.run(debug=True)
