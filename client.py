import requests

class APIClient:
    def __init__(self, endpoint):
        """em arq_config, deve-se passar um objeto path"""

        self.endpoint = endpoint
        self.response = None
        self.data = None

    def metodo_get(self, params):
        """funcao que faz a requisição get e recebe o objeto em json"""
        self.response = requests.get(url = self.endpoint, params= params)
        self.data = self.response.json()
        return self.data

    def get_status_code(self):
        if self.response is None:
            return None
        return self.response.status_code