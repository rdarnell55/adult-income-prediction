# Adult Income Prediction Project

## 1. Problem Definition and Dataset

The goal of this project is to build a machine learning model to predict whether an individual earns more than \$50,000 annually, based on demographic and work-related features. This is a binary classification problem, distinguishing between income levels `<=50K` and `>50K`.

**Dataset:**
The [Adult Income Dataset](https://archive.ics.uci.edu/ml/datasets/adult) from the UCI Machine Learning Repository was selected due to its structured format, reliable source, and relevance for socio-economic prediction tasks.

**Features Used:**

* `age` (numerical)
* `education` (categorical, label-encoded)
* `workclass` (categorical)
* `occupation` (categorical)
* `hours-per-week` (numerical)
* `marital-status`, `sex`, `race`, `native-country` and others (categorical)

**Target:**

* `income`: Binary classification — `>50K` or `<=50K`

**ML Justification:**
Machine learning enables us to model non-linear relationships between features and income outcomes, and scale predictions for large populations.

---

## 2. Data Exploration, Cleaning & Feature Engineering

Conducted in a Jupyter Notebook:

* **Data Cleaning:**

  * Removed rows with missing or ambiguous values (`?`)
  * Dropped unnecessary columns like `fnlwgt`

* **Feature Engineering:**

  * Label encoding for binary categories
  * One-hot encoding for multi-category features
  * Scaled numerical features using `StandardScaler`

* **Exploratory Data Analysis:**

  * Visualized income distribution, correlations, and categorical impacts using seaborn/matplotlib

Artifacts:

* `eda-cleaning.ipynb`
* Preprocessed model objects: `model.pkl`, `preprocess.pkl`

---

## 3. Model Training and Evaluation

* **Model Chosen:** Logistic Regression
* **Training/Test Split:** 80/20
* **Cross-Validation:** Stratified K-Fold
* **Metrics:** Accuracy, Precision, Recall, F1 Score

Artifacts:

* Notebook: `train-model.ipynb`
* Serialized files: `model.pkl`, `preprocess.pkl`

---

## 4. Local Deployment Using Flask

* Created a `serve.py` file to define a Flask app with endpoints:

  * `/ping` – Health check
  * `/invocations` – Model prediction (POST with JSON)

* Ran locally via:

  ```bash
  python serve.py
  ```

* Test using `curl` or Postman:

  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"features": [52, 287927, 13, 15000, 0, 60]}' http://localhost:8080/invocations
  ```

---

## 5. Containerization and DockerHub Push

* Dockerized the Flask app:

  * Used `python:3.10-slim` as base image
  * Installed dependencies from `requirements.txt`
  * Exposed port 8080 for inference

* Docker commands:

  ```bash
  docker build -t income-predictor .
  docker tag income-predictor <your-dockerhub-username>/income-predictor
  docker push <your-dockerhub-username>/income-predictor
  ```

Artifacts:

* `Dockerfile`
* `requirements.txt`

---

## 6. CI/CD Pipeline with Heroku Deployment

* **GitHub Actions** workflow automates:

  * Build
  * Test
  * Deploy to Heroku on `main` push

* **Heroku Setup:**

  * `Procfile` defined to run gunicorn
  * `runtime.txt`, `requirements.txt` included
  * Deployment verified via Heroku Logs and `/ping` health check

* Test deployment:

  ```bash
  curl https://<your-heroku-app>.herokuapp.com/ping
  ```

* GitHub Actions file: `.github/workflows/deploy.yml`

Artifacts:

* `.github/workflows/deploy.yml`
* `Procfile`
* `runtime.txt`

---

## 7. Kubernetes Deployment

* **Configuration:** Deployed using Kubernetes cluster with YAML definition.

* **Key Resources:**

  * `deployment.yaml`: Defines pod, replica set, container image
  * `service.yaml`: Exposes deployment via ClusterIP or LoadBalancer

* Commands:

  ```bash
  kubectl apply -f deployment.yaml
  kubectl apply -f service.yaml
  kubectl get pods
  kubectl port-forward service/income-predictor 12345:80
  ```

* Test with:

  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"features": [52, 287927, 13, 15000, 0, 60]}' http://localhost:12345/invocations
  ```

Artifacts:

* `deployment.yaml`
* `service.yaml`

---

## 8. (Optional Extra Credit) AWS SageMaker Deployment

⚠️ **Not submitted as part of the main assignment.**
Efforts were made to deploy the containerized model to AWS SageMaker using the ECR-hosted image. The process involved:

* Creating an ECR repository
* Using AWS CodeBuild to push the Docker image
* Deploying with the `sagemaker.Model` class

SageMaker deployment was not finalized due to compatibility issues and time constraints.

---

## ✅ Summary Checklist

| Task                                               | Status      |
| -------------------------------------------------- | ----------- |
| Define problem and dataset                         | ✅ Completed |
| Data cleaning and feature engineering              | ✅ Completed |
| Model training and evaluation                      | ✅ Completed |
| Local Flask deployment                             | ✅ Completed |
| Docker container + DockerHub                       | ✅ Completed |
| CI/CD pipeline and Heroku deployment               | ✅ Completed |
| Kubernetes deployment                              | ✅ Completed |
| AWS SageMaker deployment (extra credit - optional) | ⏳ Attempted |

---

## 🎮 Final Notes

This project demonstrates a complete ML engineering lifecycle:

* From raw data to cleaned, engineered features
* From notebook model to real-world, containerized Flask app
* Deployed with both cloud (Heroku) and orchestration tools (Kubernetes)

Feel free to run the local Docker container or ping the Heroku/K8s service to see the model in action.

