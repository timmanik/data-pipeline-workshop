# Weather Data Pipeline Deployment Guide

## Prerequisites
- Google Cloud SDK installed
- kubectl installed
- Docker installed

## Setup

1. List and set your GCP project:
   ```bash
   gcloud projects list
   gcloud config set project ${PROJECT_ID}
   export PROJECT_ID=$(gcloud config get-value project)
   ```

2. Create a GKE cluster:
   ```bash
   gcloud container clusters create weather-cluster --num-nodes=2 --zone=us-central1-a
   ```

3. Get credentials for the cluster:
   ```bash
   gcloud container clusters get-credentials weather-cluster --zone=us-central1-a
   ```

4. Create Kubernetes secret for database credentials:
   ```bash
   kubectl create secret generic db-credentials \
     --from-literal=DB_NAME=your_db_name \
     --from-literal=DB_USER=your_db_user \
     --from-literal=DB_PASSWORD=your_db_password \
     --from-literal=DB_HOST=postgres \
     --from-literal=DB_PORT=5432
   ```

## Build and Push Docker Images

Navigate to the project root directory:

```bash
cd ../gcp-deployment/k8s-artifacts-v2
```

Build and push data pipeline images:

```bash
# Navigate to the data-pipeline directory
cd data-pipeline

# Build and push data pipeline images
docker build --target extract -t gcr.io/${PROJECT_ID}/data-pipeline-extract:latest .
docker build --target load -t gcr.io/${PROJECT_ID}/data-pipeline-load:latest .
docker build --target transform -t gcr.io/${PROJECT_ID}/data-pipeline-transform:latest .

docker push gcr.io/${PROJECT_ID}/data-pipeline-extract:latest
docker push gcr.io/${PROJECT_ID}/data-pipeline-load:latest
docker push gcr.io/${PROJECT_ID}/data-pipeline-transform:latest

# Navigate to the flask-app directory
cd ../flask-app

# Build and push Flask app image
docker build -t gcr.io/${PROJECT_ID}/flask-app:latest .
docker push gcr.io/${PROJECT_ID}/flask-app:latest
```

## Deploy to Kubernetes

Deploy PostgreSQL:

```bash
envsubst < postgres-deployment.yaml | kubectl apply -f -
envsubst < postgres-service.yaml | kubectl apply -f -

# Wait for PostgreSQL to be ready
kubectl wait --for=condition=ready pod -l app=postgres --timeout=300s
```

Deploy data pipeline job:

```bash
envsubst < data-pipeline-job.yaml | kubectl apply -f -
kubectl create job --from=cronjob/data-pipeline-sequence data-pipeline-manual-trigger-new

# Wait for data pipeline job to complete
kubectl wait --for=condition=complete job/data-pipeline --timeout=600s
```

Deploy Flask app:

```bash
envsubst < flask-app-deployment.yaml | kubectl apply -f -
envsubst < flask-app-service.yaml | kubectl apply -f -
```

## Useful Commands for Monitoring and Debugging

1. List all pods:
   ```bash
   kubectl get pods
   ```

2. List all jobs:
   ```bash
   kubectl get jobs
   ```

3. Delete a specific job:
   ```bash
   kubectl delete job data-pipeline-manual-trigger
   ```

4. Delete a cronjob:
   ```bash
   kubectl delete cronjob data-pipeline-sequence
   ```

5. View logs for a specific container in a pod:
   ```bash
   kubectl logs <pod-name> -c <container-name>
   ```

6. List init container names for a pod:
   ```bash
   kubectl get pod <pod-name> -o jsonpath='{.spec.initContainers[*].name}'
   ```

7. View logs continuously:
   ```bash
   kubectl logs -f <pod-name> -c <container-name>
   ```

8. View logs for all containers in a pod:
   ```bash
   kubectl logs <pod-name> --all-containers=true
   ```

9. Describe a pod (lists all containers and their statuses):
   ```bash
   kubectl describe pod <pod-name>
   ```

10. Test environment variable substitution:
    ```bash
    envsubst < data-pipeline-job.yaml
    ```

11. Port forward to access services locally:
    ```bash
    kubectl port-forward service/flask-app 8080:80
    ```

12. Scale a deployment:
    ```bash
    kubectl scale deployment flask-app --replicas=3
    ```

13. View cluster events:
    ```bash
    kubectl get events --sort-by=.metadata.creationTimestamp
    ```

Remember to replace placeholders like `<pod-name>` and `<container-name>` with actual values from your deployment.
