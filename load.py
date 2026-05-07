
import os
from dotenv import load_dotenv
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert
load_dotenv()

class PostgresLoader:

    def __init__(self, table_name):
        self.table_name = table_name
        self.db_host = os.getenv('DB_HOST')
        self.db_name = os.getenv('DB_NAME')
        self.db_user = os.getenv('DB_USER')
        self.db_pass = os.getenv('DB_PASS')
        self.db_port = os.getenv('DB_PORT')
        self.conn = None
        self.metrics={
            'rows_inserted': 0,
            'rows_ignored': 0,
            'rows_received': 0,
        }

    def connect_db(self):
        try:
            self.conn = psycopg2.connect(
                host = self.db_host,
                database = self.db_name,
                user = self.db_user,
                password = self.db_pass,
                port = self.db_port
            )
            print("Conexão bem-sucedida!")
        except Exception:
            raise



    def create_table(self):
      if self.conn:
            cur = self.conn.cursor()
            with open('create_table.sql', 'r') as sql_file:
                sql_script = sql_file.read()
            cur.execute(sql_script)
            self.conn.commit()
            cur.close()
      else:
          print("A conexão está fechada, abra a conexão antes.")


    def load_data(self, df):
        engine = create_engine('postgresql+psycopg2://', creator=lambda: self.conn)
        total_df = len(df)
        def upsert_method(table, conn, keys, data_iter):
            data = [dict(zip(keys, row)) for row in data_iter]
            statement = insert(table.table).values(data).on_conflict_do_nothing(index_elements=['job_id'])
            result = conn.execute(statement)
            self.metrics['rows_inserted'] += result.rowcount

        try:

            df.to_sql(self.table_name, con= engine, if_exists='append', index=False, method= upsert_method)
            self.conn.commit()

            self.metrics['rows_ignored'] = total_df - self.metrics['rows_inserted']
            self.metrics['rows_received'] = total_df

        except Exception as e:
            print(f"Um erro critico aconteceu: {e}")

    def close_connection(self):

        if self.conn:
            self.conn.close()
            print("Conexão com o banco fechada.")

    def metrics_resume(self):
        return self.metrics
