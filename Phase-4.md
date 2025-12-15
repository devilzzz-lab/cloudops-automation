<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>

<h1>🟧 PHASE-4: CI/CD Pipeline & Automation (README.md)</h1>

<p><strong>Version:</strong> Phase 4<br>
<strong>Module:</strong> CI/CD Jobs, Webhooks & Automated Deployment<br>
<strong>Project:</strong> CloudOps Automation, CI/CD &amp; Monitoring System</p>

<hr>

<h2>📌 1. Overview</h2>

<p>Phase-4 focuses on creating a complete CI/CD automation pipeline using the environment set up in Phase-3.</p>

<p>This phase covers:</p>
<ul>
<li>✔ Creating GitHub repository with application code</li>
<li>✔ Writing Kubernetes manifests</li>
<li>✔ Creating CI job for Docker build and push</li>
<li>✔ Creating CD job for Kubernetes deployment</li>
<li>✔ Setting up ngrok for webhook access</li>
<li>✔ Configuring GitHub webhooks</li>
<li>✔ Testing complete automation</li>
</ul>

<p><strong>Prerequisites:</strong> Phase-3 must be completed (Docker + KIND + Jenkins fully configured).</p>

<hr>

<h2>🧩 2. CI/CD Pipeline Architecture</h2>

<pre>
Developer (Local Machine)
        |
        | git push
        v
  GitHub Repository
        |
        | Webhook (via ngrok)
        v
      Jenkins
        |
        |-- Job 1: cloudops-ci-build
        |   ├── Checkout code
        |   ├── Build Docker image
        |   └── Push to Docker Hub
        |
        |-- Job 2: cloudops-prod-deploy
        |   ├── Apply K8s manifests
        |   ├── Wait for rollout
        |   └── Verify deployment
        |
        v
    Docker Hub
        |
        | Pull image
        v
  KIND Kubernetes Cluster
        |
        └── Running Application
</pre>

<hr>

<h2>🐳 3. Project Repository Setup</h2>

<h3>Step 3.1: Create GitHub Repository</h3>
<p>Create a new repository named: <code>cloudops-automation</code></p>

<h3>Step 3.2: Project Structure</h3>
<pre>
cloudops-automation/
├── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── README.md
└── k8s/
    ├── namespace.yaml
    ├── configmap.yaml
    ├── deployment.yaml
    └── service.yaml
</pre>

<h3>Step 3.3: Application Code (app.py)</h3>
<pre>
from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return f"&lt;h1&gt;CloudOps Sample App&lt;/h1&gt;&lt;p&gt;Build: {os.getenv('BUILD_NUMBER', 'local')}&lt;/p&gt;"

@app.route('/health')
def health():
    return {"status": "healthy"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
</pre>

<h3>Step 3.4: requirements.txt</h3>
<pre>
Flask==3.0.0
</pre>

<h3>Step 3.5: Dockerfile</h3>
<pre>
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["python", "app.py"]
</pre>

<hr>

<h2>📁 4. Create Kubernetes Manifests</h2>

<h3>4.1 Namespace (k8s/namespace.yaml)</h3>
<pre>
apiVersion: v1
kind: Namespace
metadata:
  name: cloudops
  labels:
    name: cloudops
</pre>

<h3>4.2 ConfigMap (k8s/configmap.yaml)</h3>
<pre>
apiVersion: v1
kind: ConfigMap
metadata:
  name: cloudops-config
  namespace: cloudops
data:
  APP_ENV: "production"
  LOG_LEVEL: "info"
</pre>

<h3>4.3 Deployment (k8s/deployment.yaml)</h3>
<pre>
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cloudops-app
  namespace: cloudops
spec:
  replicas: 3
  selector:
    matchLabels:
      app: cloudops-app
  template:
    metadata:
      labels:
        app: cloudops-app
    spec:
      containers:
      - name: cloudops-app
        image: devilzz/cloudops-sample-app:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 8080
        env:
        - name: APP_ENV
          valueFrom:
            configMapKeyRef:
              name: cloudops-config
              key: APP_ENV
        - name: LOG_LEVEL
          valueFrom:
            configMapKeyRef:
              name: cloudops-config
              key: LOG_LEVEL
</pre>

<p><strong>Replace <code>devilzz</code> with your Docker Hub username!</strong></p>

<h3>4.4 Service (k8s/service.yaml)</h3>
<pre>
apiVersion: v1
kind: Service
metadata:
  name: cloudops-service
  namespace: cloudops
spec:
  type: NodePort
  selector:
    app: cloudops-app
  ports:
  - port: 80
    targetPort: 8080
    nodePort: 30080
    protocol: TCP
</pre>

<h3>Step 4.5: Commit and Push to GitHub</h3>
<pre>
git init
git add .
git commit -m "Initial commit with app and K8s manifests"
git branch -M main
git remote add origin https://github.com/&lt;your-username&gt;/cloudops-automation.git
git push -u origin main
</pre>

<hr>

<h2>🟦 5. Create CI Build Job (cloudops-ci-build)</h2>

<h3>5.1 Create New Job</h3>
<ol>
<li>Go to Jenkins Dashboard</li>
<li>Click <strong>New Item</strong></li>
<li>Enter name: <strong>cloudops-ci-build</strong></li>
<li>Select <strong>Freestyle project</strong></li>
<li>Click <strong>OK</strong></li>
</ol>

<h3>5.2 Configure Source Code Management</h3>
<p><strong>Source Code Management → Git:</strong></p>

<table border="1">
<tr>
<th>Field</th>
<th>Value</th>
</tr>
<tr>
<td>Repository URL</td>
<td><code>https://github.com/&lt;your-username&gt;/cloudops-automation.git</code></td>
</tr>
<tr>
<td>Credentials</td>
<td>Select <strong>github-token</strong></td>
</tr>
<tr>
<td>Branch Specifier</td>
<td><code>*/main</code></td>
</tr>
</table>

<h3>5.3 Configure Build Triggers</h3>
<p>Enable:</p>
<ul>
<li>☑ <strong>GitHub hook trigger for GITScm polling</strong></li>
</ul>

<h3>5.4 Configure Build Environment</h3>
<p>Enable:</p>
<ul>
<li>☑ <strong>Use secret text(s) or file(s)</strong></li>
</ul>

<p>Add binding:</p>
<table border="1">
<tr>
<th>Field</th>
<th>Value</th>
</tr>
<tr>
<td>Binding Type</td>
<td>Username and password (separated)</td>
</tr>
<tr>
<td>Username Variable</td>
<td><code>DOCKER_USER</code></td>
</tr>
<tr>
<td>Password Variable</td>
<td><code>DOCKER_PASS</code></td>
</tr>
<tr>
<td>Credentials</td>
<td>Select <strong>dockerhub-creds</strong></td>
</tr>
</table>

<h3>5.5 Add Build Step (Execute Shell)</h3>
<p>Click <strong>Add build step → Execute shell</strong> and paste:</p>

<pre>
#!/bin/bash
set -e

REGISTRY="devilzz"
IMAGE="cloudops-sample-app"
TAG="build-${BUILD_NUMBER}"
FULL_IMAGE="${REGISTRY}/${IMAGE}"

echo "===================================="
echo "🔨 CI JOB – Docker Build & Push"
echo "Image: ${FULL_IMAGE}:${TAG}"
echo "===================================="

# Docker Login
echo "🔐 Logging into Docker Hub..."
echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin

# Docker Build
echo "🐳 Building image..."
docker build -t ${FULL_IMAGE}:${TAG} .

# Tag as latest
docker tag ${FULL_IMAGE}:${TAG} ${FULL_IMAGE}:latest

# Push images
echo "📤 Pushing images..."
docker push ${FULL_IMAGE}:${TAG}
docker push ${FULL_IMAGE}:latest

echo "✅ CI Build completed successfully"
echo "📦 Image: ${FULL_IMAGE}:${TAG}"
echo "📦 Image: ${FULL_IMAGE}:latest"
</pre>

<p><strong>Replace <code>devilzz</code> with your Docker Hub username!</strong></p>

<h3>5.6 Save the Job</h3>
<p>Click <strong>Save</strong>.</p>

<hr>

<h2>🟩 6. Create CD Deployment Job (cloudops-prod-deploy)</h2>

<h3>6.1 Create New Job</h3>
<ol>
<li>Go to Jenkins Dashboard</li>
<li>Click <strong>New Item</strong></li>
<li>Enter name: <strong>cloudops-prod-deploy</strong></li>
<li>Select <strong>Freestyle project</strong></li>
<li>Click <strong>OK</strong></li>
</ol>

<h3>6.2 Configure Source Code Management</h3>
<p><strong>Source Code Management → Git:</strong></p>

<table border="1">
<tr>
<th>Field</th>
<th>Value</th>
</tr>
<tr>
<td>Repository URL</td>
<td><code>https://github.com/&lt;your-username&gt;/cloudops-automation.git</code></td>
</tr>
<tr>
<td>Credentials</td>
<td>Select <strong>github-token</strong></td>
</tr>
<tr>
<td>Branch Specifier</td>
<td><code>*/main</code></td>
</tr>
</table>

<h3>6.3 Configure Build Triggers</h3>
<p>Enable:</p>
<ul>
<li>☑ <strong>Build after other projects are built</strong></li>
<li>Projects to watch: <code>cloudops-ci-build</code></li>
<li>Trigger only if build is stable</li>
</ul>

<h3>6.4 Add Build Step (Execute Shell)</h3>
<p>Click <strong>Add build step → Execute shell</strong> and paste:</p>

<pre>
#!/bin/bash
set -e

echo "===================================="
echo "🚀 CD JOB – Kubernetes Deployment"
echo "===================================="

# Apply Kubernetes manifests
echo "📦 Applying Kubernetes manifests..."
kubectl apply -f k8s/

# Wait for deployment rollout
echo "⏳ Waiting for deployment rollout..."
kubectl rollout status deployment/cloudops-app -n cloudops --timeout=300s

# Verify pods are running
echo "🔍 Checking pod status..."
kubectl get pods -n cloudops

# Get service details
echo "🌐 Service endpoint:"
kubectl get svc cloudops-service -n cloudops

echo "✅ Deployment completed successfully!"
echo "📍 Access app at: http://localhost:30080"
</pre>

<h3>6.5 Save the Job</h3>
<p>Click <strong>Save</strong>.</p>

<hr>

<h2>🌐 7. Setup ngrok for Webhook Access</h2>

<h3>Step 7.1: Install ngrok</h3>
<p>Download from: <code>https://ngrok.com/download</code></p>

<p>Or install via Homebrew:</p>
<pre>
brew install ngrok
</pre>

<h3>Step 7.2: Start ngrok</h3>
<pre>
ngrok http 8080
</pre>

<h3>Step 7.3: Copy Public URL</h3>
<p>ngrok will display a public URL like:</p>
<pre>
https://abc123.ngrok.io
</pre>

<p><strong>Keep this terminal window open!</strong></p>

<hr>

<h2>🔗 8. Configure GitHub Webhook</h2>

<h3>Step 8.1: Go to GitHub Repository Settings</h3>
<ol>
<li>Open your <code>cloudops-automation</code> repository</li>
<li>Click <strong>Settings → Webhooks → Add webhook</strong></li>
</ol>

<h3>Step 8.2: Configure Webhook</h3>
<table border="1">
<tr>
<th>Field</th>
<th>Value</th>
</tr>
<tr>
<td>Payload URL</td>
<td><code>https://abc123.ngrok.io/github-webhook/</code></td>
</tr>
<tr>
<td>Content type</td>
<td><code>application/json</code></td>
</tr>
<tr>
<td>Which events?</td>
<td>Just the push event</td>
</tr>
<tr>
<td>Active</td>
<td>☑ Checked</td>
</tr>
</table>

<p>Click <strong>Add webhook</strong>.</p>

<h3>Step 8.3: Verify Webhook</h3>
<p>After saving, webhook should show <strong>✓</strong> with a green checkmark.</p>

<hr>

<h2>🚀 9. Test CI/CD Pipeline</h2>

<h3>Test 1: Manual Build</h3>
<ol>
<li>Go to Jenkins → <strong>cloudops-ci-build</strong></li>
<li>Click <strong>Build Now</strong></li>
<li>Check Console Output</li>
<li>Verify build success</li>
<li><strong>cloudops-prod-deploy</strong> should trigger automatically</li>
</ol>

<h3>Test 2: Verify Deployment</h3>
<pre>
kubectl get all -n cloudops
</pre>

<p><strong>Expected output:</strong></p>
<pre>
NAME                               READY   STATUS    RESTARTS   AGE
pod/cloudops-app-xxxxxxxxxx-xxxxx  1/1     Running   0          XXs

NAME                       TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
service/cloudops-service   NodePort   10.XX.XXX.XXX   &lt;none&gt;        80:30080/TCP   XXs

NAME                           READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/cloudops-app   3/3     3            3           XXs
</pre>

<h3>Test 3: Access Application</h3>
<p>Open browser:</p>
<pre>
http://localhost:30080
</pre>

<p><strong>Expected:</strong> You should see "CloudOps Sample App" with build number!</p>

<h3>Test 4: Automatic Trigger (Git Push)</h3>
<p>Make a change and push:</p>
<pre>
echo "# CI/CD Test" &gt;&gt; README.md
git add .
git commit -m "Test automatic CI/CD"
git push origin main
</pre>

<p><strong>What happens:</strong></p>
<ol>
<li>GitHub sends webhook to Jenkins (via ngrok)</li>
<li><strong>cloudops-ci-build</strong> triggers automatically</li>
<li>Docker image built and pushed</li>
<li><strong>cloudops-prod-deploy</strong> triggers after CI success</li>
<li>Kubernetes updates pods with new image</li>
<li>Application updated automatically!</li>
</ol>

<hr>

<h2>🏁 10. Completion Checklist</h2>

<table border="1">
<tr>
<th>Step</th>
<th>Status</th>
<th>Verification</th>
</tr>
<tr>
<td>GitHub repository created</td>
<td>✅</td>
<td>Repository visible on GitHub</td>
</tr>
<tr>
<td>Application code pushed</td>
<td>✅</td>
<td>Files visible in repository</td>
</tr>
<tr>
<td>K8s manifests created</td>
<td>✅</td>
<td><code>k8s/</code> folder exists</td>
</tr>
<tr>
<td>CI build job created</td>
<td>✅</td>
<td>Job <strong>cloudops-ci-build</strong> visible</td>
</tr>
<tr>
<td>CD deploy job created</td>
<td>✅</td>
<td>Job <strong>cloudops-prod-deploy</strong> visible</td>
</tr>
<tr>
<td>ngrok running</td>
<td>✅</td>
<td>Public URL active</td>
</tr>
<tr>
<td>GitHub webhook configured</td>
<td>✅</td>
<td>Webhook shows ✓</td>
</tr>
<tr>
<td>Manual build works</td>
<td>✅</td>
<td>Build Now succeeds</td>
</tr>
<tr>
<td>Auto deployment works</td>
<td>✅</td>
<td>CD job triggers after CI</td>
</tr>
<tr>
<td>Application accessible</td>
<td>✅</td>
<td><code>http://localhost:30080</code> works</td>
</tr>
<tr>
<td>Auto trigger on push works</td>
<td>✅</td>
<td>Git push triggers pipeline</td>
</tr>
</table>

<hr>

<h2>🎉 11. Phase-4 Complete</h2>

<p>Congratulations! You now have a complete CI/CD pipeline with:</p>
<ul>
<li>✅ Automated Docker image builds on every commit</li>
<li>✅ Automated Kubernetes deployments</li>
<li>✅ GitHub webhook integration</li>
<li>✅ Zero-downtime rolling updates</li>
<li>✅ Production-ready DevOps workflow</li>
</ul>

<p><strong>Your complete workflow:</strong></p>
<pre>
Code Change → Git Push → GitHub Webhook → Jenkins CI → Docker Hub → Jenkins CD → Kubernetes → Live App
</pre>

<p><strong>Next Steps:</strong></p>
<ul>
<li>Add monitoring with Prometheus & Grafana</li>
<li>Implement autoscaling</li>
<li>Add ingress controller</li>
<li>Set up centralized logging</li>
<li>Add security scanning</li>
</ul>

<hr>

<p><strong>— CloudOps Automation Project | Complete CI/CD Pipeline Ready 🚀</strong></p>

</body>
</html>
