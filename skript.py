from dash import Dash, html, dcc, Input, Output, dash_table, State
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output, State
import plotly.express as px
import pandas as pd

dat = pd.read_excel("https://github.com/datenlabor01/geodaten/raw/main/testdata_processed.xlsx")
#app = JupyterDash(__name__, external_stylesheets=[dbc.themes.LUX])
app = Dash(external_stylesheets = [dbc.themes.ZEPHYR])

figMap = px.scatter_mapbox(dat[(dat.Lat!= "")& (dat.Lat != "not found")], lat="Lat", lon="Lon",
                        hover_name="Ort", hover_data={"Name": True, "Besetzt seit": True, "Aktuell besetzt bis": True, "Maximale Dotierung": True, "Lat": False, "Lon": False},
                        zoom = 2)
figMap.update_layout(mapbox_style="carto-positron")
figMap.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

country_dropdown = dcc.Dropdown(id = "country", options=sorted(dat["Land "].unique()),
                             value='All', style={"textAlign": "center"}, clearable=False, multi=True, placeholder='Alle Länder')

time_dropdown = dcc.Dropdown(id = "time", options=sorted(dat["Aktuell besetzt bis"].unique()),
                             value='All', style={"textAlign": "center"}, clearable=False, multi=True, placeholder='Alle Zeiten')

dotation_dropdown = dcc.Dropdown(id = "dotation", options=sorted(dat["Maximale Dotierung"].unique()),
                             value='All', style={"textAlign": "center"}, clearable=False, multi=True, placeholder='Alle Dotierungen')


app.layout = html.Div([
      dbc.Row([
         html.H1(children='Prototyp Außendarstellung', style={'textAlign': 'center'}),
         html.P(children = "Das ist ein Prototyp.",
         style={'textAlign': 'center'}),
      ]),

      dbc.Row([
          dcc.Graph(figure = figMap, style={'textAlign': 'center'})
      ]),

      dbc.Row([html.Br(),
        dbc.Col([country_dropdown]),
        dbc.Col([time_dropdown]),
        dbc.Col([dotation_dropdown]),
    ], style={'textAlign': 'center'}),

      #Data Table:
      dbc.Row([
         my_table := dash_table.DataTable(
         dat.to_dict('records'), [{"name": i, "id": i} for i in dat.columns[:-5]],
         filter_action="native", sort_action="native", page_size= 25,
         style_cell={'textAlign': 'left', "whiteSpace": "normal", "height": "auto"},
         style_header={'backgroundColor': 'rgb(11, 148, 153)', 'color': 'black', 'fontWeight': 'bold'},
             style_data_conditional=[{
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(235, 240, 240)',
        }], export_format= "xlsx"),
         ]),
])

#Callback for dropdown:
@app.callback(
    [Output('time', 'options'), Output('dotation', 'options')],
    [Input("country", 'value')]
)

def update_dropdown(country):
  if (country == "All") | (country == []):
      dat_fil = dat
  else:
      dat_fil = dat[dat["Land "].isin(country)]
  return sorted(dat_fil["Aktuell besetzt bis"].unique()), sorted(dat["Maximale Dotierung"].unique())

@app.callback(
    Output('country', 'options'),
    [Input("time", 'value'), Input("dotation", 'value')]
)

def update_dropdown2(time, dotation):
  if (time == "All") | (time == []):
      dat_fil = dat
  else:
      dat_fil = dat[dat["Aktuell besetzt bis"].isin(time)]
  if (dotation == "All") | (dotation == []):
      dat_fil = dat_fil
  else:
      dat_fil = dat_fil[dat_fil["Maximale Dotierung"].isin(dotation)]

  return sorted(dat_fil["Land "].unique())

@app.callback(
    Output(my_table, "data"),
    [Input("country", 'value'), Input("time", 'value'), Input("dotation", 'value')]
)

def update_table(country, time, dotation):

   if (country == "All") | (country == []):
      dat_fil = dat
   else:
      dat_fil = dat[dat["Land "].isin(country)]
   if (time == "All") | (time == []):
      dat_fil = dat_fil
   else:
      dat_fil = dat_fil[dat_fil["Aktuell besetzt bis"].isin(time)]
   if (dotation == "All") | (dotation == []):
      dat_fil = dat_fil
   else:
      dat_fil = dat_fil[dat_fil["Maximale Dotierung"].isin(dotation)]

   return dat_fil.to_dict("records")

if __name__ == '__main__':
    app.run_server(debug=True)
