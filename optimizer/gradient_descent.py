def gradient_descent(model, x, y, lr, iterations):
    history = []

    for i in range(iterations):
        dw, db = model.gradients(x, y)
        model.w -= lr * dw
        model.b -= lr * db

        history.append({
            "w": model.w,
            "b": model.b,
            "loss": model.loss(x, y)
        })

    return history
