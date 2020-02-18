"""Display a graph of the corona virus spread"""
import pandas as pd


URL = (f"https://docs.google.com/"
       f"spreadsheets/d/18X1VM1671d99V_yd-cnUI1j8oSG2ZgfU_q1HfOizErA/"
       f"export?format=csv&id")


class CoronaVirusGrapher():
    """
    Visualize cases of the corona virus
    """
    def __init__(self, url):
        self.url = url
        self.data = pd.read_csv(self.url).fillna(0)

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

    def create_graph(self):
        """Generate the graph based off the confirmed cases and deaths"""
        fig = Figure()
        for df_cases, df_deaths, date in self.get_case_incidents():
            fig.add_trace(Scattergeo(name='Infections',
                                     lon=df_cases['longitude'],
                                     lat=df_cases['latitude'],
                                     visible=False,
                                     hovertemplate=df_cases['text'],
                                     text='Text',
                                     mode='markers',
                                     marker=dict(size=10, opacity=0.6,
                                                 color='Blue',
                                                 symbol='circle')))
            fig.add_trace(Scattergeo(name='Deaths',
                                     lon=df_deaths['longitude'],
                                     lat=df_deaths['latitude'],
                                     visible=False,
                                     hovertemplate=df_deaths['text'],
                                     text="Text",
                                     mode='markers',
                                     marker=dict(size=10, opacity=0.6,
                                                 color='Red',
                                                 symbol='circle')))

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
        return fig


if __name__ == "__main__":
    import plotly.offline as pl

    CORONA_GRAPH = CoronaVirusGrapher(url=URL).create_graph()
    CORONA_GRAPH.show()
    pl.plot(CORONA_GRAPH,
            filename='./map_cov.html',
            validate=True, auto_open=False)
