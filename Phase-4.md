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

<p>In this phase, the following objectives are achieved:</p>
<ul>
  <li>Create and manage a Kubernetes cluster using KIND</li>
  <li>Deploy application workloads using Kubernetes manifests</li>
  <li>Configure Jenkins to build Docker images and deploy to Kubernetes</li>
  <li>Validate application access using NodePort or port-forwarding</li>
</ul>

<hr>

<h2>🧩 2. Architecture Flow</h2>

<pre>
Developer → GitHub → Jenkins (CI/CD) → Docker Hub → KIND Kubernetes
</pre>

<ul>
  <li><strong>Job 1:</strong> cloudops-ci-build → Docker build & push</li>
  <li><strong>Job 2:</strong> cloudops-prod-deploy → Kubernetes deployment</li>
</ul>

<hr>

<h2>🛰 3. Create Kubernetes Cluster using KIND</h2>

<h3>Step 3.1: Create the KIND Cluster</h3>

<p>This command creates a single-node Kubernetes cluster inside Docker.</p>

<pre><code>
kind create cluster --name cloudops
</code></pre>

<hr>

<h3>Step 3.2: Verify Cluster Status</h3>

<p>Confirm that Kubernetes is running and accessible.</p>

<pre><code>
kubectl cluster-info
kubectl get nodes
kubectl config current-context
</code></pre>

<p><strong>Expected Result:</strong></p>
<pre>
Context: kind-cloudops
Node: cloudops-control-plane (Ready)
</pre>

<hr>

<h2>🧰 4. Kubernetes Manifests Structure</h2>

<p>All Kubernetes configuration files are maintained inside a dedicated <code>k8s/</code> directory.</p>

<pre>
cloudops-automation/
└── k8s/
    ├── namespace.yaml
    ├── deployment.yaml
    ├── service.yaml
    ├── configmap.yaml
    ├── secret.yaml
    ├── pvc.yaml
    ├── statefulset-db.yaml
    └── daemonset-logs.yaml
</pre>

<p>
This structure ensures version control, consistency, and reusability across environments.
</p>

<hr>

<h2>🔄 5. Jenkins Integration with KIND</h2>

<p>
Jenkins is executed as a Docker container and is responsible for both
Docker image creation and Kubernetes deployment.
</p>

<h3>Key Design Decisions</h3>
<ul>
  <li>Jenkins runs as <strong>root</strong> (required for Docker socket access on macOS)</li>
  <li>Docker socket is mounted inside Jenkins</li>
  <li>kubectl is installed inside Jenkins container</li>
  <li>KIND internal kubeconfig is used for cluster access</li>
</ul>

<hr>

<h2>🔧 6. Run Jenkins Container</h2>

<p>
The following command starts Jenkins with all required permissions and network access.
</p>

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

<p>
This allows Jenkins to:
</p>
<ul>
  <li>Build Docker images</li>
  <li>Push images to Docker Hub</li>
  <li>Communicate with the KIND Kubernetes cluster</li>
</ul>

<hr>

<h2>🔧 7. Install Docker and kubectl inside Jenkins</h2>

<h3>Step 7.1: Enter Jenkins Container</h3>

<pre><code>
docker exec -u root -it jenkins bash
</code></pre>

<h3>Step 7.2: Install Required Tools</h3>

<pre><code>
apt-get update
apt-get install -y docker.io curl
</code></pre>

<p>Install kubectl:</p>

<pre><code>
curl -LO https://dl.k8s.io/release/$(curl -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl
chmod +x kubectl
mv kubectl /usr/local/bin/
</code></pre>

<p>Exit the container:</p>

<pre><code>
exit
</code></pre>

<hr>

<h2>🔐 8. Configure KIND Internal Kubeconfig</h2>

<h3>Step 8.1: Generate Internal Kubeconfig (on Host)</h3>

<p>
This kubeconfig uses Docker DNS and is required for containers to access KIND.
</p>

<pre><code>
kind get kubeconfig --name cloudops --internal > /tmp/kind-internal-config
</code></pre>

<hr>

<h3>Step 8.2: Copy Kubeconfig into Jenkins</h3>

<pre><code>
docker cp /tmp/kind-internal-config jenkins:/var/jenkins_home/.kube/config
</code></pre>

<hr>

<h3>Step 8.3: Move Kubeconfig to Default kubectl Path</h3>

<p>
Placing kubeconfig in the default path ensures kubectl works in
non-interactive Jenkins jobs.
</p>

<pre><code>
docker exec -u root -it jenkins bash
mkdir -p /root/.kube
cp /var/jenkins_home/.kube/config /root/.kube/config
exit
</code></pre>

<hr>

<h2>✅ 9. Final Verification</h2>

<h3>Verify Docker Access</h3>

<pre><code>
docker exec -it jenkins docker ps
</code></pre>

<h3>Verify Kubernetes Access</h3>

<pre><code>
docker exec -it jenkins kubectl get nodes
</code></pre>

<p><strong>Expected Output:</strong></p>

<pre>
cloudops-control-plane   Ready
</pre>

<hr>

<h2>🎉 10. Phase 4 Completion Summary</h2>

<ul>
  <li>✔ KIND Kubernetes cluster created and verified</li>
  <li>✔ Jenkins integrated with Docker and Kubernetes</li>
  <li>✔ Automated Docker build and push pipeline</li>
  <li>✔ Automated Kubernetes deployment from Jenkins</li>
</ul>

<hr>

<h2>🧠 Interview-Ready Explanation</h2>

<blockquote>
Jenkins runs as a Docker container and deploys applications to a KIND Kubernetes
cluster using an internal kubeconfig. Docker builds, image pushes, and Kubernetes
rollouts are fully automated through CI/CD jobs.
</blockquote>

<hr>

<p><strong>— CloudOps Automation Project</strong></p>

</body>
</html>
