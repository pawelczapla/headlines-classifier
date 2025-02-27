# ML Model API with Kubernetes and Minikube

This project provides a Kubernetes-based deployment for serving a Machine Learning model using FastAPI.

## Prerequisites
- Docker
- Minikube
- kubectl
- Python 3.7+

## Deployment Steps

### Build and Deploy the ML API
Run the setup script:
```sh
python3 scripts/setup_k8s.py --setup
```
This will build the Docker image, deploy Kubernetes resources, and output the service URL.

### (optional) Get the Service URL
```sh
minikube service ml-api-service --url
```

### Send a Prediction Request
```sh
python3 src/python/client.py --url <service_url> --headline "Breaking: Cure for cancer finally discovered!"
```

### Cleanup Kubernetes Resources
```sh
python3 scripts/setup_k8s.py --cleanup
```
