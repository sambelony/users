from flask import Flask, render_template, request, jsonify
import sys

app = Flask(__name__)

users_list = ["Serjio", "Nika", "Artur", "Julia", "Daniil", "Svetlana"]


@app.route("/")
def index():
    a = {"app": "Мое первое приложение на Python", "python": sys.version}
    return jsonify(a)


@app.route("/v1/users/")
def users():
    return jsonify(users_list)


@app.route("/v1/users/", methods=['POST'])
def user_add():
    message = "Добавлен новый пользователь %s" % request.form["name"]
    return jsonify({"result": message})


@app.route("/form/user-add/")
def page_user_add():
    return render_template("user_add_form.html")


if __name__ == "__main__":
    app.run(debug=True)
