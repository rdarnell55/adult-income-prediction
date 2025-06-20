import sagemaker
from sagemaker.sklearn.model import SKLearnModel
from sagemaker import get_execution_role

# Initialize SageMaker session and IAM role
sagemaker_session = sagemaker.Session()

# Use get_execution_role() *only* if you're running in SageMaker Studio/Notebook
# If not, paste your IAM role ARN directly:
# role = "arn:aws:iam::123456789012:role/service-role/AmazonSageMaker-ExecutionRole-2025..."

role = "arn:aws:iam::998072949015:role/service-role/AmazonSageMaker-ExecutionRole-20250520T123874"

model = SKLearnModel(
    model_data="s3://adult-income-model-deploy-ron123/model/model.tar.gz",
    role=role,
    entry_point="inference.py",
    framework_version="0.23-1",
    py_version="py3",
    sagemaker_session=sagemaker_session
)

predictor = model.deploy(
    initial_instance_count=1,
    instance_type="ml.m5.large"
)