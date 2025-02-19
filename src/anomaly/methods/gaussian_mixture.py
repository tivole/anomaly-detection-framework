from sklearn.mixture import GaussianMixture


class GaussianMixtureWithThreshold:
    def __init__(
        self,
        n_components: int = 1,
        threshold: float = 0.5,
        covariance_type: str = "full",
    ):
        self.n_components = n_components
        self.threshold = threshold
        self.model = GaussianMixture(
            n_components=n_components, covariance_type=covariance_type
        )
        self.fitted_scores = None

    def fit(self, X):
        self.model.fit(X)
        scores = self.model.score_samples(X)
        self.fitted_scores = scores
        if self.threshold is None:
            self.threshold = scores.mean() - 2 * scores.std()

    def predict(self, X) -> float:
        X_2d = X.reshape(1, -1)
        scores = self.model.score_samples(X_2d)
        is_anomaly = scores[0] < self.threshold
        if is_anomaly:
            return 1.0
        return 0.0
