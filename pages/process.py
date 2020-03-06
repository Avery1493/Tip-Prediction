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
            ## Process

            """),
        dcc.Markdown(
            """
            ##### Data Collection
            * Personal daily tip earnings recorded by one driver from June 
            2017-June2019  
            * Extracted daily weather data from NOAA 

            Aside from getting this application deployed, collecting the data for this project was probably my favorite part. 
            I have worked as a delivery driver for Domino’s Pizza for over 2.5 years. It started as a part-time job during college. 
            Delivering became my full-time job for about a year after school. However, now it’s my fun second job! 


            At the first franchise store I worked at [Middle Tennessee Pizza Inc.](http://www.midtnpizza.com/), I was paid hourly 
            the federal minimum wage ($7.25). In addition, I earned cash tips every night I worked. As a finance major and number nerd, 
            I just automatically kept track of this information. I would save the information in a note on my phone, then at the 
            end of every work week, I’d enter it into a excel sheet. For budgeting purposes and to calculate my total hourly wage, 
            I kept track of how much I earned in tips, how much I was reimbursed for mileage, how many miles I drove, and how many hours 
            I spent on the road. Because I’m always recommending people to work as a delivery driver anyway, I decided I could use all this 
            information to show how much a typical person could make if they decided to work at Dominos.


            The data for this study was taken from the period spanning June of 2017 to June of 2019 for a total of 423 observations (rows). 
            I moved to a different city after that time and therefore did not include any information post relocating. The average daily sales, 
            delivery area range, demographic of the customers, and my hours of availability at the second franchise I worked for were 
            significantly different. To be consistent, I excluded that data. To help my predictive model, I 
            [extracted weather data](https://towardsdatascience.com/getting-weather-data-in-3-easy-steps-8dc10cc5c859) form 
            [NOAA](https://www.noaa.gov/) (National Oceanic and Atmospheric Administration).

            """),
        html.Img(src='assets/note.png', className='img-fluid', height="500", width="250"),
        html.Img(src='assets/tips.PNG', className='img-fluid', height="400", width="850"),
        dcc.Markdown(
            """
            ##### Feature Selection  
            * Extracted month, day, year, and day of week from the date  
            * Generated categorical feature for daily business demand  
            * Imported daily precipitation amount measured in inches

            While my initial idea was great, I got a little bit discouraged looking at my limited feature options (columns). I was especially 
            worried about potential data leakage, because I wanted to predict total daily tips, and most of my data was collected after the fact. 
            Therefore, I immediately threw out the columns “Take Home” and “Mileage”.  Later, I threw out “Week”. I used the “Miles” column to 
            generate a new feature before ultimately throwing that one out as well. 


            That left me with 3 usable columns: “Day”, “Date”, “Hours”, and my target column, “Tips”.  I used the 
            [to_datetime](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_datetime.html) function in Pandas to extract the 
            four elements from “Date”: Year, Month, Day, and the Day of the Week, which replaced my “Day” column. 


            Next, I used the “Miles” column generate a new feature. I wanted to essentially capture the daily business demand at the store. 
            Intuitively, I recognized that if the store was busy, we would have more deliveries, and therefore I would have put more miles on 
            my car that day. I calculated the number of miles I drove per hour by dividing “Miles” by “Hours”.  From the box plot you can see the 
            average miles per hour driven each work day. I classified the middle 50% (IQR) as ‘Normal’. Anything above or below that I 
            called a ‘Busy’ or ‘Slow’ day for pizza!


            """),
            html.Img(src='assets/boxplot.png', className='img-fluid',style = {'display': 'block', 
        'margin-left': 'auto', 'margin-right': 'auto'}, height="350", width="500"),
        dcc.Markdown(
            """
            Lastly, as mentioned before, I used NOAA to get information about the weather. Data supplied from the TN Murfreesboro Stones River 
            NB (Station ID:  GHCND:USC00406374) gave me the daily precipitation total.  I merged the two datasets on the date.


            Upon reflection, other features I wish I had, but did not think to collect (or couldn’t collect) were prior year to date sales, 
            total drivers scheduled, if there was a football game that day. Other features, I could have but did not explore were adding the 
            seasons (Spring, Summer, Fall, Winter). Or similarly, since my location was right off a college campus (and the university students 
            contributed much to our sales), adding the school semester (Fall, Spring, Summer, Break).  


            The final features I had for my model included, ('Day of Week’, 'Hours', 'Year', 'Month', 'Day', 'PRCP', 'Demand').
            
            
            ```
            cutoff = '2018-07-01 00:00:00'  
            train = df[df['Date'] < cutoff]  
            test = df[df['Date'] >= cutoff]  
            target = 'Tips'  
            features = ['Day of Week','Hours', 'Year', 'Month', 'Day', 'PRCP', 'Demand']
            ```
            ---

            """),
        dcc.Markdown(
            """
            ##### Model Generation  
            * Baseline model - Mean Absolute Error: $18.82  
            * Linear Regression model - Mean Absolute Error: $11.78  
            * Random Forest model - Mean Absolute Error: $7.75

            To be able to make a predictive model, I used a date split on my dataset. Any information that was collected from the end of June 2018 
            and prior (middle of the two years of data), I labeled train. The information from the train dataset is what I used to create my models. 
            The remaining data was put in the test dataset. The test set will be used afterwards to test how accurate my model predicts total tips on 
            unseen data.


            I started with a baseline model. If I were to just guess how much I took home in tips each night with the average, how correct would I be? 
            The mean for the total tips in my data set was $58.23. I used the metric mean absolute error (MAE) to measure the average error from my model’s 
            predicted values and the true values.  The baseline model’s MAE was $18.82. This means, if I were to guess that every night, I would make $58.23, 
            I would be off on average by almost $20. This is a lot of error. 


            Next, I made a Linear Regression model. Using the SkLearn library, I created a pipeline to transform my data and run a linear regression. I used 
            [Ordinal Encoder](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OrdinalEncoder.html) to turn my categorical column, 
            ‘Demand’, into a numerical value. The [Simple Imputer](https://scikit-learn.org/stable/modules/generated/sklearn.impute.SimpleImputer.html) replaced 
            all my missing values with the median value. The mean absolute error for this model was $11.78. Now that’s a lot better than just guessing.


            The last model I created was a [Random Forest model](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html). 
            Again, the regressor was wrapped in a pipeline to encode categorical values and impute missing values with the median. In addition, I used 
            [Randomized Search CV](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.RandomizedSearchCV.html) to find the optimal hyper 
            parameters  for the final pipeline. The random forest model using the tuned hyper parameters produced a mean absolute error (MAE) of $7.75. 
            I thought that was fantastic.
            

            """),
        dcc.Markdown(
            """
            ##### Model Selection  
            * The data truly has a linear pattern. The Linear Regression more accurately predicted the actual tip totals on the test set than the random forest model.

            After training my models, I wanted to know how they would perform on new data. I fed the test dataset that I left out in the beginning, through my 
            linear and random forest models. The MAE for the linear regression on the test set was $13.47 (fairly close to the train MEA of 11.78). The MAE for 
            the random forest model on the test set was $18.82 (just as bad as our original baseline). This means that the linear model would be the best to use 
            for this predictive model because it produces a lower error or more accurate prediction.


            """),
        dcc.Markdown(
            """
            ##### Conclusion 
            For generating the predictions in this app, I used a Linear Regression model (retrained on the entire dataset) with a MAE of $12.61.


            I was really surprised the random forest model was outperformed by a simple regression (even after randomized search and cross validation). 
            More than often it’s the other way around. The takeaway from this project is that linear regressions work really well when data has a linear 
            shape and a tree or random forest would have worked better if my dataset was non-linear.
            
            
            """
        ),
        

    ],
)

layout = dbc.Row([column1])