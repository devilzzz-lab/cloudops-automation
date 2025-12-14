from flask import Flask, jsonify
import os
import socket

app = Flask(__name__)

@app.route('/')
def home():
    # From Jenkins / Docker / Kubernetes
    build_number = os.getenv('BUILD_NUMBER', 'local')
    app_env = os.getenv('APP_ENV', 'not-set')
    log_level = os.getenv('LOG_LEVEL', 'not-set')

    # From Kubernetes Secrets
    db_password = os.getenv('DB_PASSWORD', 'not-set')
    api_key = os.getenv('API_KEY', 'not-set')

    # Kubernetes runtime info
    pod_name = socket.gethostname()

    return f"""
    <html>
    <head>
        <title>CloudOps Automation</title>
    </head>
    <body style="font-family: Arial; background:#0f172a; color:#e5e7eb; padding:30px;">
        <h1>🚀 CloudOps Sample Application</h1>
        <h3>Phase 4 – Kubernetes Deployment</h3>

        <hr>

        <h2>📦 Build Information</h2>
        <ul>
            <li><b>Build Number:</b> {build_number}</li>
            <li><b>Environment:</b> {app_env}</li>
            <li><b>Log Level:</b> {log_level}</li>
            <li><b>Pod Name:</b> {pod_name}</li>
        </ul>

        <h2>🔐 Configuration Injection</h2>
        <p>Values below are injected using Kubernetes ConfigMaps and Secrets:</p>
        <ul>
            <li><b>DB_PASSWORD:</b> {"*" * len(db_password)}</li>
            <li><b>API_KEY:</b> {"*" * len(api_key)}</li>
        </ul>

        <h2>⚙️ CI/CD Pipeline Flow</h2>
        <ol>
            <li>Code pushed to GitHub</li>
            <li>Jenkins pipeline triggered</li>
            <li>Docker image built & pushed to Docker Hub</li>
            <li>Kubernetes manifests applied</li>
            <li>Rolling update performed with zero downtime</li>
        </ol>

        <h2>☸️ Kubernetes Setup</h2>
        <ul>
            <li>Deployment with multiple replicas</li>
            <li>Service exposed via NodePort</li>
            <li>ConfigMap for app configuration</li>
            <li>Secrets for sensitive data</li>
            <li>StatefulSet for database</li>
            <li>DaemonSet for logging</li>
        </ul>

        <p style="color:#22c55e;"><b>✅ Application running successfully inside Kubernetes</b></p>

        <hr>
        <p><i>CloudOps Automation & Monitoring System</i></p>
    </body>
    </html>
    """

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
