import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification

# Generate dummy data (5 features to match a simple classifier style)
X, y = make_classification(n_samples=100, n_features=5, random_state=42)

# Train the model
model = LogisticRegression()
model.fit(X, y)

# Save the model to a file
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model saved as model.pkl")