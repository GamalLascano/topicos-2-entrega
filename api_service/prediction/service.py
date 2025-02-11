import requests

class PredictionRequest:
    def __init__(self, inputs = []):
        self.inputs = inputs


def Predict(request: PredictionRequest):
    response = requests.post('http://prediction_service:5005/predict', json={'inputs': request.inputs})
    return response

def CreateResponse(rsp: requests.Response):
    return {'probability': rsp.json()['probability']}