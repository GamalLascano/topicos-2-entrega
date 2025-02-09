from flask import Flask, request

from subscription_manager.service import isValidToken

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/service')
def same_entity():
    authToken = request.headers.get('Authorization')
    if (authToken):
        validation = isValidToken(authToken)
        if validation.isValid:
            return 'Request was validated!', 200
        else:
            return 'Invalid token', 403
    else:
        return 'No token provided', 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)