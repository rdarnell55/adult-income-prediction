import pickle, os, json
import numpy as np

def model_fn(model_dir):
    # Load the model from disk
    with open(os.path.join(model_dir, "model.pkl"), "rb") as f:
        return pickle.load(f)

def input_fn(request_body, content_type):
    if content_type == "application/json":
        return np.array([json.loads(request_body)])
    raise ValueError("Unsupported content type: " + content_type)

def predict_fn(input_data, model):
    return model.predict(input_data)

def output_fn(prediction, accept):
    return json.dumps({"prediction": int(prediction[0])}), accept