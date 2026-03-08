from sklearn.neural_network import MLPRegressor

def train_model(X_train, y_train):
    """
    Train model MLP Regressor untuk prediksi harga crypto.
    """
    model = MLPRegressor(
        hidden_layer_sizes=(64, 32),
        max_iter=500,
        random_state=42
    )
    model.fit(X_train, y_train)
    print(f"[train] Model selesai ditraining.")
    return model