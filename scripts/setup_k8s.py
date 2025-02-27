import subprocess
import os
import time
import argparse

IMAGE_NAME = "my-ml-api"
DEPLOYMENT_FILE = "deployment.yaml"
SERVICE_NAME = "ml-api-service"

def run_command(command, exit_on_fail=True):
    """Run a shell command and return the output.
    
    Args:
        command (str): The shell command to execute.
        exit_on_fail (bool, optional): Whether to exit the script on failure. Defaults to True.
    
    Returns:
        str: The command's output if successful, otherwise exits the script.
    """
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        if exit_on_fail:
            exit(1)
    return result.stdout.strip()

def start_minikube():
    """Start the Minikube cluster."""
    print("Starting Minikube...")
    run_command("minikube start")

def build_image():
    """Build the Docker image inside Minikube's Docker environment."""
    print("Building Docker image inside Minikube...")
    run_command("eval $(minikube docker-env) && docker build -t my-ml-api .")

def deploy():
    """Deploy the ML API to Kubernetes using the specified deployment YAML file."""
    print("Deploying ML API...")
    run_command(f"kubectl apply -f {DEPLOYMENT_FILE}")

def wait_for_pod():
    """Wait until the ML API pod is ready, with a timeout of 60 seconds."""
    print("Waiting for pod to be ready...")
    run_command("kubectl wait --for=condition=ready pod -l app=ml-api --timeout=60s")

def port_forward():
    """Forward the Kubernetes service port to localhost for direct access."""
    print("Forwarding service port to localhost...")
    run_command("kubectl port-forward svc/ml-api-service 8000:80", exit_on_fail=False)

def cleanup():
    """Clean up Kubernetes resources and stop Minikube."""
    print("Cleaning up resources...")
    run_command("kubectl delete deployment ml-api", exit_on_fail=False)
    run_command(f"kubectl delete service {SERVICE_NAME}", exit_on_fail=False)
    run_command("minikube stop", exit_on_fail=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage Minikube and Kubernetes deployment.")
    parser.add_argument("--setup", action="store_true", help="Start Minikube, build image, and deploy service")
    parser.add_argument("--cleanup", action="store_true", help="Stop Minikube and delete resources")
    
    args = parser.parse_args()

    if args.setup:
        start_minikube()
        build_image()
        deploy()
        wait_for_pod()
        port_forward()
    elif args.cleanup:
        cleanup()
    else:
        parser.print_help()
