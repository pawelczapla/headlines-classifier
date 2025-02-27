import requests
import argparse
import subprocess

SERVICE_NAME = "ml-api-service"

def run_command(command):
    """Run a shell command and return the output."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else None

def send_request(service_url, headline):
    """Send a request to the ML service and return the response."""
    data = {"text": headline}
    try:
        response = requests.post(f"{service_url}/predict", json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def main():
    parser = argparse.ArgumentParser(description="Send a request to the ML API.")
    parser.add_argument("--url", type=str, default="http://127.0.0.1:8000", help="Minikube service URL (fetch if not provided)")
    parser.add_argument("--headline", type=str, required=True, help="Headline for classification")

    args = parser.parse_args()

    if not args.url:
        print("Failed to get Minikube service URL. Is the service running?")
        exit(1)

    response = send_request(args.url, args.headline)
    print("Response:", response)

if __name__ == "__main__":
    main()
