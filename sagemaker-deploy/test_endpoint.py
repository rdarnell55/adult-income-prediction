import boto3
import json

# Use your actual endpoint name from the console
endpoint_name = "sagemaker-scikit-learn-2025-06-03-16-09-14-531"

# Sample input — must match what your model expects
# For the dummy model, 5 numeric features
input_data = [0.5, 0.2, 0.8, 0.1, 0.3]

# Call the endpoint
runtime = boto3.client("sagemaker-runtime")

response = runtime.invoke_endpoint(
    EndpointName=endpoint_name,
    ContentType="application/json",
    Body=json.dumps(input_data)
)

result = response["Body"].read().decode("utf-8")
print("Prediction result:", result)