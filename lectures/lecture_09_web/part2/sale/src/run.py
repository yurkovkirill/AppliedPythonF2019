# TODO: код где-нибудь здесь. Если есть желание, можно и на ином языке.
# Требуется создать ручку с произвольным именем, которое вы в последствии передадите на мой сервис для проверки.
# В обработчике ручки необходимо кинуть запрос на auth сервис и получить информацию о себе
# с помощью ручки about_me (авторизация по кукам).
# Вернуть json в котором указать username, age и sale, которая рассчитывается по формуле round(age / 7).
# Кука при запросе на сервис auth должна быть вида
# {'session': '<длинный id>', 'technoatom': '<длинный id2>'}, её можно получить из запроса к сервису.
import requests
from flask import Flask, abort, jsonify, request
from flask_login import (
    LoginManager, UserMixin, login_required,
    current_user, login_user, logout_user
)

app = Flask(__name__)
HOST = '0.0.0.0'

@app.route('/', methods=['GET'])
@login_required
def get_sale():
    cook = request.cookies
    resp = requests.request(method="get", url="http://auth:5000/about_me", cookies=cook)
    age = resp.json()['age']
    return round(age / 7)
        

def main():
    app.run(host=HOST, debug=True)


if __name__ == '__main__':
    main()