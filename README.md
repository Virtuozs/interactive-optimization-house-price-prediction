# House Price Prediction Using Gradient-Based Optimization Methods

This project is an interactive Dash application that demonstrates how
Gradient Descent and Quasi-Newton (BFGS) methods optimize a linear regression
model for house price prediction.

## Features
- Manual and random house data input
- Visualization of regression fit per iteration
- Loss convergence plot
- Parameter trajectory visualization (w, b)
- Comparison of Gradient Descent and Quasi-Newton methods
- Separate training and prediction pages
- Prediction in normalized space and real Rupiah units

## Concepts Demonstrated
- Gradient Descent optimization
- Quasi-Newton (BFGS) optimization
- Feature normalization and denormalization
- Convergence behavior analysis
- Interactive optimization visualization

## Tech Stack
- Python
- Dash & Plotly
- NumPy
- Pandas

## How to Run
```bash
pip install -r requirements.txt
python app.py
