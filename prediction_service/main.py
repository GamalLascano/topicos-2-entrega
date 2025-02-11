from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World'

class PredictionRequest:
    def __init__(self, inputs = []):
        self.inputs = inputs

@app.route('/predict', methods=['POST'])
def predict():
    try:
        json = request.get_json()
        inputArray = json.get('inputs')
        if (inputArray):
            return {'probability': 0.7, 'inputs': inputArray}
        return {'error': 'Request Object not valid'}, 400
    except:
        return {'error': 'Request Not Found'}, 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)