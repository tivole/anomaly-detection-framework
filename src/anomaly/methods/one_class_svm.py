from sklearn.svm import OneClassSVM


class OneClassSVMWrapper:
    def __init__(self, kernel: str = "rbf", nu: float = 0.1, gamma: str = "scale"):
        self.model = OneClassSVM(kernel=kernel, nu=nu, gamma=gamma)

    def fit(self, X):
        self.model.fit(X)

    def predict(self, X) -> float:
        X_2d = X.reshape(1, -1)
        preds = self.model.predict(X_2d)
        return 1.0 if preds[0] == -1 else 0.0
