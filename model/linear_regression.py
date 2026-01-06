import numpy as np

class LinearRegressionModel:
    def __init__(self, w=0.0, b=0.0):
        self.w = w
        self.b = b

    def predict(self, x):
        return self.w * x + self.b

    def loss(self, x, y):
        return np.mean((y - self.predict(x)) ** 2)

    def gradients(self, x, y):
        y_pred = self.predict(x)
        dw = -2 * np.mean(x * (y - y_pred))
        db = -2 * np.mean(y - y_pred)
        return dw, db
