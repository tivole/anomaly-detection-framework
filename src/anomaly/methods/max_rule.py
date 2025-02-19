class MaxRule:
    critical_values = {}

    def __init__(self, n: int = 2, threshold: float = 0.10):
        self.n = n
        self.threshold = threshold

    def fit(self, X):
        for i in range(len(X)):
            for j in range(len(X[i])):
                if j not in self.critical_values:
                    self.critical_values[j] = (0, 0)
                min_value, max_value = self.critical_values[j]
                if X[i][j] < min_value:
                    min_value = X[i][j]
                if X[i][j] > max_value:
                    max_value = X[i][j]
                self.critical_values[j] = (min_value, max_value)

    def predict(self, X) -> float:
        anomaly_count = 0
        for j in range(len(X)):
            min_value, max_value = self.critical_values[j]
            if X[j] > max_value * (1 + self.threshold) or X[j] < min_value * (
                1 - self.threshold
            ):
                anomaly_count += 1

        if anomaly_count >= self.n:
            return 1.0

        return 0.0
