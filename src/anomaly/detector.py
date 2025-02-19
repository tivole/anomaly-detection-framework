from .collection import MonitoredFeature
import numpy as np


class Detector:
    def __init__(
        self,
        method,
        predict_transform=None,
        features: list[MonitoredFeature] = [],
    ) -> None:
        """
        :param method: An anomaly detection method that supports .fit() and .predict()
        :param predict_transform: An optional function to transform the raw prediction
                                  into a probability or score. If None, the raw prediction is returned.
        """
        self._method = method
        self._predict_transform = predict_transform or (lambda x: x)
        self._features = features

    def fit(self, data: list[dict]) -> None:
        """Fit the detection method with the provided data."""
        train_data = [[d[feature] for feature in self._features] for d in data]
        numpy_data = np.array(train_data)
        self._method.fit(numpy_data)

    def predict(self, data_point: dict) -> float:
        """
        Return a transformed prediction value for the data point.
        For example, if the method returns -1 for anomalies, the transform might convert that to 1.0.
        """
        test_data_point = [data_point[feature] for feature in self._features]
        numpy_data_point = np.array(test_data_point)
        raw_prediction = self._method.predict(numpy_data_point)
        return self._predict_transform(raw_prediction)

    def get_name(self) -> str:
        """Return the name of the detection method."""
        return self._method.__class__.__name__
