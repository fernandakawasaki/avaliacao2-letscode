from flask_restful import Resource, Api
from flask import Flask
import pandas as pd
from sankey_plot import SankeyPlot

app = Flask(__name__)
api = Api(app)

class DespesasAPI(Resource):
    month_name = {'agosto': 8,
                  'setembro': 9,
                  'outubro': 10}


    def filter_df(self, df, month):
        '''Filtra os dados com base no mes fornecido'''
        month_num = self.month_name[month]
        df['MES'] = pd.to_datetime(df['DT_EMPENHO']).dt.month
        df['MES'] = df['MES'].astype(int)
        df = df[df['MES'] == month_num]
        return df


    def load_csv(self):
        url = 'https://mid.curitiba.pr.gov.br/dadosabertos/BaseReceitaDespesa/2021-11-01_Despesas_-_Base_de_Dados.csv'
        df = pd.read_csv(url, sep=';', encoding='latin_1', skiprows=[1])
        return df


    def clean_df(self, df):
        '''Limpa o dataframe, removendo valores nulos e transformando string em float'''
        valor_nao_nulo = ~df['VL_PAGO'].isna()
        df = df[valor_nao_nulo]
        df['VL_PAGO'] = df['VL_PAGO'].replace(',', '.', regex=True).astype(float)
        return df


    def persist_df(self, filtered_df, month):
        '''Persiste os dados em JSON e CSV'''
        filtered_df.to_json(f'despesas_{month}.json', orient='records')
        filtered_df.to_csv(f'despesas_{month}.csv', index=False)
        return filtered_df


    def process_df(self, month):
        '''Obtem e processa os dados'''
        df = self.load_csv()
        df = self.clean_df(df)
        df = self.filter_df(df, month)
        return df


    def get(self, month):
        '''Retorna os dados filtrados do mes fornecido'''
        month = month.lower()

        df = self.process_df(month)  # Obtem e processa os dados
        self.persist_df(df, month)

        SankeyPlot(df, month)
        return df.to_json(orient='records')


api.add_resource(DespesasAPI, '/<string:month>')

if __name__ == '__main__':
    app.run(debug=True)