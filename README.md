# Data Pipeline Workshop

This repository contains a proof of concept for a simple data pipeline and its deployment to Kubernetes on Google Cloud Platform (GCP). The project is designed as a teaching tool for researchers to learn about containerization and data pipelines.

**Note:** This is not intended to be a production workflow. It's meant for teaching the basics of containers and Kubernetes. For some opiniated thoughts on who a productionized version of this workflow would look like, refer to [production-workflow-explanation](supplementary-guides/production-workflow-explanation.md).

## Repository Structure

```
data-pipeline-workshop/
├── README.md
├── data-pipeline/
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── scripts/
│   │   ├── transform.py
│   │   ├── load.py
│   │   └── extract.py
│   ├── entrypoints/
│   │   ├── transform.sh
│   │   ├── load.sh
│   │   └── extract.sh
│   └── docker-compose.yml
├── flask-app/
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── static/
│   │   └── styles.css
│   ├── app.py
│   ├── templates/
│   │   ├── index.html
│   │   └── layout.html
│   └── docker-compose.yml
└── gcp-deployment/
    └── k8s-artifacts/
        ├── postgres-deployment.yaml
        ├── data-pipeline-job.yaml
        ├── flask-app-deployment.yaml
        ├── postgres-service.yaml
        └── flask-app-service.yaml
```

## Components

1. **Data Pipeline**: Contains scripts for extracting, loading, and transforming data, along with Dockerfile and docker-compose configuration for containerization.

2. **Flask App**: A simple web application to visualize the processed data, including Dockerfile and docker-compose configuration.

3. **GCP Deployment**: Kubernetes manifests for deploying the data pipeline and Flask app on Google Cloud Platform.

## Getting Started

1. Clone this repository
2. Follow the instructions in each component's directory to build and run the containers locally
3. Use the Kubernetes manifests in the `gcp-deployment` directory to deploy the application to GCP

For detailed instructions on using this project for learning purposes, please refer to the workshop materials.
