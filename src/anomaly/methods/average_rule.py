class AverageRule:
    average_values = {}

    def __init__(self, n: int = 2, threshold: float = 0.10):
        self.n = n
        self.threshold = threshold

    def fit(self, X):
        for i in range(len(X)):
            for j in range(len(X[i])):
                if j not in self.average_values:
                    self.average_values[j] = 0
                average_value = self.average_values[j]
                average_value += X[i][j]
                self.average_values[j] = average_value

    def predict(self, X) -> float:
        anomaly_count = 0

        for j in range(len(X)):
            average_value = self.average_values[j]
            if X[j] > average_value * (1 + self.threshold) or X[j] < average_value * (
                1 - self.threshold
            ):
                anomaly_count += 1

        if anomaly_count >= self.n:
            return 1.0

        return 0.0
