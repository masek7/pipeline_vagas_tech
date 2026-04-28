import requests
from pathlib import Path
import json
import time


path = Path('config.json')
arquivo_key_api = Path('api_key.json')
endpoint = "https://www.themuse.com/api/public/jobs"
dados = {}



def get_api_key():
    """função que obtém a chave da api caso não exista o arquivo contendo ela."""

    if not arquivo_key_api.exists():
        try:
            key_api = {}
            key_api['api_key'] = input("Digite a chave da api: ")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
        else:
            contents = json.dumps(key_api)
            arquivo_key_api.write_text(contents)
            data = json.loads(arquivo_key_api.read_text(encoding='utf-8'))
            return data

    else:
        data = json.loads(arquivo_key_api.read_text(encoding='utf-8'))
        return data

def config_params(api_key):
    """função que configura os params para enviar no get da API"""
    try:

        dados['page'] = 0
        dados['api_key'] = api_key['api_key']
        dados['location'] = input("Digite a localização, em ingles: (Exemplo: Rio de Janeiro, Brazil) ")
        dados['level'] = input("Digite o nível da vaga: (Entry Level, Mid Level, Senior Level, Internship, management) ")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    else:
        contents = json.dumps(dados)
        path.write_text(contents)
        return dados

api_key = get_api_key()
params = config_params(api_key)


def get_api():
    """função que envia o get e recebe o contéudo da api."""
    response = requests.get(url= endpoint, params= params )

    print("URL FINAL: ", response.url)
    print("Status: ", response.status_code)

    if response.status_code == 200:
        data = response.json()
        arquivo_conteudo = json.dumps(data)

        print(data)

        return data
    else:
        print(response.text)


def consult_api(qtd_requisicoes=5):
    for i in range(1, qtd_requisicoes + 1):
        dados['page'] = i
        time.sleep(1.5)
        get_api()



consult_api()