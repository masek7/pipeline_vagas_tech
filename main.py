import requests
from pathlib import Path
import json
import time

arq_config = Path('config.json')
arquivo_key_api = Path('api_key.json')
endpoint = "https://www.themuse.com/api/public/jobs"

def coletar_dados(arquivo_api_key):
    try:
        page = 0
        location = input("Digite a localização, em inglês (Exemplo: Rio de Janeiro, Brazil): ")
        level = input("Digite o nível da vaga (Entry Level, Mid Level, Senior Level, Internship, management): ")
        api_key = json.loads(arquivo_api_key.read_text(encoding='utf-8'))
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    else:
        return {
            "page": page,
            "location": location,
            "level": level,
            "api_key": api_key['api_key']
        }

def salva_dados(dados, config):

    try:
        contents = json.dumps(dados)
        config.write_text(contents)
    except Exception as e:
        print(f"Ocorreu um erro: {e}")


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

class JobExtractor:
    def __init__(self, qtd_paginas, dados):
        self.qtd_paginas = qtd_paginas
        self.dados = dados
        self.apiclient = APIClient(endpoint)

    def paginacao_dados(self):
        """metodo que itera por pela quantidade de paginas definidas"""
        vagas = []
        for page in range(1, self.qtd_paginas +1):
            self.dados['page'] = page
            time.sleep(1.5)
            get = self.apiclient.metodo_get(self.dados)
            for result in get['results']:
                vagas.append(result)

        return vagas


params = coletar_dados(arquivo_key_api)
salva_dados(params, arq_config)
test = APIClient(endpoint)
job = JobExtractor(5, params)
job.paginacao_dados()

