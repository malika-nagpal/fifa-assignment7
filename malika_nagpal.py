# -*- coding: utf-8 -*-
"""MALIKA_NAGPAL.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/17J8Xf8-EAKiPyXO77B9hz8FghxUCaRmB
"""

import pandas as pd
import numpy as np

data = {
    "Year": [1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 1974,
             1978, 1982, 1986, 1990, 1994, 1998, 2002, 2006, 2010, 2014,
             2018, 2022],
    "Winner": ["Uruguay", "Italy", "Italy", "Uruguay", "West Germany", "Brazil", "Brazil", "England", "Brazil", "West Germany",
               "Argentina", "Italy", "Argentina", "West Germany", "Brazil", "France", "Brazil", "Italy", "Spain", "Germany",
               "France", "Argentina"],
    "Runner-Up": ["Argentina", "Czechoslovakia", "Hungary", "Brazil", "Hungary", "Sweden", "Czechoslovakia", "West Germany", "Italy", "Netherlands",
                  "Netherlands", "West Germany", "West Germany", "Argentina", "Italy", "Brazil", "Germany", "France", "Netherlands", "Argentina",
                  "Croatia", "France"]
}

#  West Germany → Germany
for col in ["Winner", "Runner-Up"]:
    data[col] = ["Germany" if val == "West Germany" else val for val in data[col]]

df = pd.DataFrame(data)

# wins per country
win_counts = df["Winner"].value_counts().reset_index()
win_counts.columns = ["Country", "Wins"]

# Save CSV for use in Dash later
df.to_csv("world_cup_finals.csv", index=False)
win_counts.to_csv("world_cup_wins.csv", index=False)

# Display the datasets
print("=== Finals Dataset ===")
print(df.head())

print("\n=== Win Count Dataset ===")
print(win_counts.head())

# app.py
# link to render dashboard https://fifa-dashapp.onrender.com

import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px


df_finals = pd.read_csv("world_cup_finals.csv")
df_wins= pd.read_csv("world_cup_wins.csv")


app = Dash()
server=app.server
app.title = "FIFA World Cup Dashboard"


app.layout = html.Div([
    html.H1("FIFA World Cup Winners Dashboard", style={'textAlign': 'center'}),

    html.H2("Choropleth Map of World Cup Winners", style={'marginTop': '20px'}),
    dcc.Graph(id='choropleth'),

    html.H2("Select a Country to See Number of Wins"),
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': c, 'value': c} for c in wins_df["Country"].unique()],
        placeholder="Select a country",
        style={'width': '50%'}
    ),
    html.Div(id='country-wins', style={'marginTop': '10px'}),

    html.H2("Select a Year"),
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': y, 'value': y} for y in finals_df["Year"]],
        placeholder="Select a year",
        style={'width': '50%'}
    ),
    html.Div(id='final-result', style={'marginTop': '10px'})
])


@app.callback(
    Output('choropleth', 'figure'),
    Input('choropleth', 'id')
)
def map_update(_):
    fig = px.choropleth(
        df_wins,
        locations="Country",
        locationmode="country names",
        color="Wins",
        color_continuous_scale="Blues",
        title="World Cup Wins by Country"
    )
    fig.update_layout(geo=dict(showframe=False))
    return fig


@app.callback(
    Output('country-wins', 'children'),
    Input('country-dropdown', 'value')
)
def display_country_wins(selected_country):
    if not selected_country:
        return ""
    wins = df_wins.loc[wins_df["Country"] == selected_country, "Wins"].values[0]
    return html.H4(f"{selected_country} has won the World Cup {wins} times.")

@app.callback(
    Output('final-result', 'children'),
    Input('year-dropdown', 'value')
)
def display_final_result(selected_year):
    if not selected_year:
        return ""
    row = df_finals[df_finals["Year"] == selected_year].iloc[0]
    return html.H4(f"In {selected_year}, {row['Winner']} won against {row['Runner-Up']}.")


if __name__ == '__main__':
    app.run(debug=True)

code = '''


import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# Load datasets
finals_df = pd.read_csv("world_cup_finals.csv")
wins_df = pd.read_csv("world_cup_wins.csv")

app = dash.Dash(__name__)
app.title = "FIFA World Cup Dashboard"

app.layout = html.Div([
    html.H1("FIFA World Cup Winners Dashboard", style={'textAlign': 'center'}),
    html.H2("Choropleth Map of World Cup Winners"),
    dcc.Graph(id='choropleth'),
    html.H2("Select a Country to See Number of Wins"),
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': c, 'value': c} for c in wins_df["Country"].unique()],
        placeholder="Select a country",
        style={'width': '50%'}
    ),
    html.Div(id='country-wins'),
    html.H2(" Select a Year to See Final Result"),
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': y, 'value': y} for y in finals_df["Year"]],
        placeholder="Select a year",
        style={'width': '50%'}
    ),
    html.Div(id='final-result')
])

@app.callback(
    Output('choropleth', 'figure'),
    Input('choropleth', 'id')
)
def update_map(_):
    fig = px.choropleth(
        wins_df,
        locations="Country",
        locationmode="country names",
        color="Wins",
        color_continuous_scale="Blues",
        title="World Cup Wins by Country"
    )
    fig.update_layout(geo=dict(showframe=False))
    return fig

@app.callback(
    Output('country-wins', 'children'),
    Input('country-dropdown', 'value')
)
def display_country_wins(selected_country):
    if not selected_country:
        return ""
    wins = wins_df.loc[wins_df["Country"] == selected_country, "Wins"].values[0]
    return html.H4(f"{selected_country} has won the World Cup {wins} times.")

@app.callback(
    Output('final-result', 'children'),
    Input('year-dropdown', 'value')
)
def display_final_result(selected_year):
    if not selected_year:
        return ""
    row = finals_df[finals_df["Year"] == selected_year].iloc[0]
    return html.H4(f"In {selected_year}, {row['Winner']} won against {row['Runner-Up']}.")

if __name__ == '__main__':
    app.run_server(debug=True)
'''

with open("app.py", "w") as f:
    f.write(code)

print(" app.py has been created.")

requirements = '''
dash
pandas
plotly
gunicorn
'''

with open("requirements.txt", "w") as f:
    f.write(requirements.strip())

print("requirements.txt has been created.")

with open("Procfile", "w") as f:
    f.write("web: gunicorn app:app")

print("Procfile has been created.")
