import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.optimizers import Adam

class LSTMModel:
    def __init__(self, time_step=60, prediction_days=30):
        self.time_step = time_step
        self.prediction_days = prediction_days
        self.model = None
        
    def build_model(self, input_shape):
        """Build LSTM model architecture."""
        # Fix for TensorFlow version compatibility
        tf.compat.v1.disable_eager_execution()
        
        model = Sequential()
        
        # First LSTM layer with Dropout
        model.add(LSTM(
            units=50, 
            return_sequences=True, 
            input_shape=input_shape,
            recurrent_dropout=0
        ))
        model.add(Dropout(0.2))
        
        # Second LSTM layer with Dropout
        model.add(LSTM(
            units=50, 
            return_sequences=False,
            recurrent_dropout=0
        ))
        model.add(Dropout(0.2))
        
        # Output layer
        model.add(Dense(units=1))
        
        # Compile model
        model.compile(optimizer='adam', loss='mean_squared_error')
        
        self.model = model
        return model
    
    def train(self, X_train, y_train, X_test, y_test, epochs=50, batch_size=32, verbose=1):
        """Train the LSTM model."""
        if self.model is None:
            self.build_model(input_shape=(X_train.shape[1], 1))
        
        # Early stopping to prevent overfitting
        early_stopping = EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True
        )
        
        # Train the model
        history = self.model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_data=(X_test, y_test),
            callbacks=[early_stopping],
            verbose=verbose
        )
        
        return history
    
    def predict(self, X):
        """Make predictions with the trained model."""
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        
        return self.model.predict(X)
    
    def predict_future(self, last_sequence, scaler, days=None):
        """Predict future values based on the last sequence of data."""
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        
        if days is None:
            days = self.prediction_days
            
        # Initialize future predictions with the last sequence
        future_sequence = last_sequence.copy()
        future_predictions = []
        
        # Predict for the number of days
        for _ in range(days):
            # Reshape for prediction
            current_seq = future_sequence[-self.time_step:].reshape(1, self.time_step, 1)
            
            # Predict next day
            next_day = self.model.predict(current_seq)[0][0]
            
            # Add to predictions
            future_predictions.append(next_day)
            
            # Add to sequence for next iteration
            future_sequence = np.append(future_sequence, next_day)
        
        # Transform predictions back to original scale
        future_predictions = np.array(future_predictions).reshape(-1, 1)
        future_predictions = scaler.inverse_transform(future_predictions)
        
        return future_predictions
    
    def save_model(self, filepath):
        """Save the trained model."""
        if self.model is None:
            raise ValueError("No model to save. Train the model first.")
        
        self.model.save(filepath)
    
    def load_model(self, filepath):
        """Load a trained model."""
        self.model = tf.keras.models.load_model(filepath)
        return self.model 