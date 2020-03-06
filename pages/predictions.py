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
pipeline = load('assets/lg.joblib')
print('Pipline3 loaded')

# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column = dbc.Col(
    [
        dcc.Markdown(
            """
            # 📈 Predictions

            Let's predict how much money you could take home 
            in tips. *Try adjusting the following 
            __inputs__ to generate a new prediction.*

            **Inputs:** 
            * Date: the day you want to work 
            * Hours: how long will you work
            * Demand: how busy is your store 
            * Precipitation: expected rain/snow in inches
            
            """
        )
    ]

)
column1 = dbc.Col(
    [
        dcc.Markdown(
            """
            ### Predicted Earnings 
            &nbsp; """
        ),
     
        #html.Img(src='assets/friends.jpg', className='img-fluid'),
        html.Div(id='prediction-image', className='mb-2'),
        html.Div(id='prediction-content', className='lead',
        style={'textAlign':'center', 'fontSize':25}),
        
    ],
    md=4,
    
)

column2 = dbc.Col(
    [
        dcc.Markdown("""
        ### Feature Selection  
        &nbsp; """),

        dcc.Markdown("""#### 📅**DATE**  
        """, className='mb-2'),
        dcc.DatePickerSingle(
            id='date-picker-single',
            date=('2017-07-01'),
            min_date_allowed=dt(2017, 7,1),
            max_date_allowed=dt(2022, 6, 30)
            
        ),
        html.Div(style={'padding': 10}),
        dcc.Markdown("""#### 👔**SHIFT HOURS**""", className='mb-2'),
        dcc.Slider(
            id='Hours',
            min=2,
            max=10,
            step=.5,
            marks={i: '{}'.format(i) for i in range(12)},
            value=4.5,),
        
        html.Div(style={'padding': 10}),
        dcc.Markdown("""#### 🍕**DEMAND**""", className='mb-2'),
        dcc.RadioItems(
            id='Demand',
            options=[
                {'label': 'Slow', 'value': 'Slow'},
                {'label': 'Normal', 'value': 'Normal'},
                {'label': 'Busy', 'value': 'Busy'}
            ],
            value='Normal'),
        
        #html.Div([html.P([html.Br()])]),
        html.Div(style={'padding': 10}),
        dcc.Markdown("""#### 🌧️**PRECIPITATION**""", className='mb-2'),
        dcc.Slider(
        id='PRCP',
        min=0,
        max=3,
        step=0.1,
        value=0.0),
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
    return '{} inch(es)'.format(input_value) 

#tip prediction
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

#image selection
@app.callback(
    Output('prediction-image','children'),
    [Input("Demand", 'value')]
)
def select_image(Demand):
    if Demand == 'Slow':
        return html.Img(src='assets/group.jpg', className='img-fluid', 
        style = {'height': '300px', 'display': 'block', 
        'margin-left': 'auto', 'margin-right': 'auto'})
    elif Demand == 'Busy':
        return html.Img(src='assets/busy.jpg', className='img-fluid', 
        style = {'height': '300px', 'display': 'block', 
        'margin-left': 'auto', 'margin-right': 'auto'})
    else:
        return html.Img(src='assets/friend.jpg', className='img-fluid', 
        style = {'height': '300px', 'display': 'block', 
        'margin-left': 'auto', 'margin-right': 'auto'})
    


        
  