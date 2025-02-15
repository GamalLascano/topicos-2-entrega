from flask import Flask, request
from prediction.service import PredictionService

app = Flask(__name__)
service = PredictionService()

@app.route('/')
def hello_world():
    return 'Hello World'

class PredictionRequest:
    def __init__(self, inputs = []):
        self.inputs = inputs

@app.route('/predict', methods=['POST'])
def predict():
    json = request.get_json()
    inputArray = json.get('inputs')
    if (inputArray):
        if (len(inputArray) == 2):
            return {'probability': service.predict(inputArray[0], inputArray[1])}, 200
        return {'error': 'There was a problem with your request'}, 500
    return {'error': 'Request Object not valid'}, 400
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)