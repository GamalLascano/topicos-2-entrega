from flask import Flask, request

from subscription_manager.service import isValidToken
from rate_limit.service import isRateLimited
from logger.service import StartTimer, Log

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/service')
def same_entity():
    start_time = StartTimer()
    authToken = request.headers.get('Authorization')
    if (authToken):
        validation = isValidToken(authToken)
        if validation.isValid:
            if isRateLimited(authToken, validation.subscription):
                Log(authToken, validation.subscription, start_time, 'POST', '/service', 429)
                return 'Rate limit exceeded', 429
            Log(authToken, validation.subscription, start_time, 'POST', '/service', 200)
            return 'Request was validated!', 200
        Log(authToken, 'NOT_VALID', start_time, 'POST', '/service', 403)
        return 'Invalid token', 403
    Log('NO_TOKEN', 'NOT_VALID', start_time, 'POST', '/service', 401)
    return 'No token provided', 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)