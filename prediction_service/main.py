from flask import Flask, request
from prediction_service import PredictionService

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World'

class PredictionRequest:
    def __init__(self, inputs = []):
        self.inputs = inputs
        self.service = PredictionService()

@app.route('/predict', methods=['POST'])
def predict():
    try:
        json = request.get_json()
        inputArray = json.get('inputs')
        if (inputArray):
            if (len(inputArray) == 2):
                return self.service.predict(inputArray[0], inputArray[1])
            return {'error': 'There was a problem with your request'}, 500
        return {'error': 'Request Object not valid'}, 400
    except:
        return {'error': 'Request Not Found'}, 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)