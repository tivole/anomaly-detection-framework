import numpy as np


class ZScore:
    def __init__(self, n: int = 2, threshold: float = 1.5):
        self.threshold = threshold
        self.n = n

    def fit(self, X):
        self.mean = np.mean(X, axis=0)
        self.std = np.std(X, axis=0)
        self.std[self.std == 0] = 1

    def predict(self, X) -> float:
        z = np.abs((X - self.mean) / self.std)
        is_anomaly = (z > self.threshold).sum() >= self.n

        if is_anomaly:
            return 1.0

        return 0.0
