# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Imports from this application
from app import app

# 1 column layout
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## Insights

            ##### Permutation Importance   
            A few different inputs went into this linear model: Month, Day, Year, Day of Week, Hours, Demand, and Precipitation. 
            With so many features, it can become difficult to understand how the model concludes the predictions. Looking at the 
            permutation feature importances, we can get a better grasp on which features carry the most weight in predicting the daily tip value. 


            The specific day of the week and amount of rain or snowfall were important but held the least weight in determining the value of tips. 
            On the other hand, the number of hours worked in a day and the business demand had the greatest impact on tips earned. 
            This make sense once you think about the flow of a business; you would expect greater sales and earnings the longer you are open 
            and how busy your store is.


            """
        ),
        html.Img(src='assets/importances.PNG', className='img-fluid', style = {'display': 'block', 
        'margin-left': 'auto', 'margin-right': 'auto'}, height="600", width="300"),
        dcc.Markdown(
            """
            ##### Partial Dependency  
            Making this point clearer, an interactive partial dependency plot between hours and demand shows that as the values of both 
            increases, so does the estimated take home tip value. As mentioned above, the amount of rainfall did seem to be positively correlated 
            with tips as well, but at a smaller rate.

            """
        ),
        html.Img(src='assets/demandhours.png', className='img-fluid', height="1000", width="550"),
        html.Img(src='assets/demandprcp.png', className='img-fluid', height="1000", width="550"),
        dcc.Markdown(
            """
            ---
            
            ### Fun Fact:  
            Domino's drivers in Madrid, Spain will deliver you pizza on this!
            """),

        html.Img(src='assets/spain.jpg', className='img-fluid', height="200", width="400")


    ],
)


layout = dbc.Row([column1])