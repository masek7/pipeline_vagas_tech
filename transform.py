
import numpy as np
import pandas as pd


class JobTransformer:
    def __init__(self, raw_data):
        self.raw_data = raw_data


    def convert_to_df(self):
        df = pd.DataFrame(self.raw_data)
        df['job_level'] = df['levels'].str[0].str.get('name') #metodo para acessar itens em listas que contem dicts
        df['company_id'] = df['company'].str.get('id') #metodo para acessar itens em dicts
        df.to_csv('raw_data.csv', index=False, encoding='utf-8')

        return df

    def extract_and_join(self, dict_list):
        extracted_values = []
        for dictonary in dict_list:
            key, value = next(iter(dictonary.items()))
            extracted_values.append(str(value))

        return ' | '.join(extracted_values)

    def create_new_df(self, df):
        clear_df = df.copy()
        clear_df['location_name'] = clear_df['locations'].apply(self.extract_and_join)
        clear_df['company_name'] = clear_df['company'].str.get('name')
        clear_df['landing_page'] = clear_df['refs'].str.get('landing_page')
        clear_df['levels'] = clear_df['levels'].apply(self.extract_and_join)
        clear_df['categories'] = clear_df['categories'].apply(self.extract_and_join)
        clear_df.rename(columns={'id':'job_id'}, inplace=True)
        clear_df.rename(columns={'name':'job_name'}, inplace=True)
        clear_df.rename(columns={'categories':'category'}, inplace=True)
        clear_df = clear_df.drop(['type','contents','short_name','model_type','locations', 'refs','company','tags', 'job_level'], axis=1)
        clear_df.insert(0,'job_id', clear_df.pop('job_id'))

        clear_df.to_csv('clear_data.csv', index=False, encoding='utf-8')

        return clear_df

    def standardizes_data(self):

        df = self.create_new_df(self.convert_to_df())
        df['job_id'] = pd.to_numeric(df['job_id'], errors='coerce')
        df['job_name'] = df['job_name'].astype('string')
        df['publication_date'] = pd.to_datetime(df['publication_date'], errors='coerce')

        df['category'] = df['category'].replace(r'^\s*$', np.nan, regex=True)
        df['category'] = df ['category'].astype('string')

        df['levels'] = df['levels'].replace(r'^\s*$', np.nan, regex=True)
        df['levels'] = df['levels'].astype('string')

        df['company_id'] = pd.to_numeric(df['company_id'], errors='coerce')

        df['location_name'] = df['location_name'].replace(r'^\s*$', np.nan, regex=True)
        df['location_name'] = df['location_name'].astype('string')

        df['company_name'] = df['company_name'].replace(r'^\s*$', np.nan, regex=True)
        df['company_name'] = df['company_name'].astype('string')

        df['landing_page'] = df['landing_page'].replace(r'^\s*$', np.nan, regex=True)
        df['landing_page'] = df['landing_page'].astype('string')

        df['category'] = df['category'].fillna('unknown')
        df['levels'] = df['levels'].fillna('unknown')
        df['location_name'] = df['location_name'].fillna('unknown')
        df['landing_page'] = df['landing_page'].fillna('unknown')
        df['company_name'] = df['company_name'].fillna('unknown')

        df.dropna(subset=['job_id', 'job_name', 'publication_date', 'company_id'], inplace=True)
        df.drop_duplicates(subset=['job_id'], inplace=True)

        return df