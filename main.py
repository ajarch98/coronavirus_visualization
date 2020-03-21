import plotly.offline as go_offline
import plotly.graph_objects as go
import pandas as pd


class Grapher():
    def __init__(self):
        self.confirmed_cases_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'
        self.deaths_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv'
        self.confirmed_data = pd.read_csv(self.confirmed_cases_url)
        self.deaths_data = pd.read_csv(self.deaths_url)
        assert len(self.confirmed_data.columns) == len(self.deaths_data.columns)

    def create_graph(self):
        fig = go.Figure()
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
        go_offline.plot(fig, filename='./map_cov.html', validate=True, auto_open=False)


if __name__ == "__main__":
    grapher = Grapher()
    grapher.create_graph()
