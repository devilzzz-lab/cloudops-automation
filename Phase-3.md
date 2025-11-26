<html lang="en">
<head>
  <meta charset="utf-8" />
</head>
<body>

<h1>🟩 PHASE-3 CloudOps Automation: CI/CD Pipeline (Jenkins + GitHub + Docker) (README.md)</h1>

<p><strong>Version:</strong> Phase 3<br/>
<strong>Module:</strong> CI/CD &amp; Container Build Automation<br/>
<strong>Project:</strong> CloudOps Automation, CI/CD &amp; Monitoring System</p>

<hr/>

<h2>📌 1. Overview</h2>
<p>Phase-3 focuses on building a complete CI/CD pipeline for the CloudOps Automation System using:</p>
<ul>
  <li>Jenkins (CI Orchestrator)</li>
  <li>GitHub (Source Repository)</li>
  <li>Docker (Containerization)</li>
  <li>Docker Hub (Container Registry)</li>
  <li>Webhooks (Trigger Builds Automatically)</li>
</ul>

<p>This pipeline ensures:</p>
<ul>
  <li>✔ Every GitHub commit triggers Jenkins automatically</li>
  <li>✔ Jenkins builds the application</li>
  <li>✔ Jenkins builds &amp; pushes Docker images to Docker Hub</li>
  <li>✔ Automated Deployment stage (local for Phase-3)</li>
  <li>✔ Full build → test → containerize → push sequence</li>
</ul>

<hr/>

<h2>🧩 2. Architecture Diagram</h2>

<pre>
Developer (Local Machine)
            |
            |  git push
            v
      GitHub Repository
            |
            |  Webhook (push event)
            v
          Jenkins
  --------------------------------------------
| Checkout | Build | Test | Docker Build | Push |
  --------------------------------------------
            |
            v
        Docker Hub
            |
            |  (Optional Deploy)
            v
      Deployment Target (Local/K8s-Phase4)
</pre>

<hr/>

<h2>🏗 3. Jenkins Setup (Docker-Based Installation)</h2>

<h3>3.1 Start Jenkins in Docker</h3>
<p>Create Jenkins home directory:</p>
<pre>
mkdir -p ~/jenkins_home
chmod 700 ~/jenkins_home
</pre>

<p>Run Jenkins container:</p>
<pre>
docker run -d --name jenkins -u 0 \
  --restart=unless-stopped \
  -p 8080:8080 -p 50000:50000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v ~/jenkins_home:/var/jenkins_home \
  jenkins/jenkins:lts
</pre>

<p>Unlock Jenkins:</p>
<pre>
docker exec -it jenkins cat /var/jenkins_home/secrets/initialAdminPassword
</pre>

<p>Open in browser:</p>
<p>http://localhost:8080</p>
<p>Install Suggested Plugins.</p>

<hr/>

<h2>🔌 4. Required Plugins</h2>
<p>Install these plugins:</p>
<ul>
  <li>Git</li>
  <li>GitHub Integration</li>
  <li>GitHub Branch Source</li>
  <li>Credentials</li>
  <li>Credentials Binding</li>
  <li>Docker Pipeline (optional)</li>
  <li>Pipeline</li>
  <li>Blue Ocean (optional UI)</li>
</ul>

<hr/>

<h2>🔑 5. Configure Jenkins Credentials</h2>

<h3>5.1 GitHub Token (for private repo)</h3>
<p>Navigate: Manage Jenkins → Credentials → System → Global → Add Credentials</p>
<ul>
  <li>Kind: Secret text</li>
  <li>Secret: &lt;your GitHub PAT&gt;</li>
  <li>ID: <strong>github-token</strong></li>
</ul>

<h3>5.2 Docker Hub Credentials</h3>
<ul>
  <li>Kind: Username with password</li>
  <li>Username: DockerHub Username</li>
  <li>Password: DockerHub Password or PAT</li>
  <li>ID: <strong>dockerhub-creds</strong></li>
</ul>

<hr/>

<h2>🐳 6. Project Repository Setup</h2>

<p>Repo Structure:</p>
<pre>
cloudops-automation/
 ├── app.py
 ├── requirements.txt
 ├── Dockerfile
 ├── Jenkinsfile
 ├── README.md
 ├── Phase-1.md
 ├── Phase-2.md
 ├── Phase-3.md
 ├── .dockerignore
 └── tests/   (optional)
</pre>

<p>Sample <code>app.py</code>:</p>
<pre>
```python
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
```
</pre>

<p><strong>requirements.txt</strong></p>
<pre>
Flask==3.0.0
</pre>

<p><strong>Dockerfile</strong></p>
<pre>
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["python","app.py"]
</pre>

<hr/>

<h2>🟦 7. Jenkins Freestyle Job Setup (Manual UI Method)</h2>

<h3>7.1 Create Job</h3>
<ol>
  <li>Jenkins Dashboard → New Item</li>
  <li>Select Freestyle Project</li>
  <li>Name: <strong>cloudops-sample-app-job</strong></li>
</ol>

<h3>7.2 Configure Source Code Management</h3>
<p>Under Source Code Management → Git:</p>
<ul>
  <li>Repository URL: <code>https://github.com/&lt;username&gt;/cloudops-automation.git</code></li>
  <li>Credentials: <strong>github-token</strong></li>
  <li>Branch: <code>*/main</code></li>
</ul>

<h3>7.3 Build Triggers</h3>
<p>Enable:</p>
<ul>
  <li>GitHub hook trigger for GITScm polling</li>
</ul>

<h3>7.4 Build Environment</h3>
<p>Enable <em>Use secret text(s) or file(s)</em>. Add:</p>
<ul>
  <li>Credentials: <strong>dockerhub-creds</strong></li>
  <li>Username Variable: <code>DOCKER_USER</code></li>
  <li>Password Variable: <code>DOCKER_PASS</code></li>
</ul>

<h3>7.5 Build Step (Execute Shell)</h3>
<pre>
#!/bin/bash
set -e

REGISTRY="docker-hub-username"
IMAGE="cloudops-sample-app"
TAG="build-${BUILD_NUMBER}"

echo "Building Docker image ${REGISTRY}/${IMAGE}:${TAG}"

docker build -t ${REGISTRY}/${IMAGE}:${TAG} .

echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin

docker push ${REGISTRY}/${IMAGE}:${TAG}

docker tag ${REGISTRY}/${IMAGE}:${TAG} ${REGISTRY}/${IMAGE}:latest || true
docker push ${REGISTRY}/${IMAGE}:latest || true

echo "DONE: Image pushed to Docker Hub."
</pre>

<p>Click Save.</p>

<hr/>

<h2>🌐 8. Configure GitHub Webhook (Push Trigger)</h2>

<p>If Jenkins is local:</p>
<pre>
ngrok http 8080
</pre>

<p>Copy ngrok public URL:</p>
<p><code>https://&lt;subdomain&gt;.ngrok.io</code></p>

<p>Go to GitHub Repo → Settings → Webhooks → Add Webhook</p>
<ul>
  <li>Payload URL: <code>https://&lt;ngrok-url&gt;/github-webhook/</code></li>
  <li>Content Type: <code>application/json</code></li>
  <li>Event: Just the push event</li>
</ul>

<p>Webhook should show ✓ 200 OK after you push code.</p>

<hr/>

<h2>🚀 9. Verification Steps</h2>

<ol>
  <li>Push a commit:
    <pre>git commit --allow-empty -m "CI/CD Test"
git push origin main</pre>
  </li>

  <li>Jenkins should trigger automatically. Console Output should show:
    <ul>
      <li>Git checkout ✔</li>
      <li>Docker build ✔</li>
      <li>Docker push ✔</li>
      <li>Build SUCCESS ✔</li>
    </ul>
  </li>

  <li>Verify images on Docker Hub:
    <p>https://hub.docker.com/r/doccker-hub-username/cloudops-sample-app</p>
  </li>

  <li>Pull &amp; run container locally:
    <pre>docker pull devilzz/cloudops-sample-app:latest
docker run -p 9090:8080 devilzz/cloudops-sample-app:latest</pre>
    <p>Open: <a href="http://localhost:9090">http://localhost:9090</a> — You should see your app running.</p>
  </li>
</ol>

<hr/>

<h2>🏁 10. Completion Checklist</h2>

<ul>
  <li>Jenkins server setup — ✅ Done — http://localhost:8080</li>
  <li>Install plugins — ✅ Done — Manage Plugins</li>
  <li>Configure Docker socket — ✅ Done — docker --version inside container</li>
  <li>GitHub repo created — ✅ Done — Repo visible</li>
  <li>Dockerfile added — ✅ Done — File exists</li>
  <li>Jenkins connected to GitHub — ✅ Done — Webhook 200</li>
  <li>DockerHub credentials configured — ✅ Done — dockerhub-creds visible</li>
  <li>Jenkins job created — ✅ Done — Job visible</li>
  <li>Jenkins builds on push — ✅ Done — Auto-trigger success</li>
  <li>Docker image built — ✅ Done — Build logs</li>
  <li>Docker image pushed — ✅ Done — Docker Hub tags visible</li>
  <li>App deployable — ✅ Done — docker run works</li>
</ul>

<hr/>

<h2>🎉 Phase-3 Complete</h2>
<p>Your CI/CD pipeline is fully automated &amp; operational. You now have a production-style build system exactly like real DevOps workflows.</p>

</body>
</html>
