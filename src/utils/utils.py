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

def convert_aed_to_usd(amount_in_aed):
    amount_in_aed = extract_numeric_value(amount_in_aed)
    amount_in_usd = amount_in_aed * 0.27
    return amount_in_usd

def convert_price(df):
    for index, row in df.iterrows():
        # Access individual elements using column names
        row['Price'] = convert_aed_to_usd(row['Price'])

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






#the whole process using those functions for data transforming
def process_data(data):
    convert_price(data)
    data['Duration'] = data['Duration'].apply(convert_to_minutes)
    data = convert_stops_to_numeric(data, 'stops')
    data['arrival time'] = data['arrival time'].apply(clean_arrival_time)
    data['arrival time'] = data['arrival time'].apply(categorize_time)
    data['depature time'] = data['depature time'].apply(categorize_time)
    data['Date'] = data['Date'].str.strip()
    data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')
    data['Price'] = data['Price'].astype(float)

    # Calculate the days left
    search_date = pd.to_datetime('2024-05-28')
    data['Days Left'] = (data['Date'] - search_date).dt.days
    data['Day of Week'] = data['Date'].dt.dayofweek

    le = LabelEncoder()
    ordinal_variables = ['Airline', 'class', 'depature time', 'arrival time']
    data[ordinal_variables] = data[ordinal_variables].apply(lambda col: le.fit_transform(col))
    data = pd.get_dummies(data, columns=['Source', 'Destination'])

    data['Price'] = np.log(data['Price'])
    data['Duration'] = np.log(data['Duration'])
    data.drop(columns="Date", inplace=True)
    bool_columns = ['Source_CMN', 'Source_IST', 'Source_LAX', 'Source_NRT', 'Source_PAR', 
                'Destination_CMN', 'Destination_IST', 'Destination_LAX', 'Destination_NRT', 'Destination_PAR']

    data[bool_columns] = data[bool_columns].astype(int)

    return data
