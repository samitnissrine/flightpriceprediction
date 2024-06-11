import os
import sys
import pickle
import numpy as np
import pandas as pd
from src.logger.logging import logging
from src.exception.exception import customexception
import re
from sklearn.metrics import r2_score, mean_absolute_error,mean_squared_error
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import OneHotEncoder
from datetime import date


def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise customexception(e, sys)
    
def evaluate_model(X_train,y_train,X_test,y_test,models):
    try:
        report = {}
        for i in range(len(models)):
            model = list(models.values())[i]
            # Train model
            model.fit(X_train,y_train)

            

            # Predict Testing data
            y_test_pred =model.predict(X_test)

            # Get R2 scores for train and test data
            #train_model_score = r2_score(ytrain,y_train_pred)
            test_model_score = r2_score(y_test,y_test_pred)

            report[list(models.keys())[i]] =  test_model_score

        return report

    except Exception as e:
        logging.info('Exception occured during model training')
        raise customexception(e,sys)
    
def load_object(file_path):
    try:
        with open(file_path,'rb') as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        logging.info('Exception Occured in load_object function utils')
        raise customexception(e,sys)

    
###########functions for data transformation


def extract_numeric_value(value_string):
    # Use regular expression to find digits and commas
    matches = re.findall(r'\d+', value_string.replace(',', ''))
    # Join the matches into a single string and convert to float
    numeric_value = float(''.join(matches))
    return numeric_value

# Define the function to convert AED to USD
def convert_aed_to_usd(amount_in_aed, exchange_rate=0.27):
    """
    Convert an amount from AED (United Arab Emirates Dirham) to USD (United States Dollar).

    Args:
    amount_in_aed (float): Amount in AED.
    exchange_rate (float, optional): Exchange rate from AED to USD. Default is 0.27.

    Returns:
    float: Amount converted to USD.
    """
    amount_in_usd = amount_in_aed * exchange_rate
    return amount_in_usd
'''
def convert_price(df):
    for index, row in df.iterrows():
        # Access individual elements using column names
        row['Price'] = convert_aed_to_usd(row['Price'])'''

def clean_arrival_time(arrival_time):
    if '+' in arrival_time:
        return arrival_time.split('+')[0]
    else:
        return arrival_time


def convert_to_minutes(duration):
    parts = duration.split(' ')
    
    hours = 0
    minutes = 0
    
    if 'h' in parts[0]:
        hours = int(parts[0].replace('h', ''))
    
    if 'm' in parts[-1]:
        minutes = int(parts[-1].replace('m', ''))
    
    return hours * 60 + minutes



def convert_stops_to_numeric(df, column_name):
    mapping_dict = {value: index for index, value in enumerate(df[column_name].unique())}

    df[column_name] = df[column_name].replace(mapping_dict)

    return df



def categorize_time(hour):
    # Split the string using ":" as the delimiter
    hours, minutes = map(int, hour.split(':'))
    # Extract the hour part as an integer
    hour_as_int = int(hours)
    if 4 <= hour_as_int < 7:
        return "Early Morning"
    elif 7 <= hour_as_int < 12:
        return "Morning"
    elif 12 <= hour_as_int < 17:
        return "Afternoon"
    elif 17 <= hour_as_int < 20:
        return "Evening"
    elif 20 <= hour_as_int < 24:
        return "Night"
    else:
        return "Late Night"


def categorize_time_alternative(time_str):
    """
    Categorizes a time string into one of several time periods using different intervals.
    
    Args:
    time_str (str): Time in the format 'HH:MM'.
    
    Returns:
    str: Time category.
    """
    hour = int(time_str.split(':')[0])
    
    if 0 <= hour < 6:
        return 'Late Night'
    elif 6 <= hour < 12:
        return 'Morning'
    elif 12 <= hour < 18:
        return 'Afternoon'
    elif 18 <= hour < 21:
        return 'Evening'
    else:
        return 'Night'



#the whole process using those functions for data transforming
def process_data(data):
    data['Price'] = data['Price'].apply(extract_numeric_value)
    data['Price'] = data['Price'].astype(float)
    data['Price'] = data['Price'].apply(convert_aed_to_usd)
    data['Duration'] = data['Duration'].apply(convert_to_minutes)
    data = convert_stops_to_numeric(data, 'stops')
    data['arrival time'] = data['arrival time'].apply(clean_arrival_time)
    data['arrival time'] = data['arrival time'].apply(categorize_time)
    data['departure time'] = data['departure time'].apply(categorize_time)
    data['Date'] = data['Date'].str.strip()
    data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')
    data['Price'] = data['Price'].astype(float)
    # Calculate the days left
    #search_date = pd.to_datetime('2024-05-28')
    data['search_date'] = pd.to_datetime(data['search_date'], format='%Y-%m-%d')

    data['Days Left'] = (data['Date'] - data['search_date']).dt.days
    #data['Day of Week'] = data['Date'].dt.dayofweek
    le = LabelEncoder()
    ordinal_variables = ['Airline', 'class', 'departure time', 'arrival time']
    data[ordinal_variables] = data[ordinal_variables].apply(lambda col: le.fit_transform(col))


    dropsource = 'Source'
    dropdest = 'Destination'
    data = data.drop(columns=dropsource,axis=1)
    data = data.drop(columns=dropdest,axis=1)

    data['Price'] = np.log(data['Price'])
    data.drop(columns="Date", inplace=True)
    data.drop(columns="search_date", inplace=True)
    return data





















def transforming_features(data):
    label_encoder = LabelEncoder()
    data['Duration'] = data['Duration'].apply(convert_to_minutes)
    data = convert_stops_to_numeric(data, 'stops')
    data['arrival time'] = data['arrival time'].apply(clean_arrival_time)
    data['arrival time'] = data['arrival time'].apply(categorize_time)
    data['departure time'] = data['departure time'].apply(categorize_time)
    data['departure time'] = label_encoder.fit_transform(data['departure time'])
    data['arrival time'] = label_encoder.fit_transform(data['arrival time'])
    #data['arrival time'] = data['arrival time'].apply(categorize_time_alternative)
    #data['departure time'] = data['departure time'].apply(categorize_time_alternative)
    data['Date'] = data['Date'].str.strip()
    data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')
    # Calculate the days left
    current_date = date.today()
    data['search_date'] = current_date
    data['search_date'] = pd.to_datetime(data['search_date'], format='%Y-%m-%d')

    data['Days Left'] = (data['Date'] - data['search_date']).dt.days
      
    data.drop(columns="Date", inplace=True)
    data.drop(columns="search_date", inplace=True)

    return data

