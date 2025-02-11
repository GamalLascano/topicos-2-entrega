from flask import Flask, request

from prediction.service import PredictionRequest, Predict, CreateResponse
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
            try:
                inputArray = request.get_json().get('inputs')
                if (inputArray):
                    requestBody = PredictionRequest(inputArray)
                    responseBody = Predict(requestBody)
                    if responseBody.status_code == 200:
                        Log(authToken, validation.subscription, start_time, 'POST', '/service', 200)
                        return CreateResponse(responseBody), 200
                    Log(authToken, validation.subscription, start_time, 'POST', '/service', 500)
                    return 'Internal Server Error', 500
                Log(authToken, validation.subscription, start_time, 'POST', '/service', 400)
                return 'Bad Request', 400
            except:
                Log(authToken, validation.subscription, start_time, 'POST', '/service', 400)
                return 'Request body not found', 400
        Log(authToken, 'NOT_VALID', start_time, 'POST', '/service', 403)
        return 'Invalid token', 403
    Log('NO_TOKEN', 'NOT_VALID', start_time, 'POST', '/service', 401)
    return 'No token provided', 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)