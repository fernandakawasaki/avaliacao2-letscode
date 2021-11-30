import plotly.graph_objects as go

class SankeyPlot():
    def __init__(self, df, month):
        self.group_link1, self.group_link2 = self.create_links(df)

        # Labels e dict que sera usado para consultar o indice de uma dada label
        self.label = self.get_unique_labels()
        self.label_source = {self.label[i]: i for i in range(len(self.label))}

        # Dados para plotar os links
        self.source = self.get_source()
        self.target = self.get_target()
        self.values = self.get_values()

        self.plot_graph(month)


    def create_links(self, df):
        '''Cria groups que correspondem aos links'''
        group_link1 = df.groupby(['DS_FUNCAO', 'DS_ORGAO']).agg({'VL_PAGO': 'sum'})
        group_link2 = df.groupby(['DS_ORGAO', 'DS_MODALIDADE']).agg({'VL_PAGO': 'sum'})
        return group_link1, group_link2


    def get_unique_labels(self):
        '''Obtem todas as labels unicas'''
        label = list(self.group_link1.index.get_level_values('DS_FUNCAO').unique())
        label.extend(list(self.group_link1.index.get_level_values('DS_ORGAO').unique()))
        label.extend(list(self.group_link2.index.get_level_values('DS_MODALIDADE').unique()))
        return label


    def get_source(self):
        '''Obtem as origens do sankey plot'''
        s = list(self.group_link1.index.get_level_values('DS_FUNCAO'))
        s.extend(list(self.group_link2.index.get_level_values('DS_ORGAO')))
        source = [self.label_source[element] for element in s]
        return source


    def get_target(self):
        '''Obtem os alvos do sankey plot'''
        t = list(self.group_link1.index.get_level_values('DS_ORGAO'))
        t.extend(list(self.group_link2.index.get_level_values('DS_MODALIDADE')))
        target = [self.label_source[element] for element in t]
        return target


    def get_values(self):
        '''Obtem os valores da espessura dos links do sankey plot'''
        values = list(self.group_link1.values)
        values.extend(list(self.group_link2.values))
        return values


    def plot_graph(self, month):
        '''Plota o grafico usando Plotly'''
        fig = go.Figure(data=[go.Sankey(
            node = dict(
            pad = 15,
            thickness = 20,
            line = dict(color = "black", width = 0.5),
            label = self.label,
            color = "blue"
            ),
            link = dict(
            source = self.source,
            target = self.target,
            value = self.values
        ))])

        fig.update_layout(title_text=f'Distribuição dos gastos da prefeitura de Curitiba em {month} de 2021', font_size=10)
        fig.write_image(f'despesas_{month}.png')
