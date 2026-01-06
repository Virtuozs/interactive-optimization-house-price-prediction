import numpy as np

def quasi_newton_bfgs(model, x, y, lr, iterations):
    theta = np.array([model.w, model.b])
    H_inv = np.eye(2)
    history = []

    def grad(theta):
        model.w, model.b = theta
        return np.array(model.gradients(x, y))

    for _ in range(iterations):
        g = grad(theta)
        theta_new = theta - lr * H_inv @ g

        g_new = grad(theta_new)
        s = theta_new - theta
        yk = g_new - g

        if yk @ s > 1e-8:
            rho = 1.0 / (yk @ s)
            I = np.eye(2)
            H_inv = (
                (I - rho * np.outer(s, yk)) @ H_inv @
                (I - rho * np.outer(yk, s)) +
                rho * np.outer(s, s)
            )

        theta = theta_new
        model.w, model.b = theta

        history.append({
            "w": model.w,
            "b": model.b,
            "loss": model.loss(x, y)
        })

    return history
