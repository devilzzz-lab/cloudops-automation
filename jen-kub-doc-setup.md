<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>

<h1>✅ Jenkins + Docker + kubectl + KIND Complete Setup (macOS) (README.md)</h1>

<p><strong>Version:</strong> Production-Ready CI/CD<br>
<strong>Module:</strong> Jenkins Setup & Configuration<br>
<strong>Project:</strong> CloudOps Automation, CI/CD &amp; Monitoring System</p>

<hr>

<h2>📌 1. Overview</h2>
<p>This guide provides the complete, production-style setup for Jenkins on macOS with Docker and Kubernetes (KIND) integration. This setup ensures seamless CI/CD operations without configuration hacks or workarounds.</p>

<p>This setup ensures:</p>
<ul>
  <li>✔ Jenkins runs as root (required for macOS Docker socket access)</li>
  <li>✔ Docker CLI works inside Jenkins</li>
  <li>✔ kubectl works inside Jenkins</li>
  <li>✔ kubeconfig is in default path</li>
  <li>✔ <code>docker exec jenkins kubectl get nodes</code> works</li>
  <li>✔ CI + CD jobs work without hacks</li>
</ul>

<hr>

<h2>🧱 2. Prerequisites (On Mac)</h2>

<p>Make sure these already work on your Mac:</p>

<table border="1">
  <tr>
    <th>Tool</th>
    <th>Verification Command</th>
  </tr>
  <tr>
    <td>Docker</td>
    <td><code>docker --version</code></td>
  </tr>
  <tr>
    <td>kubectl</td>
    <td><code>kubectl version --client</code></td>
  </tr>
  <tr>
    <td>KIND</td>
    <td><code>kind version</code></td>
  </tr>
</table>

<h3>Verify KIND Cluster Exists</h3>
<pre>
kind get clusters
</pre>

<p><strong>Expected output:</strong></p>
<pre>
cloudops
</pre>

<p>If no cluster exists, create one:</p>
<pre>
kind create cluster --name cloudops
</pre>

<hr>

<h2>🟦 3. STEP 1: Delete Old Jenkins (Important)</h2>

<p>Clean up any existing Jenkins container to avoid conflicts:</p>

<pre>
docker stop jenkins || true
docker rm jenkins || true
</pre>

<h3>Optional: Clean Jenkins Home (Fresh Start)</h3>
<pre>
rm -rf ~/jenkins_home
</pre>

<p><strong>⚠️ Warning:</strong> This deletes all Jenkins data, jobs, and configurations.</p>

<hr>

<h2>🟦 4. STEP 2: Run Jenkins as Root (Correct Way for macOS)</h2>

<p><strong>👉 This is REQUIRED on macOS</strong> because <code>docker.sock</code> is owned by <code>root:root</code></p>

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

<h3>What This Does:</h3>

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
    <td>Jenkins agent port</td>
  </tr>
  <tr>
    <td><code>-v /var/run/docker.sock</code></td>
    <td>Mounts Docker socket for Docker CLI access</td>
  </tr>
  <tr>
    <td><code>-v ~/jenkins_home</code></td>
    <td>Persists Jenkins data</td>
  </tr>
  <tr>
    <td><code>-v ~/.kube</code></td>
    <td>Shares kubeconfig with Jenkins</td>
  </tr>
  <tr>
    <td><code>--network kind</code></td>
    <td>Connects Jenkins to KIND network</td>
  </tr>
</table>

<h3>✅ Jenkins Now:</h3>
<ul>
  <li>Runs as root</li>
  <li>Can access Docker socket</li>
  <li>Can access KIND network</li>
</ul>

<hr>

<h2>🟦 5. STEP 3: Install Docker CLI Inside Jenkins</h2>

<p>Enter Jenkins container as root:</p>
<pre>
docker exec -u root -it jenkins bash
</pre>

<p>Inside container, run:</p>
<pre>
apt-get update
apt-get install -y docker.io curl
docker --version
</pre>

<p><strong>Expected output:</strong></p>
<pre>
Docker version XX.X.X
</pre>

<p>Exit container:</p>
<pre>
exit
</pre>

<hr>

<h2>🟦 6. STEP 4: Install kubectl Inside Jenkins</h2>

<p>Enter Jenkins container as root:</p>
<pre>
docker exec -u root -it jenkins bash
</pre>

<p>Inside container, run:</p>
<pre>
curl -LO https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl
chmod +x kubectl
mv kubectl /usr/local/bin/
kubectl version --client
</pre>

<p><strong>Expected output:</strong></p>
<pre>
Client Version: vX.XX.X
</pre>

<p>Exit container:</p>
<pre>
exit
</pre>

<hr>

<h2>🟦 7. STEP 5: Create Internal Kubeconfig (On Mac)</h2>

<p><strong>⚠️ This is VERY IMPORTANT</strong></p>

<p>KIND clusters have two kubeconfig types:</p>
<ul>
  <li><strong>External:</strong> Uses <code>localhost</code> (for host machine)</li>
  <li><strong>Internal:</strong> Uses Docker DNS (for containers)</li>
</ul>

<p>Generate internal kubeconfig:</p>
<pre>
kind get kubeconfig --name cloudops --internal &gt; /tmp/kind-internal-config
</pre>

<p>Verify the file:</p>
<pre>
cat /tmp/kind-internal-config | grep server
</pre>

<p><strong>Expected output (shows Docker internal DNS):</strong></p>
<pre>
server: https://cloudops-control-plane:6443
</pre>

<hr>

<h2>🟦 8. STEP 6: Copy Kubeconfig Into Jenkins</h2>

<p>Copy the internal kubeconfig into Jenkins container:</p>
<pre>
docker cp /tmp/kind-internal-config jenkins:/var/jenkins_home/.kube/config
</pre>

<p>Verify the copy:</p>
<pre>
docker exec -it jenkins ls -l /var/jenkins_home/.kube/config
</pre>

<hr>

<h2>🟦 9. STEP 7: Move Kubeconfig to Default kubectl Path (🔥 MOST IMPORTANT 🔥)</h2>

<p><strong>👉 This avoids <code>export KUBECONFIG</code> issues forever.</strong></p>

<p>Enter Jenkins container as root:</p>
<pre>
docker exec -u root -it jenkins bash
</pre>

<p>Inside container, run:</p>
<pre>
mkdir -p /root/.kube
cp /var/jenkins_home/.kube/config /root/.kube/config
chmod 600 /root/.kube/config
ls -l /root/.kube/config
</pre>

<p><strong>Expected output:</strong></p>
<pre>
-rw------- 1 root root XXXX /root/.kube/config
</pre>

<p>Exit container:</p>
<pre>
exit
</pre>

<h3>Why This Step is Critical:</h3>
<ul>
  <li>kubectl automatically looks for config at <code>/root/.kube/config</code></li>
  <li>No need for <code>KUBECONFIG</code> environment variable</li>
  <li>Works in non-interactive Jenkins jobs</li>
  <li>Production-standard configuration</li>
</ul>

<hr>

<h2>🟦 10. STEP 8: Final Verification (THIS MUST WORK)</h2>

<h3>✅ Test 1: Docker Works Inside Jenkins</h3>
<pre>
docker exec -it jenkins docker ps
</pre>

<p><strong>Expected:</strong> List of running Docker containers</p>

<h3>✅ Test 2: kubectl Works Inside Jenkins</h3>
<pre>
docker exec -it jenkins kubectl get nodes
</pre>

<p><strong>Expected output:</strong></p>
<pre>
NAME                     STATUS   ROLES           AGE   VERSION
cloudops-control-plane   Ready    control-plane   XXm   vX.XX.X
</pre>

<h3>🎉 THIS IS THE FINAL CONFIRMATION</h3>
<p>If both commands work, your setup is <strong>100% complete and production-ready</strong>.</p>

<hr>

<h2>🟦 11. STEP 9: Restore Host kubectl (Mac) - Optional</h2>

<p>Keep your Mac's kubectl working with localhost:</p>

<pre>
kind get kubeconfig --name cloudops &gt; ~/.kube/config
kubectl get nodes
</pre>

<h3>This Keeps:</h3>
<ul>
  <li><strong>Mac kubectl</strong> → Uses <code>localhost:XXXXX</code></li>
  <li><strong>Jenkins kubectl</strong> → Uses internal Docker DNS <code>cloudops-control-plane:6443</code></li>
</ul>

<hr>

<h2>🏗️ 12. Final Architecture (You Built This)</h2>

<pre>
Mac (Docker Desktop)
 │
 ├── KIND Kubernetes (cloudops)
 │    ├── Control Plane: cloudops-control-plane
 │    └── Resources: Pods / Services / Deployments
 │
 └── Jenkins Container (Docker, ROOT)
      ├── Docker CLI (installed) ✅
      ├── kubectl (installed) ✅
      ├── /root/.kube/config (internal kubeconfig) ✅
      ├── /var/run/docker.sock (mounted) ✅
      └── Network: kind (connected to KIND cluster) ✅
</pre>

<p><strong>This is PRODUCTION-STYLE CI/CD, not tutorial junk.</strong></p>

<hr>

<h2>🔧 13. Troubleshooting Common Issues</h2>

<table border="1">
  <tr>
    <th>Issue</th>
    <th>Solution</th>
  </tr>
  <tr>
    <td>kubectl: command not found</td>
    <td>Re-run STEP 4 to install kubectl</td>
  </tr>
  <tr>
    <td>docker: command not found</td>
    <td>Re-run STEP 3 to install Docker CLI</td>
  </tr>
  <tr>
    <td>kubectl: connection refused</td>
    <td>Verify kubeconfig is in <code>/root/.kube/config</code> (STEP 7)</td>
  </tr>
  <tr>
    <td>kubectl: server mismatch</td>
    <td>Use internal kubeconfig (STEP 5)</td>
  </tr>
  <tr>
    <td>Permission denied (docker.sock)</td>
    <td>Ensure Jenkins runs as root (<code>--user root</code> in STEP 2)</td>
  </tr>
  <tr>
    <td>Jenkins can't reach KIND</td>
    <td>Verify <code>--network kind</code> flag in STEP 2</td>
  </tr>
</table>

<hr>

<h2>🧪 14. Testing Your Setup</h2>

<h3>Test 1: Create Test Deployment</h3>
<pre>
docker exec -it jenkins kubectl create deployment nginx --image=nginx -n default
docker exec -it jenkins kubectl get pods -n default
</pre>

<h3>Test 2: Build Docker Image</h3>
<pre>
docker exec -it jenkins docker build --help
</pre>

<h3>Test 3: Access Kubernetes Service</h3>
<pre>
docker exec -it jenkins kubectl get svc -A
</pre>

<hr>

<h2>🧠 15. Why This Setup is Perfect (Interview Gold)</h2>

<blockquote>
<p><strong>Interview Answer:</strong></p>
<p>"On macOS Docker Desktop, Jenkins must run as root to access <code>docker.sock</code>. kubectl is installed inside Jenkins and uses KIND's internal kubeconfig placed in the default path (<code>/root/.kube/config</code>) for non-interactive CI jobs. This ensures seamless Docker builds and Kubernetes deployments without environment variable exports or path hacks."</p>
</blockquote>

<p><strong>🔥 That answer = Strong DevOps confidence</strong></p>

<hr>

<h2>📊 16. Setup Validation Checklist</h2>

<table border="1">
  <tr>
    <th>Step</th>
    <th>Command</th>
    <th>Status</th>
  </tr>
  <tr>
    <td>Jenkins Running</td>
    <td><code>docker ps | grep jenkins</code></td>
    <td>✅</td>
  </tr>
  <tr>
    <td>Jenkins as Root</td>
    <td><code>docker exec jenkins whoami</code> → <code>root</code></td>
    <td>✅</td>
  </tr>
  <tr>
    <td>Docker CLI Installed</td>
    <td><code>docker exec jenkins docker --version</code></td>
    <td>✅</td>
  </tr>
  <tr>
    <td>kubectl Installed</td>
    <td><code>docker exec jenkins kubectl version --client</code></td>
    <td>✅</td>
  </tr>
  <tr>
    <td>Kubeconfig in Place</td>
    <td><code>docker exec jenkins ls /root/.kube/config</code></td>
    <td>✅</td>
  </tr>
  <tr>
    <td>kubectl Connects</td>
    <td><code>docker exec jenkins kubectl get nodes</code></td>
    <td>✅</td>
  </tr>
  <tr>
    <td>Docker Socket Works</td>
    <td><code>docker exec jenkins docker ps</code></td>
    <td>✅</td>
  </tr>
  <tr>
    <td>Network Connected</td>
    <td><code>docker network inspect kind | grep jenkins</code></td>
    <td>✅</td>
  </tr>
</table>

<hr>

<h2>🎯 17. Next Steps</h2>

<p>Now that your Jenkins environment is fully configured, you can:</p>

<ol>
  <li><strong>Create Jenkins Pipeline Jobs</strong> - Build and deploy applications</li>
  <li><strong>Configure GitHub Webhooks</strong> - Trigger builds automatically</li>
  <li><strong>Set up Docker Hub Integration</strong> - Push images to registry</li>
  <li><strong>Deploy to Kubernetes</strong> - Use kubectl in Jenkins jobs</li>
  <li><strong>Add Monitoring</strong> - Prometheus + Grafana integration</li>
</ol>

<hr>

<h2>📚 18. Quick Reference Commands</h2>

<table border="1">
  <tr>
    <th>Action</th>
    <th>Command</th>
  </tr>
  <tr>
    <td>Access Jenkins Container</td>
    <td><code>docker exec -it jenkins bash</code></td>
  </tr>
  <tr>
    <td>View Jenkins Logs</td>
    <td><code>docker logs -f jenkins</code></td>
  </tr>
  <tr>
    <td>Restart Jenkins</td>
    <td><code>docker restart jenkins</code></td>
  </tr>
  <tr>
    <td>Test kubectl</td>
    <td><code>docker exec jenkins kubectl get nodes</code></td>
  </tr>
  <tr>
    <td>Test Docker</td>
    <td><code>docker exec jenkins docker ps</code></td>
  </tr>
  <tr>
    <td>Check kubeconfig</td>
    <td><code>docker exec jenkins cat /root/.kube/config</code></td>
  </tr>
  <tr>
    <td>Jenkins Initial Password</td>
    <td><code>docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword</code></td>
  </tr>
</table>

<hr>

<h2>🏆 19. Completion</h2>

<p><strong>Congratulations!</strong> You have successfully set up a production-grade Jenkins CI/CD environment with:</p>

<ul>
  <li>✅ Full Docker integration</li>
  <li>✅ Complete Kubernetes access</li>
  <li>✅ Proper security configuration</li>
  <li>✅ Network connectivity to KIND cluster</li>
  <li>✅ Production-ready setup</li>
</ul>

<p>This setup mirrors real-world DevOps environments used by professional teams.</p>

<hr>

<h2>🔗 Related Documentation</h2>

<ul>
  <li><a href="https://www.jenkins.io/doc/">Jenkins Official Documentation</a></li>
  <li><a href="https://kind.sigs.k8s.io/">KIND Documentation</a></li>
  <li><a href="https://kubernetes.io/docs/home/">Kubernetes Documentation</a></li>
  <li><a href="https://docs.docker.com/">Docker Documentation</a></li>
</ul>

</body>
</html>
