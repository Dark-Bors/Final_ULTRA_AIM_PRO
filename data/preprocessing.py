# preprocessing.py
# This file contains functions for data cleaning, scaling, and splitting.

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np
from app_logging import logger


def calculate_reliability(row, t=87660 * 10):
    lambda_ = 1 / row['ttf']
    return np.exp(-lambda_ * t) * 100

def preprocess_data(file_path):
    logger.info("ℹ️ Starting preprocessing of data.")

    try:
        # Load the data
        data = pd.read_excel(file_path)
        logger.info("ℹ️ Data loaded successfully from {}".format(file_path))
    except Exception as e:
        logger.critical("⛔ Critical error in loading data: {}".format(e))
        raise e

    # Check if columns have the correct data type
    columns_to_check = ['V', 'f', 'T', 'N', 'ttf']
    for col in columns_to_check:
        if not pd.api.types.is_numeric_dtype(data[col]):
            logger.warning("⚠️ Column {} is not numeric. Converting to numeric dtype.".format(col))
            data[col] = pd.to_numeric(data[col], errors='coerce')

    try:
        # Drop rows with any NaN values
        initial_row_count = len(data)
        data = data.dropna()
        dropped_row_count = initial_row_count - len(data)
        logger.info("ℹ️ Dropped {} rows due to NaN values.".format(dropped_row_count))
    except Exception as e:
        logger.critical("⛔ Critical error when dropping NaN values: {}".format(e))
        raise e

    try:
        # Add a new column for the reliability
        data['reliability'] = data.apply(calculate_reliability, axis=1)
        logger.info("ℹ️ Reliability column added successfully.")
    except Exception as e:
        logger.critical("⛔ Critical error when calculating reliability: {}".format(e))
        raise e

    try:
        # Feature Engineering: Add new feature if possible, for now just square of 'N'
        data['N_squared'] = data['N'] ** 2
        logger.info("ℹ️ N_squared feature engineered successfully.")
    except Exception as e:
        logger.critical("⛔ Critical error in feature engineering N_squared: {}".format(e))
        raise e

    try:
        # Extract features and targets
        X = data[['V', 'f', 'T', 'N', 'N_squared']].values
        Y_reliability = data['reliability'].values
        logger.debug("🐛 Features and targets extracted.")
    except Exception as e:
        logger.critical("⛔ Critical error in extracting features and targets: {}".format(e))
        raise e

    try:
        # Normalize the inputs
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        logger.info("ℹ️ Input data normalized successfully.")
    except Exception as e:
        logger.critical("⛔ Critical error in input normalization: {}".format(e))
        raise e

    try:
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, Y_reliability, test_size=0.05, random_state=250)
        logger.info("ℹ️ Data split into train and test sets successfully.")
    except Exception as e:
        logger.critical("⛔ Critical error in data splitting: {}".format(e))
        raise e

    return X_train, X_test, y_train, y_test, scaler
