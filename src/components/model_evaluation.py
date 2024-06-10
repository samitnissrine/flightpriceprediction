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

class ModelEvaluation:
    def __init__(self):
        logging.info("Evaluation started")

    def eval_metrics(self, actual, pred):
        mape = mean_absolute_percentage_error(actual, pred)
        logging.info("Evaluation metrics captured")
        return mape

    def initiate_model_evaluation(self, train_array, test_array):
        try:
            X_test, y_test = (test_array[:, :-1], test_array[:, -1])

            model_path = os.path.join("artifacts", "model.pkl")
            model = load_object(model_path)

            logging.info("Model has been loaded")

            tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

            print(tracking_url_type_store)

            with mlflow.start_run():
                prediction = model.predict(X_test)
                mape = self.eval_metrics(y_test, prediction)

                mlflow.log_metric("mape", mape)

                # Model registry does not work with file store
                if tracking_url_type_store != "file":
                    # Register the model
                    mlflow.sklearn.log_model(model, "model", registered_model_name="ml_model")
                else:
                    mlflow.sklearn.log_model(model, "model")

        except Exception as e:
            raise customexception(e, sys)
