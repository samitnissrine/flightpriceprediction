import os
import sys
import pandas as pd
from src.exception.exception import customexception
from src.logger.logging import logging
from src.utils.utils import *

class PredictPipeline:
    def __init__(self):
        print("Initializing the prediction pipeline...")

    def predict(self, features):
        try:
            model_path = os.path.join("artifacts", "model.pkl")
            model = load_object(model_path)

            processed_features = transforming_features(features)
            print(processed_features)
            pred = model.predict(processed_features)

            return pred

        except Exception as e:
            raise customexception(e, sys)

class CustomData:
    def __init__(self,
                 departure_time: str,
                 arrival_time: str,
                 duration: str,
                 date: str,
                 airline: str,
                 stops: str,
                 flight_class: str):

        
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.duration = duration
        self.date = date
        self.airline = airline
        self.stops = stops
        self.flight_class = flight_class

    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict = {
                'departure time': [self.departure_time],
                'arrival time': [self.arrival_time],
                'Duration': [self.duration],
                'Date': [self.date],
                'Airline': [self.airline],
                'stops': [self.stops],
                'Class': [self.flight_class]
            }
            df = pd.DataFrame(custom_data_input_dict)
            logging.info('Dataframe Gathered')
            return df
        except Exception as e:
            logging.info('Exception Occurred in prediction pipeline')
            raise customexception(e, sys)
