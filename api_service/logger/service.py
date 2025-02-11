import requests
import timeit

def StartTimer():
    return timeit.default_timer()

def Log(apiKey: str, subscription: str, executionTime: float, operation: str, endpoint: str, status: int):
    execution_time = (timeit.default_timer() - executionTime) * 1000
    executionTime = f"{execution_time:.2f} ms"
    response = requests.post('http://logger_service:5006/log', json={'apiKey': apiKey, 'subscription': subscription, 'executionTime': executionTime, 'operation': operation, 'endpoint': endpoint, 'status': status})
    if response.status_code == 201:
        return True
    return False