
import json
from extract import JobExtractor
from transform import JobTransformer
from load import PostgresLoader
from pathlib import Path
import sys

config_file = Path('config.json')
api_key_file = Path('api_key.json')

def colect_data(api_key_file):
    try:
        page = 0
        location = input("Digite a localização, em inglês (Exemplo: Rio de Janeiro, Brazil): ")
        level = input("Digite o nível da vaga (Entry Level, Mid Level, Senior Level, Internship, management): ")
        api_key = json.loads(api_key_file.read_text(encoding='utf-8'))
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    else:
        return {
            "page": page,
            "location": location,
            "level": level,
            "api_key": api_key['api_key']
        }

def save_data(data, config):

    try:
        contents = json.dumps(data)
        config.write_text(contents)
    except Exception as e:
        print(f"Ocorreu um erro: {e}")


class PipelineRunner:

    def __init__(self, params, config_file, table_name, qty_page):
        self.params = params
        self.config_file = config_file
        self.table_name = table_name
        self.qty_page = qty_page

    def run(self):

        save_data(self.params, self.config_file)
        extractor = JobExtractor(self.qty_page, self.params)
        data_pagination = extractor.data_pagination()
        transform = JobTransformer(data_pagination)
        standard_df= transform.standardizes_data()
        loader= PostgresLoader(self.table_name)

        try:
            loader.connect_db()
            loader.create_table()
            loader.load_data(standard_df)

        except Exception as e:
            print(f"Erro: {e}. A execução do pipeline foi parada.")
            sys.exit(1)
        else:
            metrics_resume = loader.metrics_resume()
            print(f"Linhas recebidas: {metrics_resume['rows_received']}\n"
                  f"Linhas inseridas: {metrics_resume['rows_inserted']}\n"
                  f"Linhas ignoradas: {metrics_resume['rows_ignored']}")
        finally:
            loader.close_connection()


pipeline = PipelineRunner(colect_data(api_key_file), config_file,'job_vacancies',5)

pipeline.run()