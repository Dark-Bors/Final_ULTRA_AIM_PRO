# neural_network.py
# This file defines the neural network model and the training process.

from tensorflow import keras
from sklearn.metrics import r2_score, mean_squared_error
from keras.callbacks import EarlyStopping, LambdaCallback
from app_logging import logger

class NeuralNetworkModel:
    def __init__(self, input_shape, dense1_units=64, dense2_units=32, learning_rate=0.001):
        logger.info(f"ℹ️ Initializing NeuralNetworkModel with input shape {input_shape}, "
                    f"dense1_units={dense1_units}, dense2_units={dense2_units}, "
                    f"learning_rate={learning_rate}")
        self.model = keras.Sequential([
            keras.layers.Dense(dense1_units, activation='relu', input_shape=input_shape),
            keras.layers.Dense(dense2_units, activation='relu'),
            keras.layers.Dense(1)  # One output: reliability
        ])

        optimizer = keras.optimizers.Adam(learning_rate=learning_rate)
        self.model.compile(loss='mean_squared_error', optimizer=optimizer)
        logger.debug("🐛 Model compiled successfully with Adam optimizer and MSE loss.")

    def train(self, X_train, y_train, validation_split=0.07, epochs=1000, batch_size=77, min_delta=0.00001, patience=100):
        logger.info("ℹ️ Training started with the following parameters: "
                    f"validation_split={validation_split}, epochs={epochs}, "
                    f"batch_size={batch_size}, min_delta={min_delta}, patience={patience}")

        # Log epoch beginning and end
        epoch_callback = LambdaCallback(
            on_epoch_begin=lambda epoch, logs: logger.debug(f"🐛 Starting epoch {epoch+1}"),
            on_epoch_end=lambda epoch, logs: logger.debug(f"🐛 Finished epoch {epoch+1}")
        )

        early_stopping = EarlyStopping(
            min_delta=min_delta,
            patience=patience,
            restore_best_weights=True
        )

        history = self.model.fit(
            X_train, y_train,
            validation_split=validation_split,
            epochs=epochs,
            batch_size=batch_size,
            callbacks=[early_stopping, epoch_callback]
        )
        logger.info("ℹ️ Training completed.")
        return history

    def predict(self, X_test):
        logger.debug("🐛 Making predictions on the test set.")
        predictions = self.model.predict(X_test).flatten()
        logger.debug("🐛 Predictions completed.")
        return predictions

    def evaluate(self, X_test, y_test):
        logger.info("ℹ️ Evaluating the model.")
        predicted_reliability = self.predict(X_test)
        r2 = r2_score(y_test, predicted_reliability)
        mse = mean_squared_error(y_test, predicted_reliability)
        logger.info(f"ℹ️ Evaluation results - R^2: {r2:.4f}, MSE: {mse:.4f}")
        return r2, mse