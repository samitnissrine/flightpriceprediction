from src.exception.exception import customexception
from src.logger.logging import logging
import pandas as pd 
import numpy as np 
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from src.utils.utils import save_object,evaluate_model
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.tree import DecisionTreeRegressor




@dataclass

class ModelTrainerConfig:
    pass

class ModelTrainer:
    def __init__(self):
        pass
        

    def initiate_ModelTrainer(self):
        try:
            pass
        except Exception as e:
            logging.info()
            raise customexception(e,sys)

