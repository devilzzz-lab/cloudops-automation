<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>

<h1>🟩 PHASE-3 CloudOps Automation: CI/CD Pipeline (Jenkins + GitHub + Docker) (README.md)</h1>

<p><strong>Version:</strong> Phase 3<br>
<strong>Module:</strong> CI/CD &amp; Container Build Automation<br>
<strong>Project:</strong> CloudOps Automation, CI/CD &amp; Monitoring System</p>

<hr>

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

<hr>

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

<hr>

<h2>🏗 3. Jenkins Setup (Docker-Based Installation)</h2>

<h3>3.1 Start Jenkins in Docker</h3>
<p>Create Jenkins home directory:</p>
<pre>
mkdir -p ~/jenkins_home
chmod 700 ~/jenkins_home
</pre>

<p>Run Jenkins container:</p>
<pre>
docker run -d \
  --name jenkins \
  --user root \
  -p 8080:8080 \
  -p 50000:50000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v ~/jenkins_home:/var/jenkins_home \
  -v ~/.kube:/var/jenkins_home/.kube \
  --network kind \
  jenkins/jenkins:lts
</pre>

<p>Unlock Jenkins:</p>
<pre>
docker exec -it jenkins cat /var/jenkins_home/secrets/initialAdminPassword
</pre>

<p>Open in browser:</p>
<p><a href="http://localhost:8080">http://localhost:8080</a></p>
<p>Install Suggested Plugins.</p>

<p><strong>Jenkins Environment Screenshot:</strong></p>
<img src="screenshots/jenkins-job-environment.png" alt="Jenkins Job Environment">

<hr>

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

<hr>

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

<hr>

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


<p><strong>requirements.txt</strong></p>
<pre>
Flask==3.0.0
</pre>

<p><strong>Dockerfile</strong></p>

<hr>

<h2>🟦 7. Jenkins Freestyle Job Setup (Manual UI Method)</h2>

<h3>7.1 Create Job</h3>
<ol>
  <li>Jenkins Dashboard → New Item</li>
  <li>Select Freestyle Project</li>
  <li>Name: <strong>cloudops-ci-build</strong></li>
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

</pre>

<p><strong>Execute Shell Screenshot:</strong></p>
<img src="screenshots/jenkins-execute-shell.png" alt="Jenkins Execute Shell">

<p><strong>Console Output Screenshot (build logs):</strong></p>
<img src="screenshots/jenkins-console-output.png" alt="Jenkins Console Output">

<p><strong>Job Success Screenshot:</strong></p>
<img src="screenshots/jenkins-job-success.png" alt="Jenkins Job Success">

<hr>

<h2>🌐 8. Configure GitHub Webhook (Push Trigger)</h2>

<p>If Jenkins is local:</p>
<pre>
ngrok http 8080
</pre>

<p>Copy ngrok public URL (example):</p>
<p><code>https://&lt;subdomain&gt;.ngrok.io</code></p>

<p><strong>ngrok Public URL Screenshot:</strong></p>
<img src="screenshots/ngrok-success.png" alt="ngrok Success">

<p>Go to GitHub Repo → Settings → Webhooks → Add Webhook</p>
<ul>
  <li>Payload URL: <code>https://&lt;ngrok-url&gt;/github-webhook/</code></li>
  <li>Content Type: <code>application/json</code></li>
  <li>Event: Just the push event</li>
</ul>

<p><strong>Webhooks Success Screenshot:</strong></p>
<img src="screenshots/webhooks-success.png" alt="Webhooks Success">


<p>Webhook should show ✓ 200 OK after you push code.</p>

<hr>

<h2>🚀 9. Verification Steps</h2>

<ol>
  <li>
    <p>Push a commit:</p>
    <pre>
git commit --allow-empty -m "CI/CD Test"
git push origin main
    </pre>
  </li>

  <li>
    <p>Jenkins should trigger automatically. Console Output should show:</p>
    <ul>
      <li>Git checkout ✔</li>
      <li>Docker build ✔</li>
      <li>Docker push ✔</li>
      <li>Build SUCCESS ✔</li>
    </ul>
  </li>

  <li>
    <p>Verify images on Docker Hub:</p>
    <p><a href="https://hub.docker.com/r/docker-hub-username/cloudops-sample-app">https://hub.docker.com/r/docker-hub-username/cloudops-sample-app</a></p>
  </li>

  <li>
    <p>Pull &amp; run container locally:</p>
    <pre>
docker pull devilzz/cloudops-sample-app:latest
docker run -p 9090:8080 devilzz/cloudops-sample-app:latest
    </pre>
    <p>Open: <a href="http://localhost:9090">http://localhost:9090</a> — You should see your app running.</p>
  </li>
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
    <td>Jenkins server setup</td>
    <td>✅ Done</td>
    <td>http://localhost:8080</td>
  </tr>
  <tr>
    <td>Install plugins</td>
    <td>✅ Done</td>
    <td>Manage Plugins</td>
  </tr>
  <tr>
    <td>Configure Docker socket</td>
    <td>✅ Done</td>
    <td>docker --version inside container</td>
  </tr>
  <tr>
    <td>GitHub repo created</td>
    <td>✅ Done</td>
    <td>Repo visible</td>
  </tr>
  <tr>
    <td>Dockerfile added</td>
    <td>✅ Done</td>
    <td>File exists</td>
  </tr>
  <tr>
    <td>Jenkins connected to GitHub</td>
    <td>✅ Done</td>
    <td>Webhook 200</td>
  </tr>
  <tr>
    <td>DockerHub credentials configured</td>
    <td>✅ Done</td>
    <td>dockerhub-creds visible</td>
  </tr>
  <tr>
    <td>Jenkins job created</td>
    <td>✅ Done</td>
    <td>Job visible</td>
  </tr>
  <tr>
    <td>Jenkins builds on push</td>
    <td>✅ Done</td>
    <td>Auto-trigger success</td>
  </tr>
  <tr>
    <td>Docker image built</td>
    <td>✅ Done</td>
    <td>Build logs</td>
  </tr>
  <tr>
    <td>Docker image pushed</td>
    <td>✅ Done</td>
    <td>Docker Hub tags visible</td>
  </tr>
  <tr>
    <td>App deployable</td>
    <td>✅ Done</td>
    <td>docker run works</td>
  </tr>
</table>

<hr>

<h2>🎉 Phase-3 Complete</h2>
<p>Your CI/CD pipeline is fully automated &amp; operational. You now have a production-style build system exactly like real DevOps workflows.</p>

</body>
</html>
