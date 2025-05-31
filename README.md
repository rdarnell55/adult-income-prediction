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

### 4. Local Deployment Using Flask

To demonstrate local model deployment, a lightweight web app was built using **Flask**. This application provides a simple, form-based UI to input demographic and employment-related attributes, then returns a prediction on whether the individual earns more or less than $50,000 per year.

#### File Structure (Relevant to Local Deployment)
- `app.py` — Flask application entry point  
- `templates/` — contains the HTML form (e.g., `form.html`)  
- `model/`
  - `model.pkl` — trained classification model  
  - `preprocess.pkl` — preprocessing pipeline used on input data  

####️ How to Run Locally
1. **Install dependencies** (ideally in a virtual environment):
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Flask app**:
   ```bash
   python app.py
   ```

3. **Open a browser to**:
   ```
   http://127.0.0.1:5000/
   ```

4. **Use the web interface** to submit data and receive live predictions.

#### How It Works
- The `app.py` file loads the pre-trained model and preprocessing pipeline.
- User inputs from the form are processed and transformed before being passed to the model.
- The model predicts whether the individual earns `>50K` or `<=50K`, and the result is displayed in the browser.

#### Requirements Met
- This implementation fulfills the requirement to deploy the trained machine learning model on a **local machine using Flask**.

---

## 5. Containerization and DockerHub Push

To make the model portable and reproducible, it was containerized using Docker. This allows the model and all its dependencies to be packaged together, ensuring consistent behavior across environments.

### Docker Setup

The following files were created to support Dockerization:

* `Dockerfile`: Defines the container image, its dependencies, and the command to run the app.
* `requirements.txt`: Contains Python package dependencies.
* `app.py`: Flask application used to serve predictions.
* `model/`: Directory containing serialized model and preprocessing pipeline (`model.pkl`, `preprocess.pkl`).

**Dockerfile Example:**

```Dockerfile
# 5. Containerization and DockerHub Push

To make the model portable and reproducible, it was containerized using Docker. This allows the model and all its dependencies to be packaged together, ensuring consistent behavior across environments.

### Docker Setup

The following files were created to support Dockerization:

* `Dockerfile`: Defines the container image, its dependencies, and the command to run the app.
* `requirements.txt`: Contains Python package dependencies.
* `app.py`: Flask application used to serve predictions.
* `model/`: Directory containing serialized model and preprocessing pipeline (`model.pkl`, `preprocess.pkl`).

**Dockerfile Example:**

```Dockerfile
   FROM python:3.10-slim
   WORKDIR /app
   COPY requirements.txt ./
   RUN pip install --no-cache-dir -r requirements.txt
   COPY . .
   EXPOSE 5000
   CMD ["python", "app.py"]
```

### Building and Testing Locally

To build and run the Docker container locally:

```bash
   docker build -t income-predictor .
   docker run -p 5000:5000 income-predictor
```

You can then test it using `curl` or a tool like Postman to send JSON to `http://localhost:5000/predict`.

### Publishing to DockerHub

Once tested locally, the image was pushed to DockerHub for broader accessibility:

```bash
   docker tag income-predictor your-dockerhub-username/income-predictor
   docker push your-dockerhub-username/income-predictor
```

The container image is now available for use in CI/CD pipelines and cloud platforms such as Heroku or Kubernetes.
This step ensures that anyone, anywhere can pull the image and run it, making the model cloud-native and easily deployable.
```

### Building and Testing Locally

To build and run the Docker container locally:

```bash
   docker build -t income-predictor .
   docker run -p 5000:5000 income-predictor
```

You can then test it using `curl` or a tool like Postman to send JSON to `http://localhost:5000/predict`.

### Publishing to DockerHub

Once tested locally, the image was pushed to DockerHub for broader accessibility:

```bash
   docker tag income-predictor your-dockerhub-username/income-predictor
   docker push your-dockerhub-username/income-predictor
```

The container image is now available for use in CI/CD pipelines and cloud platforms such as Heroku or Kubernetes.
This step ensures that anyone, anywhere can pull the image and run it, making the model cloud-native and easily deployable.


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

    https://adult-income-prediction-3012ecce80a6.herokuapp.com/  

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

