import pickle

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

print("Model loaded successfully.")
print("Model type:", type(model))