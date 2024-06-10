import os
import sys
import mlflow
import mlflow.sklearn
import numpy as np
import pickle
from src.utils.utils import load_object
from urllib.parse import urlparse
from sklearn.metrics import mean_absolute_percentage_error
from src.logger.logging import logging
from src.exception.exception import customexception
from dataclasses import dataclass
from pathlib import Path
from src.utils.utils import save_object
from sklearn.linear_model import LinearRegression
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR

@dataclass 
class ModelTrainerConfig:
    trained_model_file_path = os.path.join('artifacts', 'model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def evaluate_model(self, X_train, y_train, X_test, y_test, models):
        model_performance = {}
        for model_name, model in models.items():
            model.fit(X_train, y_train)
            predictions = model.predict(X_test)
            mape = mean_absolute_percentage_error(y_test, predictions)
            model_performance[model_name] = mape
        return model_performance

    def initate_model_training(self, train_array, test_array):
        try:
            logging.info('Splitting Dependent and Independent variables from train and test data')

            # Assuming the last column is the target variable
            X_train = train_array[:, :-1]
            y_train = train_array[:, -1]
            X_test = test_array[:, :-1]
            y_test = test_array[:, -1]

            models = {
                'LinearRegression': LinearRegression(),
                'RandomForest': RandomForestRegressor(),
                'XGBoost': XGBRegressor(),
                'DecisionTree': DecisionTreeRegressor(),
                'SVR': SVR()
            }

            model_report = self.evaluate_model(X_train, y_train, X_test, y_test, models)
            print(model_report)
            print('\n====================================================================================\n')
            logging.info(f'Model Report : {model_report}')

            # To get the best model score from the dictionary
            best_model_score = min(sorted(model_report.values()))  # Lower MAPE is better
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
            
            best_model = models[best_model_name]

            print(f'Best Model Found, Model Name: {best_model_name}, MAPE: {best_model_score}')
            print('\n====================================================================================\n')
            logging.info(f'Best Model Found, Model Name: {best_model_name}, MAPE: {best_model_score}')

            save_object(
                 file_path=self.model_trainer_config.trained_model_file_path,
                 obj=best_model
            )

        except Exception as e:
            logging.info('Exception occurred during Model Training')
            raise customexception(e, sys)
