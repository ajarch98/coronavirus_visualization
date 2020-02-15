import plotly.offline as go_offline
import plotly.graph_objects as go
import pandas as pd


class Grapher():
    def __init__(self):
        self.url = 'https://docs.google.com/spreadsheets/d/18X1VM1671d99V_yd-cnUI1j8oSG2ZgfU_q1HfOizErA/export?format=csv&id'
        self.data = pd.read_csv(self.url)
        self.data = self.data.fillna(0)

    def create_graph(self):
        fig = go.Figure()
        col_names = self.data.columns

        date_list = []
        for i in range(5, len(self.data.columns), 2):
            cases_col = i
            cases_col_name = col_names[cases_col]
            deaths_col = i + 1
            deaths_col_name = col_names[deaths_col]

            df = self.data[['latitude', 'longitude', 'country', 'location', col_names[cases_col], col_names[deaths_col]]]
            date = df[col_names[deaths_col]].name[7:17]
            date_list.append(date)

            df_cases = df[df[cases_col_name] != 0]
            df_cases['text'] = df_cases['country'] + '<br>' + df_cases['location'] + '<br>' + 'confirmed cases: ' + (df_cases[df_cases.columns[-2]].astype(int)).astype(str) + '<br>' +\
                'deaths: ' + (df_cases[df_cases.columns[-1]].astype(int))\
                .astype(str)
            cases_lat = df_cases['latitude']
            cases_lng = df_cases['longitude']

            df_deaths = df[df[deaths_col_name] !=0 ]
            deaths_lat = df_deaths['latitude']
            deaths_lng = df_deaths['longitude']
            df_deaths['text'] = df_deaths['country'] + '<br>' + df_deaths['location'] + '<br>' + 'confirmed cases: ' + (df_deaths[df_deaths.columns[-2]].astype(int)).astype(str) + '<br>' +\
                'deaths: ' + (df_deaths[df_deaths.columns[-1]].astype(int))\
                .astype(str)

            fig.add_trace(go.Scattergeo(name='Infections', lon=cases_lng, lat=cases_lat, visible=False, hovertemplate=df_cases['text'], text='Text', mode='markers',
                                        marker=dict(size=10, opacity=0.6, color='Blue', symbol='circle'),
                                        ))
            fig.add_trace(go.Scattergeo(name='Deaths', lon=deaths_lng, lat=deaths_lat, visible=False, hovertemplate=df_deaths['text'], text="Text", mode='markers',
                                        marker=dict(size=10, opacity=0.6, color='Red', symbol='circle')))

            steps = []
            for index, i in enumerate(range(0, len(fig.data), 2)):
                step = dict(
                        method="restyle",
                        args=["visible", [False] * len(fig.data)],
                        label=date_list[index],
                        )
                step["args"][1][i] = True
                step["args"][1][i+1] = True
                steps.append(step)

            sliders = [dict(
                        active=0,
                        currentvalue={"prefix": "Date: "},
                        pad={"t": 1},
                        steps=steps
                        )]

            fig.data[0].visible = True
            fig.data[1].visible = True

        fig.update_geos(
            showcountries=True, countrycolor="RebeccaPurple",
            projection_type='natural earth'
            )
        fig.update_layout(sliders=sliders,
                          title='Rise of the Novel Coronavirus<br>A Python Data Visualization by Advait Joshi', title_x=0.5,
                          legend_title='Key',
                          height=600)
        fig.show()
        go_offline.plot(fig, filename='./map_cov.html', validate=True, auto_open=False)


if __name__ == "__main__":
    grapher = Grapher()
    grapher.create_graph()
