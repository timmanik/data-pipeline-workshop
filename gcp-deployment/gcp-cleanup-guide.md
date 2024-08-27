# GCP and Kubernetes Resource Cleanup Guide

## 1. Delete Kubernetes Resources

```bash
kubectl delete cronjob data-pipeline-sequence
kubectl delete job,deployment,service --all
kubectl delete secret db-credentials
```

## 2. Delete GKE Cluster

```bash
gcloud container clusters delete weather-cluster --zone=us-central1-a
```

## 3. Delete Container Images

```bash
# List images
gcloud container images list

# Delete images (repeat for each image)
gcloud container images list-tags gcr.io/YOUR_PROJECT_ID/IMAGE_NAME --format='get(digest)' | xargs -I {} gcloud container images delete gcr.io/YOUR_PROJECT_ID/IMAGE_NAME@{} --force-delete-tags --quiet
```

## 4. Clean Up Other Resources

```bash
# Delete disks
gcloud compute disks delete DISK_NAME --zone=ZONE

# Delete firewall rules
gcloud compute firewall-rules delete RULE_NAME

# Delete load balancers
gcloud compute forwarding-rules delete RULE_NAME --global

# Delete static IPs
gcloud compute addresses delete ADDRESS_NAME --region=REGION

# Delete storage buckets
gsutil rm -r gs://BUCKET_NAME

# Delete service accounts
gcloud iam service-accounts delete SERVICE_ACCOUNT_EMAIL
```

## 5. Delete Project (Optional, Use with Caution)

```bash
gcloud projects delete YOUR_PROJECT_ID
```

Replace placeholders with actual resource names. Double-check the Google Cloud Console to ensure all resources are removed.
