import requests
from pathlib import Path
import json
import time


path = Path('config.json')
arquivo_key_api = Path('api_key.json')
endpoint = "https://www.themuse.com/api/public/jobs"
dados = {}


class APIClient:
    def __init__(self, arq_config, endpoint, api_key):

        """em arq_config, deve-se passar um objeto path"""

        self.dados = {}
        self.arq_config = arq_config
        self.endpoint = endpoint
        self.api_key = json.loads(api_key.read_text(encoding='utf-8'))
        self.response = None
        self.data = None

    def config_params(self):
        """ metodo que configura os parametros para a chamada da API"""
        try:
            self.dados['page'] = 0
            self.dados['api_key'] = self.api_key
            self.dados['location'] = input("Digite a localização, em ingles: (Exemplo: Rio de Janeiro, Brazil) ")
            self.dados['level'] = input("Digite o nível da vaga: (Entry Level, Mid Level, Senior Level, Internship, management) ")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
        else:
            contents = json.dumps(self.dados)
            self.arq_config.write_text(contents)
            return self.dados


    def metodo_get(self):

        """funcao que faz a requisição get e recebe o objeto em json"""

        self.response = requests.get(url = self.endpoint, params= self.config_params())
        self.data = self.response.json()
        return self.data

    def logger(self):
        if self.response.status_code == 200:
            log = {
                "page_count": self.data["page_count"],
                "items_per_page": self.data["items_per_page"],
                "total": self.data["total"]
            }
            print(log)
        else:
            print(self.response.status_code)



test = APIClient(path,endpoint,arquivo_key_api)

test.metodo_get()
test.logger()