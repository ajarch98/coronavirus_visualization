"""Display a graph of the corona virus spread"""
import pandas as pd
import plotly.graph_objs as go


<<<<<<< HEAD
class Grapher():
    def __init__(self):
        self.confirmed_cases_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'
        self.deaths_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv'
        self.confirmed_data = pd.read_csv(self.confirmed_cases_url)
        self.deaths_data = pd.read_csv(self.deaths_url)
        assert len(self.confirmed_data.columns) == len(self.deaths_data.columns)
=======
URL = (f"https://docs.google.com/"
       f"spreadsheets/d/18X1VM1671d99V_yd-cnUI1j8oSG2ZgfU_q1HfOizErA/"
       f"export?format=csv&id")


class CoronaVirusGrapher():
    """
    Visualize cases of the corona virus
    """
    def __init__(self, url):
        self.data = pd.read_csv(url).fillna(0)

    def get_case_incidents(self):
        """Return a generator containing the confirmed cases as a tuple of
        confirmed_cases(dataframe), confirmed_date(dataframe) and date(string)

        """
        for confirmed_case_date, death_date in zip(
                self.data.filter(like='confirmedcases'),
                self.data.filter(like='deaths')):
            data_frame = self.data[
                ['latitude',
                 'longitude',
                 'country',
                 'location',
                 confirmed_case_date,
                 death_date,
                 ]
            ]

            df_cases = data_frame[data_frame[confirmed_case_date] != 0]
            df_cases['text'] = (df_cases['country']
                                + '<br>'
                                + df_cases['location']
                                + '<br>'
                                + 'confirmed cases: '
                                + (df_cases[df_cases.columns[-2]
                                            ].astype(int)).astype(str)
                                + '<br>'
                                + 'deaths: '
                                + (df_cases[df_cases.columns[-1]]
                                   .astype(int)).astype(str))

            df_deaths = data_frame[data_frame[death_date] != 0]
            df_deaths['text'] = (df_deaths['country']
                                 + '<br>'
                                 + df_deaths['location']
                                 + '<br>' + 'confirmed cases: '
                                 + (df_deaths[df_deaths.columns[-2]]
                                    .astype(int)).astype(str)
                                 + '<br>'
                                 + 'deaths: '
                                 + (df_deaths[df_deaths.columns[-1]]
                                    .astype(int)).astype(str))
            yield df_cases, df_deaths, death_date[-10:]
>>>>>>> d25dc7f06424ecf4e06aa508277ac70c45c5f7f5

    def create_graph(self):
        """Generate the graph based off the confirmed cases and deaths"""
        fig = go.Figure()
<<<<<<< HEAD
        col_names = self.confirmed_data.columns

        date_list = []
        for i in range(4, len(self.confirmed_data.columns)):

            confirmed_df = self.confirmed_data
            deaths_df = self.deaths_data

            date = confirmed_df[col_names[i]].name
            date_list.append(date)

            confirmed_df = confirmed_df[confirmed_df[date] != 0]
            confirmed_lat = confirmed_df['Lat']
            confirmed_lng = confirmed_df['Long']
            confirmed_df['text'] = 'Country/Region: ' + confirmed_df['Country/Region'] + '<br>' + 'Confirmed cases: ' +\
                confirmed_df[date].astype(str) + '<br>' +\
                'deaths: ' + deaths_df[date].astype(str)

            deaths_df = deaths_df[deaths_df[date] != 0]
            deaths_lat = deaths_df['Lat']
            deaths_lng = deaths_df['Long']
            deaths_df['text'] = 'Country/Region: ' + deaths_df['Country/Region'] + '<br>' + 'Confirmed cases: ' +\
                confirmed_df[date].astype(str) + '<br>' +\
                'Deaths: ' + deaths_df[date].astype(str)

            fig.add_trace(go.Scattergeo(name='Infections', lon=confirmed_lng, lat=confirmed_lat, visible=False, hovertemplate=confirmed_df['text'], text='Text', mode='markers',
                                        marker=dict(size=10, opacity=0.6, color='Blue', symbol='circle'),
                                        ))
            fig.add_trace(go.Scattergeo(name='Deaths', lon=deaths_lng, lat=deaths_lat, visible=False, hovertemplate=deaths_df['text'], text="Text", mode='markers',
                                        marker=dict(size=10, opacity=0.6, color='Red', symbol='circle')))
=======
        for df_cases, df_deaths, death_date in self.get_case_incidents():
            fig.add_trace(go.Scattergeo(name='Infections',
                                        lon=df_cases['longitude'],
                                        lat=df_cases['latitude'],
                                        visible=False,
                                        hovertemplate=df_cases['text'],
                                        text='Text',
                                        mode='markers',
                                        marker=dict(size=10, opacity=0.6,
                                                    color='Blue',
                                                    symbol='circle')))
            fig.add_trace(go.Scattergeo(name='Deaths',
                                        lon=df_deaths['longitude'],
                                        lat=df_deaths['latitude'],
                                        visible=False,
                                        hovertemplate=df_deaths['text'],
                                        text="Text",
                                        mode='markers',
                                        marker=dict(size=10, opacity=0.6,
                                                    color='Red',
                                                    symbol='circle')))
>>>>>>> d25dc7f06424ecf4e06aa508277ac70c45c5f7f5

            steps = []
            for _, i in enumerate(range(0, len(fig.data), 2)):
                step = dict(
                    method="restyle",
                    args=["visible", [False] * len(fig.data)],
                    label=death_date,
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
                          title=(f"Rise of the Novel Coronavirus<br>"
                                 f"A Python Data Visualization "
                                 f"by Advait Joshi"),
                          title_x=0.5,
                          legend_title='Key',
                          height=600)
<<<<<<< HEAD
        go_offline.plot(fig, filename='./map_cov.html', validate=True, auto_open=False)
=======
        return fig
>>>>>>> d25dc7f06424ecf4e06aa508277ac70c45c5f7f5


if __name__ == "__main__":
    import plotly.offline as pl

    CORONA_GRAPH = CoronaVirusGrapher(url=URL).create_graph()
    CORONA_GRAPH.show()
    pl.plot(CORONA_GRAPH,
            filename='./map_cov.html',
            validate=True, auto_open=False)
