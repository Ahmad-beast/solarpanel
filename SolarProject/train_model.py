import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

# Sample dataset banana
data = {
    'temperature': [15, 20, 25, 30, 35, 22, 18, 28, 32, 40],
    'irradiance': [0.2, 0.4, 0.6, 0.8, 1.0, 0.5, 0.3, 0.7, 0.9, 0.95],
    'power_output': [150, 300, 500, 750, 950, 450, 250, 650, 850, 900]
}
df = pd.DataFrame(data)

# Features (Input) aur Target (Output) ko alag karna
X = df[['temperature', 'irradiance']]
y = df['power_output']

# Machine Learning Model ko initialize aur train karna
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Trained model ko file mein save karna
joblib.dump(model, 'solar_model.joblib')

print("Model train ho gaya aur 'solar_model.joblib' file save ho gayi hai!")