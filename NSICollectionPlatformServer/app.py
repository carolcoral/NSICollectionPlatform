from flask import Flask
from flask import request

from dataSource import DataSource
import hashlib

app = Flask(__name__)

db = DataSource(host="118.24.151.27", username="admin", password="Liu947752894!", database="NSI")


def create_token(message):
    m2 = hashlib.md5()
    m2.update(message.encode("utf8"))
    return m2.hexdigest()


def valid_login(username, password):
    sql = 'SELECT * FROM USER WHERE username="' + username + '" AND password="' + password + '"'
    return db.fetchone(sql=sql)


@app.route('/login', methods=['POST'])
def login():
    res = {}
    if request.method == 'POST':
        result = valid_login(request.values['username'], request.values['password'])
        if len(result) == 0:
            res = {
                "code": "000000",
                "desc": "SUCCESS",
                "data": {
                    "token": "",
                    "role": ""
                }
            }
        else:
            res = {
                "code": "000000",
                "desc": "SUCCESS",
                "data": {
                    "token": create_token(result['username']+result['password']),
                    "role": result['role']
                }
            }
    return res


if __name__ == '__main__':
    app.run()
