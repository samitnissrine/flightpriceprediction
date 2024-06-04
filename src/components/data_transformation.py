import pandas as pd
import numpy as np
from src.logger.logging import logging
from src.exception.exception import customexception
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder,StandardScaler
from src.utils.utils import save_object
from src.utils.utils import *


@dataclass

class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts','preprocessor.pkl')


class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

        
    def initialize_data_transformation(self,train_path,test_path):
        try:
            logging.info("readin the train and test data")
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)
            
            logging.info("read train and test data complete")
            logging.info(f'Train Dataframe Head : \n{train_df.head().to_string()}')
            logging.info(f'Test Dataframe Head : \n{test_df.head().to_string()}')
            logging.info("train data processing started")

            train_df=process_data(train_df)
            logging.info("train data processing finished")
            logging.info("test data processing started")
            test_df=process_data(test_df)
            logging.info("test data processing finished")
            

            logging.info("turning the dataframes into np arrays")
            target_column_name = 'Price'
            drop_columns = [target_column_name]
            input_feature_train_df = train_df.drop(columns=drop_columns,axis=1)
            target_feature_train_df=train_df[target_column_name]
            input_feature_test_df=test_df.drop(columns=drop_columns,axis=1)
            target_feature_test_df=test_df[target_column_name]
            train_arr = np.c_[np.array(input_feature_train_df), np.array(target_feature_train_df)]
            test_arr = np.c_[np.array(input_feature_test_df), np.array(target_feature_test_df)]
            logging.info("finished with np arrays")
                        
            
            logging.info("preprocessing pickle file saved")
            
            return (
                train_arr,
                test_arr
            )


        except Exception as e:
            logging.info("Exception occured in the initiate_datatransformation")
            raise customexception(e,sys)

