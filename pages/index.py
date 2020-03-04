# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

# Imports from this application
from app import app

# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## 🤑 How much could you make?

            Imagine you work as a delivey driver for Domino's Pizza. 
            You receive a direct wage, but most of your earnings are received in tips. 

            Does your income depend solely on your excellent service and generosity of your customers? 
            Or can we optimize your earnings by planning out your work schedule? 

            You can use this interactive app to predict your daily take home tips. 

            """
            

        ),
        
        dcc.Link(dbc.Button("Let's try!", color='primary'), href='/predictions')
    ],
    md=4,
)

gapminder = px.data.gapminder()
fig = px.scatter(gapminder.query("year==2007"), x="gdpPercap", y="lifeExp", size="pop", color="continent",
           hover_name="country", log_x=True, size_max=60)

column2 = dbc.Col(
    [
        #dcc.Graph(figure=fig),
        html.Img(src='assets/domino.jpg', className='img-fluid'),
    ]
)

layout = dbc.Row([column1, column2])