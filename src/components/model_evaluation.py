import os
import sys
import mlflow
import mlflow.sklearn
import numpy as np
import pickle
from src.utils.utils import load_object
from urllib.parse import urlparse
from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score
from src.logger.logging import logging
from src.exception. exception import customexception

class ModelEvaluation:
    def __init__(self):
        pass
    

    def eval_metrics(self,actual,pred):
        pass

    def initiate_model_evaluation(self,train_array,test_array):
        try:
            pass

        except Exception as e:
            raise customexception(e,sys)