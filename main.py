import pandas as pd
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

    def get_status_code(self):
        if self.response is None:
            return None
        return self.response.status_code

class JobExtractor:
    def __init__(self, qtd_paginas, dados):
        self.qtd_paginas = qtd_paginas
        self.dados = dados
        self.apiclient = APIClient(endpoint)

        self.total_pages = 0
        self.total_vagas = 0
        self.logs = []

    def logger(self):

        self.status_code = self.apiclient.get_status_code()
        try:
            status = None
            if self.status_code == 200:
                status = "Sucesso"
            else:
                status = "Falhou"

            log = {
                "status_code": self.status_code,
                "actual_page": self.get['page'],
                "total_per_page": len(self.get['results']),
                "status": status,
            }
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
        else:
            return log

    def paginacao_dados(self):
        """metodo que itera por pela quantidade de paginas definidas"""
        vagas = []
        for page in range(1, self.qtd_paginas +1):
            #loop que faz a paginação
            self.dados['page'] = page
            time.sleep(1.5)
            self.get = self.apiclient.metodo_get(self.dados)
            self.total_pages +=1
            self.logs.append(self.logger())
            for result in self.get['results']:
                self.total_vagas +=1
                vagas.append(result)
        return vagas

class JobTransformer:
    def __init__(self, dados_brutos):
        self.dados_brutos = dados_brutos


    def convert_to_df(self):
        df = pd.DataFrame(self.dados_brutos)
        df['job_level'] = df['levels'].str[0].str.get('name') #metodo para acessar itens que estão em listas que contem dicts
        df['company_id'] = df['company'].str.get('id') #metodo para acessar itens em dicts
        df.to_csv('dados_brutos.csv', index=False, encoding='utf-8')

        return df

    def extract_and_join(self, lista_dict):
        valores_extraidos = []
        for dicionario in lista_dict:
            for valor in dicionario.values():
                valores_extraidos.append(str(valor))

        return ' | '.join(valores_extraidos)

    def create_new_df(self, df):
        df_limpo = df.copy()
        df_limpo['location_name'] = df_limpo['locations'].apply(self.extract_and_join)
        df_limpo['company_name'] = df_limpo['company'].str.get('name')
        df_limpo['link_vaga'] = df_limpo['refs'].str.get('landing_page')
        df_limpo.rename(columns={'id':'job_id'}, inplace=True)
        df_limpo = df_limpo.drop(['type','short_name','model_type','locations','levels', 'refs','company','tags'], axis=1)
        df_limpo.insert(0,'job_id', df_limpo.pop('job_id'))

        df_limpo.to_csv('dados_limpos.csv', index=False, encoding='utf-8')

        return df_limpo




params = coletar_dados(arquivo_key_api)
salva_dados(params, arq_config)
job = JobExtractor(5, params)

test = JobTransformer(job.paginacao_dados())
test.create_new_df(test.convert_to_df())

