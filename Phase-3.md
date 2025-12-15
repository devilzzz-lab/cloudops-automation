<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>

<h1>🟩 PHASE-3: Complete Development Environment Setup (README.md)</h1>

<p><strong>Version:</strong> Phase 3<br>
<strong>Module:</strong> Docker + Kubernetes + Jenkins Environment Setup<br>
<strong>Project:</strong> CloudOps Automation, CI/CD &amp; Monitoring System</p>

<hr>

<h2>📌 1. Overview</h2>

<p>Phase-3 focuses on setting up a complete local development and CI/CD environment with:</p>
<ul>
<li>Docker Desktop (Container Runtime)</li>
<li>KIND (Kubernetes IN Docker - Local K8s Cluster)</li>
<li>Jenkins (CI/CD Server with all tools installed)</li>
</ul>

<p>This phase ensures:</p>
<ul>
<li>✔ Docker installed and running on macOS</li>
<li>✔ KIND installed on macOS for local Kubernetes</li>
<li>✔ Kubernetes cluster created and verified</li>
<li>✔ Jenkins running with Docker, kubectl, and KIND access</li>
<li>✔ All necessary mounts and network configurations</li>
</ul>

<p><strong>Note:</strong> No CI/CD jobs are created in Phase-3. Job creation happens in Phase-4.</p>

<hr>

<h2>🧩 2. Architecture Overview</h2>

<pre>
macOS (Host Machine)
    |
    ├── Docker Desktop
    |   └── Container Runtime
    |
    ├── KIND (Kubernetes Cluster)
    |   └── cloudops-control-plane
    |
    └── Jenkins Container
        ├── Docker CLI (installed)
        ├── kubectl (installed)
        ├── Access to Docker socket
        ├── Access to KIND cluster
        └── Connected to KIND network
</pre>

<hr>

<h2>🐳 3. Install Docker Desktop on macOS</h2>

<h3>Step 3.1: Download and Install</h3>
<p>Download Docker Desktop from:</p>
<pre>
https://www.docker.com/products/docker-desktop
</pre>

<p>Install and start Docker Desktop.</p>

<h3>Step 3.2: Verify Installation</h3>
<pre>
docker --version
docker ps
</pre>

<p><strong>Expected output:</strong></p>
<pre>
Docker version XX.X.X
</pre>

<hr>

<h2>☸️ 4. Install KIND on macOS</h2>

<h3>Step 4.1: Install KIND using Homebrew</h3>
<pre>
brew install kind
</pre>

<h3>Step 4.2: Verify Installation</h3>
<pre>
kind version
</pre>

<p><strong>Expected output:</strong></p>
<pre>
kind v0.20.0 go1.21.0 darwin/arm64
</pre>

<hr>

<h2>🛰 5. Create Kubernetes Cluster using KIND</h2>

<h3>Step 5.1: Create Cluster</h3>
<pre>
kind create cluster --name cloudops
</pre>

<p><strong>Expected output:</strong></p>
<pre>
Creating cluster "cloudops" ...
 ✓ Ensuring node image
 ✓ Preparing nodes
 ✓ Writing configuration
 ✓ Starting control-plane
 ✓ Installing CNI
 ✓ Installing StorageClass
Set kubectl context to "kind-cloudops"
</pre>

<h3>Step 5.2: Verify Cluster</h3>
<pre>
kubectl cluster-info
</pre>

<p><strong>Expected output:</strong></p>
<pre>
Kubernetes control plane is running at https://127.0.0.1:XXXXX
</pre>

<pre>
kubectl get nodes
</pre>

<p><strong>Expected output:</strong></p>
<pre>
NAME                     STATUS   ROLES           AGE   VERSION
cloudops-control-plane   Ready    control-plane   XXs   vX.XX.X
</pre>

<pre>
kubectl config current-context
</pre>

<p><strong>Expected output:</strong></p>
<pre>
kind-cloudops
</pre>

<hr>

<h2>🏗 6. Jenkins Setup with Complete Integration</h2>

<h3>Step 6.1: Create Jenkins Home Directory</h3>
<pre>
mkdir -p ~/jenkins_home
chmod 700 ~/jenkins_home
</pre>

<h3>Step 6.2: Run Jenkins Container (Complete Setup)</h3>
<pre>
docker run -d \
  --name jenkins \
  --user root \
  --restart=unless-stopped \
  -p 8080:8080 \
  -p 50000:50000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v ~/jenkins_home:/var/jenkins_home \
  -v ~/.kube:/var/jenkins_home/.kube \
  --network kind \
  jenkins/jenkins:lts
</pre>

<p><strong>What each flag does:</strong></p>
<table border="1">
<tr>
<th>Flag</th>
<th>Purpose</th>
</tr>
<tr>
<td><code>--user root</code></td>
<td>Runs Jenkins as root (required for Docker socket access)</td>
</tr>
<tr>
<td><code>-p 8080:8080</code></td>
<td>Exposes Jenkins web UI</td>
</tr>
<tr>
<td><code>-p 50000:50000</code></td>
<td>Jenkins agent communication port</td>
</tr>
<tr>
<td><code>-v /var/run/docker.sock</code></td>
<td>Mounts Docker socket for Docker CLI access</td>
</tr>
<tr>
<td><code>-v ~/jenkins_home</code></td>
<td>Persists Jenkins data and configuration</td>
</tr>
<tr>
<td><code>-v ~/.kube</code></td>
<td>Mounts kubeconfig for Kubernetes access</td>
</tr>
<tr>
<td><code>--network kind</code></td>
<td>Connects Jenkins to KIND Docker network</td>
</tr>
</table>

<h3>Step 6.3: Verify Jenkins is Running</h3>
<pre>
docker ps | grep jenkins
</pre>

<p><strong>Expected:</strong> Jenkins container should be running.</p>

<hr>

<h2>🔨 7. Install Docker CLI Inside Jenkins Container</h2>

<h3>Step 7.1: Enter Jenkins Container</h3>
<pre>
docker exec -u root -it jenkins bash
</pre>

<h3>Step 7.2: Install Docker CLI</h3>
<p>Run the following commands inside the Jenkins container:</p>

<pre>
apt-get update
apt-get install -y docker.io
</pre>

<h3>Step 7.3: Verify Docker Installation</h3>
<pre>
docker --version
</pre>

<p><strong>Expected output:</strong></p>
<pre>
Docker version xx.xx
</pre>

<h3>Step 7.4: Exit Container</h3>
<pre>
exit
</pre>

<hr>

<h2>☸️ 8. Install kubectl Inside Jenkins Container</h2>

<h3>Step 8.1: Enter Jenkins Container</h3>
<pre>
docker exec -u root -it jenkins bash
</pre>

<h3>Step 8.2: Move kubeconfig to kubectl's Default Path</h3>

<p><strong>Option 1 (BEST & SIMPLEST):</strong></p>
<p>Move kubeconfig to kubectl's default path:</p>

<pre>
mkdir -p /root/.kube
cp /var/jenkins_home/.kube/config /root/.kube/config
exit
</pre>

<p>Then test:</p>
<pre>
docker exec -it jenkins kubectl get nodes
</pre>

<p><strong>✅ It will WORK.</strong></p>

<p><strong>Why?</strong></p>
<ul>
<li>kubectl looks for config at <code>/root/.kube/config</code> by default</li>
<li>You mounted <code>~/.kube</code> to <code>/var/jenkins_home/.kube</code></li>
<li>Copying it to <code>/root/.kube/config</code> makes it accessible to kubectl</li>
</ul>

<h3>Step 8.3: Exit Container</h3>
<pre>
exit
</pre>

<hr>

<h2>✅ 9. Final Verification</h2>

<h3>Test 1: Docker Works in Jenkins</h3>
<pre>
docker exec -it jenkins docker ps
</pre>

<p><strong>Expected:</strong> List of running Docker containers.</p>

<h3>Test 2: kubectl Works in Jenkins</h3>
<pre>
docker exec -it jenkins kubectl get nodes
</pre>

<p><strong>Expected output:</strong></p>
<pre>
NAME                     STATUS   ROLES           AGE   VERSION
cloudops-control-plane   Ready    control-plane   XXm   vX.XX.X
</pre>

<h3>Test 3: kubectl get pods Works</h3>
<pre>
docker exec -it jenkins kubectl get pods -A
</pre>

<p><strong>Expected output:</strong></p>
<pre>
NAMESPACE            NAME                                         READY   STATUS    RESTARTS   AGE
kube-system          coredns-xxxxxxxx-xxxxx                      1/1     Running   0          XXm
kube-system          etcd-cloudops-control-plane                 1/1     Running   0          XXm
kube-system          kindnet-xxxxx                               1/1     Running   0          XXm
kube-system          kube-apiserver-cloudops-control-plane       1/1     Running   0          XXm
kube-system          kube-controller-manager-cloudops-control... 1/1     Running   0          XXm
kube-system          kube-proxy-xxxxx                            1/1     Running   0          XXm
kube-system          kube-scheduler-cloudops-control-plane       1/1     Running   0          XXm
local-path-storage   local-path-provisioner-xxxxxxxx-xxxxx       1/1     Running   0          XXm
</pre>

<h3>Test 4: Jenkins Can Access KIND Cluster</h3>
<pre>
docker exec -it jenkins kubectl cluster-info
</pre>

<p><strong>Expected output:</strong></p>
<pre>
Kubernetes control plane is running at https://cloudops-control-plane:6443
</pre>

<p><strong>✅ If all four tests pass, your environment is ready!</strong></p>

<hr>

<h2>🔧 10. Initial Jenkins Configuration</h2>

<h3>Step 10.1: Unlock Jenkins</h3>
<p>Get initial admin password:</p>
<pre>
docker exec -it jenkins cat /var/jenkins_home/secrets/initialAdminPassword
</pre>

<h3>Step 10.2: Access Jenkins UI</h3>
<p>Open in browser:</p>
<pre>
http://localhost:8080
</pre>

<p>Enter the password and click <strong>Install Suggested Plugins</strong>.</p>

<h3>Step 10.3: Create Admin User</h3>
<p>Fill in the admin user details and click <strong>Save and Continue</strong>.</p>

<hr>

<h2>🔌 11. Install Required Jenkins Plugins</h2>

<p>Navigate: <strong>Manage Jenkins → Plugins → Available plugins</strong></p>

<p>Install these plugins:</p>
<ul>
<li>Git</li>
<li>GitHub Integration</li>
<li>GitHub Branch Source</li>
<li>Credentials</li>
<li>Credentials Binding</li>
<li>Pipeline</li>
</ul>

<p>Click <strong>Install</strong> and restart Jenkins if needed.</p>

<hr>

<h2>🔑 12. Configure Jenkins Credentials</h2>

<h3>12.1 GitHub Token (for private repo)</h3>
<p>Navigate: <strong>Manage Jenkins → Credentials → System → Global credentials → Add Credentials</strong></p>

<table border="1">
<tr>
<th>Field</th>
<th>Value</th>
</tr>
<tr>
<td>Kind</td>
<td>Secret text</td>
</tr>
<tr>
<td>Scope</td>
<td>Global</td>
</tr>
<tr>
<td>Secret</td>
<td>Your GitHub Personal Access Token</td>
</tr>
<tr>
<td>ID</td>
<td><strong>github-token</strong></td>
</tr>
<tr>
<td>Description</td>
<td>GitHub Access Token</td>
</tr>
</table>

<h3>12.2 Docker Hub Credentials</h3>
<p>Navigate: <strong>Manage Jenkins → Credentials → System → Global credentials → Add Credentials</strong></p>

<table border="1">
<tr>
<th>Field</th>
<th>Value</th>
</tr>
<tr>
<td>Kind</td>
<td>Username with password</td>
</tr>
<tr>
<td>Scope</td>
<td>Global</td>
</tr>
<tr>
<td>Username</td>
<td>Your Docker Hub Username (e.g., devilzz)</td>
</tr>
<tr>
<td>Password</td>
<td>Your Docker Hub Password or Access Token</td>
</tr>
<tr>
<td>ID</td>
<td><strong>dockerhub-creds</strong></td>
</tr>
<tr>
<td>Description</td>
<td>Docker Hub Credentials</td>
</tr>
</table>

<hr>

<h2>🏁 13. Completion Checklist</h2>

<table border="1">
<tr>
<th>Component</th>
<th>Status</th>
<th>Verification</th>
</tr>
<tr>
<td>Docker Desktop installed</td>
<td>✅</td>
<td><code>docker --version</code></td>
</tr>
<tr>
<td>KIND installed</td>
<td>✅</td>
<td><code>kind version</code></td>
</tr>
<tr>
<td>KIND cluster created</td>
<td>✅</td>
<td><code>kind get clusters</code></td>
</tr>
<tr>
<td>Kubernetes cluster running</td>
<td>✅</td>
<td><code>kubectl get nodes</code></td>
</tr>
<tr>
<td>Jenkins container running</td>
<td>✅</td>
<td><code>docker ps | grep jenkins</code></td>
</tr>
<tr>
<td>Docker CLI in Jenkins</td>
<td>✅</td>
<td><code>docker exec jenkins docker --version</code></td>
</tr>
<tr>
<td>kubectl in Jenkins</td>
<td>✅</td>
<td><code>docker exec jenkins kubectl version</code></td>
</tr>
<tr>
<td>Jenkins can access KIND</td>
<td>✅</td>
<td><code>docker exec jenkins kubectl get nodes</code></td>
</tr>
<tr>
<td>Jenkins can list pods</td>
<td>✅</td>
<td><code>docker exec jenkins kubectl get pods -A</code></td>
</tr>
<tr>
<td>Jenkins UI accessible</td>
<td>✅</td>
<td><code>http://localhost:8080</code></td>
</tr>
<tr>
<td>Jenkins plugins installed</td>
<td>✅</td>
<td>Manage Jenkins → Plugins</td>
</tr>
<tr>
<td>GitHub credentials configured</td>
<td>✅</td>
<td>Credentials page</td>
</tr>
<tr>
<td>Docker Hub credentials configured</td>
<td>✅</td>
<td>Credentials page</td>
</tr>
</table>

<hr>

<h2>🎯 14. What's Next?</h2>

<p>Phase-3 is complete! You now have a fully configured development environment with:</p>
<ul>
<li>✅ Docker Desktop for container runtime</li>
<li>✅ KIND cluster for local Kubernetes</li>
<li>✅ Jenkins with Docker and kubectl installed</li>
<li>✅ All necessary network and volume mounts</li>
<li>✅ Credentials configured for GitHub and Docker Hub</li>
</ul>

<p><strong>In Phase-4, you will:</strong></p>
<ul>
<li>Create GitHub repository with application code</li>
<li>Create Kubernetes manifests</li>
<li>Create CI build job (<strong>cloudops-ci-build</strong>)</li>
<li>Create CD deployment job (<strong>cloudops-prod-deploy</strong>)</li>
<li>Configure ngrok for webhook access</li>
<li>Set up GitHub webhooks</li>
<li>Test complete CI/CD automation</li>
</ul>

<hr>

<h2>🎉 Phase-3 Complete</h2>
<p>Your complete development environment is ready! All tools are installed, configured, and verified.</p>

<p><strong>Next:</strong> Move to <strong>Phase-4</strong> for CI/CD pipeline creation.</p>

</body>
</html>
