from sklearn.metrics import mean_squared_error
import numpy as np

def evaluate_rmse(y_true, y_pred):
    """
    Hitung RMSE antara nilai aktual dan prediksi.
    """
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    print(f"[evaluate] RMSE: {rmse:.4f}")
    return rmse