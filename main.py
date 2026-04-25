import requests
from pathlib import Path
import json

path = Path('config.json')
url = "https://www.themuse.com/api/public/jobs"
dados = {}

class Pipeline:
    def __init__(self, dados = {}):
        self.dados = dados

    def config_params(self):
        try:
            self.dados['page'] = int(input("Quantas páginas você quer pesquisar?: "))
            self.dados['api_key'] = input("Digite sua chave api: ")
            self.dados['location'] = input("Digite a localização, em ingles: (Exemplo: Rio de Janeiro, Brazil")
            self.dados['level'] = input("Digite o nível da vaga: (Entry Level, Mid Level, Senior Level, Internship, management")
        except ValueError:
            pass
        else:
            contents = json.dumps(self.dados)
            path.write_text(contents)

    def read_params(self):

        try:
            contents = path.read_text()
        except FileNotFoundError:
            print("Arquivo de params não encontrado.")
        else:
            data = json.loads(contents)
            return data

    def get_new_data(self):

        print("Insira os novos dados: ")
        self.config_params()

    def consult_api(self):

        if path.exists():
            check = input("Deseja mudar os dados da consulta? S/N").upper()
            if check != "N":
                self.get_new_data()
                self.read_params()

        else:
            self.config_params()
            self.read_params()

def consult_api():
    response = requests.get(url, params=)

    print("URL FINAL: ", response.url)
    print("Status: ", response.status_code)

    if response.status_code == 200:
        data = response.json()
        print(data)
        print(data['items_per_page'])
    else:
        print(response.text)