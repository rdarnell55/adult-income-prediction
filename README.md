# Adult Income Prediction Project

## 1. Problem Definition and Dataset

This project aims to predict whether an individual earns more than \$50,000 per year based on U.S. Census data. This is framed as a binary classification task where the output label is either `<=50K` or `>50K`.

### Why Machine Learning?

Income prediction involves numerous interrelated demographic and occupational features. A machine learning model can learn complex, nonlinear relationships in this multidimensional space, enabling accurate predictions and useful generalizations for unseen data.

### Dataset

* **Source**: [UCI Machine Learning Repository - Adult Income Dataset](https://archive.ics.uci.edu/ml/datasets/adult)
* **Features Used**:

  * `age`
  * `workclass`
  * `education`
  * `education_num`
  * `marital_status`
  * `occupation`
  * `relationship`
  * `race`
  * `sex`
  * `capital_gain`
  * `capital_loss`
  * `hours_per_week`
  * `native_country`
* **Target**: `income` (binary: `<=50K` or `>50K`)

---

## 2. Data Exploration, Cleaning, and Feature Engineering

Exploratory Data Analysis (EDA) was conducted using Pandas and Seaborn to examine distributions, detect anomalies, and understand feature relationships.

### Key Steps:

* Missing values marked with '?' were identified and removed.
* Categorical features were encoded using `OneHotEncoder`.
* Continuous variables were scaled using `StandardScaler`.
* The `fnlwgt` feature was dropped due to lack of predictive power.

### Notebooks

* All data preprocessing steps were documented and executed in Jupyter Notebook.
* Output: Cleaned dataset, `preprocess.pkl` (scaler and encoder pipeline), and EDA visualizations.

---

## 3. Model Training and Evaluation

The clean dataset was split as follows:

* Training Set: 70%
* Validation Set: 15%
* Test Set: 15%

### Models Considered:

* Logistic Regression
* Decision Tree
* Random Forest

### Chosen Model:

* Logistic Regression (for interpretability and strong baseline performance)

### Evaluation Metrics:

* Accuracy
* Precision
* Recall
* F1 Score

The final model and pipeline were serialized using `joblib` into the `model/` directory.

---

## 4. Local Deployment Using Flask

To serve predictions locally, a Flask web server was created.

### Core Files

* `app.py`: Flask application
* `templates/index.html`: Simple HTML form to collect feature inputs
* `model/`: Directory containing serialized `model.pkl` and `preprocess.pkl`

### Running Locally

```bash
python app.py
```

### Accessing the Application

Open your browser and navigate to:

```
http://localhost:5000
```

Use the provided form to input features and get a prediction.

### Example Prediction Route

An API route `/predict` accepts POST requests with JSON input and returns the predicted class. This enables testing via Postman, curl, or other programmatic clients.

---

## 5. Containerization and DockerHub Push

To make the model portable and reproducible, it was containerized using Docker. This allows the model and all its dependencies to be packaged together, ensuring consistent behavior across environments.

### Docker Setup

The following files were created to support Dockerization:

* `Dockerfile`: Defines the container image, its dependencies, and the command to run the app.
* `requirements.txt`: Contains Python package dependencies.
* `app.py`: Flask application used to serve predictions.
* `model/`: Directory containing serialized model and preprocessing pipeline (`model.pkl`, `preprocess.pkl`).

**Dockerfile:**

```Dockerfile
# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Copy the contents of your project into the container
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port Flask runs on
EXPOSE 5000

# Run the application
CMD ["python", "app/app.py"]
```

### Building and Testing Locally

To build and run the Docker container locally:

```bash
docker build -t income-predictor .
docker run -p 5000:5000 income-predictor
```

You can then test it using `curl`, Postman, or the included HTML form by visiting `http://localhost:5000`.

### Publishing to DockerHub

Once tested locally, the image was pushed to DockerHub for broader accessibility:

```bash
docker tag income-predictor your-dockerhub-username/income-predictor

docker push your-dockerhub-username/income-predictor
```

The container image is now available for use in CI/CD pipelines and cloud platforms such as Heroku or Kubernetes.

This step ensures that anyone, anywhere can pull the image and run it, making the model cloud-native and easily deployable.

---

## 6. CI/CD Pipeline with Heroku Deployment

To automate deployment, a CI/CD pipeline was implemented using GitHub and Heroku. This ensures that updates to the codebase trigger a new deployment without manual intervention.

### Project Structure for CI/CD

* `app.py`: Flask app entry point
* `requirements.txt`: Python dependencies
* `Procfile`: Tells Heroku how to run the app
* `.github/workflows/deploy.yml`: GitHub Actions workflow for CI/CD

**Procfile Example:**

```
web: python app.py
```

### CI/CD YAML:

```yaml
ame: Build and Push Docker Image

on:
  push:
    branches: [ "main" ]

jobs:
  build-and-push:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to DockerHub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_TOKEN }}

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: rdarnell55/income-predictor:latest
```

### Testing the Live App

Once deployed, the application can be tested using the live Heroku URL:

[https://adult-income-prediction-3012ecce80a6.herokuapp.com](https://adult-income-prediction-3012ecce80a6.herokuapp.com)

A simple HTML form served at the root route allows manual input testing. For API-style testing, tools like Postman can be used to send JSON requests to `/predict`.

This CI/CD integration enables rapid iteration, consistent deployment, and reliable delivery of updates with minimal manual steps.

---

## 7. Kubernetes Deployment

To demonstrate orchestration and scalability, the application was also deployed using Kubernetes. This allows for efficient management of containerized workloads across clusters.

### Kubernetes Files Included

* `k8s-deployment.yaml`: Defines the deployment, specifying the number of replicas, container image, ports, and labels.
* `k8s-service.yaml`: Exposes the application using a `NodePort` service for external access.

**k8s-deployment.yaml:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: income-predictor-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: income-predictor
  template:
    metadata:
      labels:
        app: income-predictor
    spec:
      containers:
        - name: income-predictor
          image: rdarnell55/income-predictor:latest
          ports:
            - containerPort: 5000
```

**k8s-service.yaml Example:**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: income-predictor-service
spec:
  type: LoadBalancer
  selector:
    app: income-predictor
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
```

### Deploying to Kubernetes Cluster

```bash
kubectl apply -f k8s-deployment.yaml
kubectl apply -f k8s-service.yaml
```

Access the application at `http://<your-node-ip>:30036`

---

## 8. AWS SageMaker Deployment

To demonstrate scalable cloud-based ML inference, the model was deployed using **Amazon SageMaker**.

### Model Packaging

* The trained `LogisticRegression` model (`model.pkl`) was serialized using `joblib`.
* It was then archived into `model.tar.gz` as required by SageMaker hosting specifications.
* The archive was uploaded to an Amazon S3 bucket: s3://adult-income-model-deploy-ron123/model/model.tar.gz
  
 ### Hosting the Model

* A SageMaker `SKLearnModel` was instantiated using the Scikit-learn container provided by AWS.
* The model was deployed to a real-time endpoint using a `ml.m5.large` instance.
* Python `boto3` and `sagemaker` SDKs were used for deployment automation.

### Flask UI for SageMaker Endpoint

* A separate `apps/app.py` was created to interact with the SageMaker endpoint.
* User input is passed to the endpoint and predictions are rendered dynamically in the browser.

### Live Testing the Endpoint

* The deployed endpoint can be hit via:

- HTML form in Flask app
- Postman or curl:
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '[25, "Private", "Bachelors", ...]' \
  https://runtime.sagemaker.YOUR_REGION.amazonaws.com/endpoints/sagemaker-scikit-learn-2025-06-03-16-09-14-531/invocations
  ```

### Benefits of SageMaker Deployment

* Fully managed, auto-scaling deployment environment.
* Logs, metrics, and endpoint monitoring included.
* Great for demonstrating production-ready deployment in a real cloud environment.


## Summary

This project demonstrates a full end-to-end machine learning workflow:

1. Data preprocessing and feature engineering using Python and Pandas
2. Model training, evaluation, and serialization using scikit-learn
3. Local deployment using Flask
4. Containerization using Docker and hosting on DockerHub
5. CI/CD automation using GitHub Actions with deployment to Heroku
6. Kubernetes orchestration using YAML configuration files
7. Deployment vis AWS SageMaker (endpoint: `sagemaker-scikit-learn-2025-06-03-16-09-14-531`).

Each step was designed to highlight real-world machine learning engineering practices with scalable, production-ready tools.

The project repository includes all source code, models, container and orchestration configurations, as well as documentation for replication and future extension.

## 🎮 Final Notes

This project demonstrates a complete ML engineering lifecycle:

* From raw data to cleaned, engineered features
* From notebook model to real-world, containerized Flask app
* Deployed with both cloud (Heroku) and orchestration tools (Kubernetes)

Feel free to run the local Docker container or ping the Heroku/K8s service to see the model in action.

