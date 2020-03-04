# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from datetime import datetime as dt
import dash_html_components as html
from dash.dependencies import Input, Output
from joblib import load
import pandas as pd

# Imports from this application
from app import app

#Load pipeline
pipeline = load('assets/rf2.joblib')
print('Pipline2 loaded')

# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column = dbc.Col(
    [
        dcc.Markdown(
            """
            ## 📈 Predictions

            We want to predict how much money we will take home in tips today.
            *Try adjusting the following __inputs__ to generate a new prediction.*

            **Inputs:** 
            * Date: the day you want to work 
            * Hours: how long will you work
            * Demand: how busy the store is 
            * Precipitation: expected rain/snow (inches)
            
            """
        )
    ]

)
column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ### Predictions

            We want to predict how much money we will take home in tips today.

            """
        ),
        html.H2('Day Earnings', className='mb-2'), 
        html.Img(src='assets/friends.jpg', className='img-fluid'),
        html.Div(id='prediction-content', className='lead'),
        
    ],
    md=4,
)

column2 = dbc.Col(
    [
        dcc.Markdown("""
        ### Feature Selection
        
        **DATE**""", className='mt-4'),
        dcc.DatePickerSingle(
            id='date-picker-single',
            min_date_allowed=dt(2017, 6, 26),
            max_date_allowed=dt(2019, 6, 30)
            
        ),
        dcc.Markdown("""**SHIFT HOURS**""", className='mt-4'),
        dcc.Slider(
            id='Hours',
            min=2,
            max=9,
            step=.5,
            marks={i: '{}'.format(i) for i in range(14)},
            value=5.5,),
        dcc.Markdown("""**DEMAND**""", className='mt-4'),
        dcc.RadioItems(
            id='Demand',
            options=[
                {'label': 'Slow', 'value': 1},
                {'label': 'Normal', 'value': 2},
                {'label': 'Busy', 'value': 3}
            ],
            value=1),
        dcc.Markdown("""**PRECIPITATION**""", className='mt-4'),
        dcc.Slider(
        id='PRCP',
        min=0,
        max=4,
        step=0.1,
        value=0),
        dcc.Markdown("""""", id='out2') 
        
        
    ]
)

layout = dbc.Row(column), dbc.Row([column1, column2])
#precipitation text
@app.callback(
    Output(component_id='out2', component_property='children'),
    [Input(component_id='PRCP', component_property='value')]
)
def update_output_div(input_value):
    return '{} inches'.format(input_value) 


@app.callback(
    Output('prediction-content', 'children'),
    [Input('Hours', 'value'),Input('PRCP', 'value'),
    Input('Demand', 'value'),Input('date-picker-single', 'date')],
)
def predict(Hours,PRCP,Demand,date):
    #string to datetime
    date = dt.strptime(date,'%Y-%m-%d')
    #get tuple of all attributes
    tt= dt.timetuple(date)
    a =[]
    for it in tt:
        a+=[it]

    #extracting y,m,d,&day of week(0-6)  
    Year = a[0]
    Month = a[1]
    Day = a[2] 
    Dow = a[6] 

    df = pd.DataFrame(
        columns=['Day of Week','Hours','Year','Month','Day','PRCP','Demand'], 
        data=[[Dow, Hours, Year, Month, Day, PRCP, Demand]]
    )
    y_pred = pipeline.predict(df)[0]
    return f'Estimated Tips: ${y_pred:.2f}'


        
  