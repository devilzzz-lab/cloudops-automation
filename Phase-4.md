<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>

<h1>🟧 PHASE 4 – Kubernetes Deployment using KIND</h1>

<p><strong>Version:</strong> Phase 4<br>
<strong>Module:</strong> Kubernetes Deployment & Local Orchestration<br>
<strong>Project:</strong> CloudOps Automation, CI/CD & Monitoring System</p>

<p>
This phase focuses on deploying the Dockerized CloudOps application to a local
Kubernetes cluster created using <strong>KIND (Kubernetes IN Docker)</strong>, with automated
build and deployment handled by Jenkins.
</p>

<hr>

<h2>📌 1. Phase Overview</h2>

<ul>
  <li>Create and manage a Kubernetes cluster using KIND</li>
  <li>Deploy application workloads using Kubernetes manifests</li>
  <li>Configure Jenkins to build Docker images and deploy to Kubernetes</li>
  <li>Trigger deployments automatically from GitHub</li>
</ul>

<hr>

<h2>🧰 2. Install KIND on macOS</h2>

<p>KIND is installed on macOS using Homebrew.</p>

<h3>Step 2.1: Install KIND</h3>

<pre><code>
brew install kind
</code></pre>

<h3>Step 2.2: Verify Installation</h3>

<pre><code>
kind version
</code></pre>

<p><strong>Expected:</strong> KIND version is displayed successfully.</p>

<hr>

<h2>🛰 3. Create Kubernetes Cluster using KIND</h2>

<h3>Step 3.1: Create the Cluster</h3>

<pre><code>
kind create cluster --name cloudops
</code></pre>

<h3>Step 3.2: Verify Cluster</h3>

<pre><code>
kubectl cluster-info
kubectl get nodes
kubectl config current-context
</code></pre>

<p><strong>Expected:</strong></p>
<pre>
Context: kind-cloudops
Node: cloudops-control-plane (Ready)
</pre>

<hr>

<h2>🧩 4. Architecture Flow</h2>

<pre>
Developer → GitHub → Jenkins → Docker Hub → KIND Kubernetes
</pre>

<ul>
  <li><strong>cloudops-ci-build:</strong> Docker build & push</li>
  <li><strong>cloudops-prod-deploy:</strong> Kubernetes deployment</li>
</ul>

<hr>

<h2>🔄 5. Jenkins Integration with KIND</h2>

<ul>
  <li>Jenkins runs as <strong>root</strong> inside Docker</li>
  <li>Docker socket is mounted</li>
  <li>kubectl is installed inside Jenkins</li>
  <li>KIND internal kubeconfig is used</li>
</ul>

<hr>

<h2>🔧 6. Run Jenkins Container</h2>

<pre><code>
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
</code></pre>

<p>Jenkins UI will be available at:</p>
<pre><code>http://localhost:8080</code></pre>

<hr>

<h2>🌐 7. Expose Jenkins using ngrok</h2>

<p>
To receive GitHub webhook events on a local machine, Jenkins must be exposed
to the internet using ngrok.
</p>

<h3>Step 7.1: Start ngrok</h3>

<pre><code>
ngrok http 8080
</code></pre>

<h3>Step 7.2: Copy Public URL</h3>

<p>
ngrok will generate a public HTTPS URL similar to:
</p>

<pre>
https://abcd1234.ngrok.io
</pre>

<p>
Copy this URL and append <code>/github-webhook/</code>
</p>

<pre>
https://abcd1234.ngrok.io/github-webhook/
</pre>

<hr>

<h2>🔗 8. Configure GitHub Webhook</h2>

<h3>Step 8.1: GitHub Webhook Setup</h3>

<ol>
  <li>Go to GitHub repository → <strong>Settings</strong></li>
  <li>Open <strong>Webhooks</strong> → Add webhook</li>
  <li>Payload URL: <code>ngrok-URL/github-webhook/</code></li>
  <li>Content type: <strong>application/json</strong></li>
  <li>Select event: <strong>Just the push event</strong></li>
  <li>Save webhook</li>
</ol>

<p>
Once configured, GitHub will send events to Jenkins automatically.
</p>

<hr>

<h2>⚙️ 9. Jenkins Job Creation (To Be Added)</h2>

<p><strong>🚧 This section will be documented later.</strong></p>

<hr>

<h2>🚀 10. Git Push → Jenkins Auto Trigger Flow</h2>

<p>
After webhook configuration, the CI/CD flow becomes fully automated.
</p>

<h3>Developer Workflow</h3>

<pre><code>
git add .
git commit -m "your commit message"
git push
</code></pre>

<h3>What Happens Automatically</h3>
<ul>
  <li>GitHub sends webhook event</li>
  <li>Jenkins CI job triggers automatically</li>
  <li>Docker image is built and pushed</li>
  <li>Kubernetes deployment job runs</li>
  <li>Application is updated in KIND cluster</li>
</ul>

<hr>

<h2>🎉 11. Phase 4 Completion Summary</h2>

<ul>
  <li>✔ KIND installed and cluster created</li>
  <li>✔ Jenkins exposed via ngrok</li>
  <li>✔ GitHub webhook triggers Jenkins automatically</li>
  <li>✔ CI/CD pipeline deploys to Kubernetes</li>
</ul>

<hr>

<p><strong>— CloudOps Automation Project</strong></p>

</body>
</html>
