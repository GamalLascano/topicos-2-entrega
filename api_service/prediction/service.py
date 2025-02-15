import requests

class PredictionRequest:
    def __init__(self, inputs = []):
        self.inputs = inputs


def Predict(request: PredictionRequest):
    response = requests.post('http://prediction_service:5005/predict', json={'inputs': request.inputs})

    return response

def CreateResponse(rsp: requests.Response):
    probability = 100 - abs(100 - rsp.json()['probability'] * 100)
    return {'probability': probability}