<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>

<h1>🟧 PHASE 4 – Kubernetes Deployment using KIND (README.md)</h1>

<p><strong>Version:</strong> Phase 4<br>
<strong>Module:</strong> Kubernetes Deployment & Continuous Deployment (CD)<br>
<strong>Project:</strong> CloudOps Automation, CI/CD &amp; Monitoring System</p>

<hr>

<h2>📌 1. Overview</h2>

<p>Phase-4 focuses on deploying the Dockerized CloudOps application (built in Phase-3) to a local Kubernetes cluster using <strong>KIND (Kubernetes IN Docker)</strong>.</p>

<p><strong>Important:</strong> KIND and all Kubernetes tooling are installed <strong>only in Phase-4</strong>. Phase-3 handled CI (Continuous Integration) without any Kubernetes cluster.</p>

<p>This phase covers:</p>
<ul>
<li>✔ Installing KIND on macOS</li>
<li>✔ Creating a local Kubernetes cluster</li>
<li>✔ Writing Kubernetes manifests for deployment</li>
<li>✔ Reconfiguring Jenkins to connect to KIND cluster</li>
<li>✔ Installing kubectl inside Jenkins</li>
<li>✔ Creating CD job (<strong>cloudops-prod-deploy</strong>) for automated deployment</li>
</ul>

<p><strong>Prerequisites:</strong> Phase-3 must be completed (Jenkins + Docker + CI build job working).</p>

<hr>

<h2>🧩 2. Architecture Diagram</h2>

<pre>
Developer (Local Machine)
        |
        | git push
        v
  GitHub Repository
        |
        | Webhook
        v
      Jenkins
        |
        |-- Job 1: cloudops-ci-build (Phase-3)
        |   └── Builds & pushes Docker image
        |
        |-- Job 2: cloudops-prod-deploy (Phase-4)
        |   └── Deploys to Kubernetes
        |
        v
    Docker Hub
        |
        | Pull image
        v
  KIND Kubernetes Cluster
        |
        └── Namespace: cloudops
            ├── Deployment
            ├── Service
            └── ConfigMap
</pre>

<hr>

<h2>🧰 3. Install KIND on macOS</h2>

<h3>Step 3.1: Install KIND</h3>
<pre>
brew install kind
</pre>

<h3>Step 3.2: Verify Installation</h3>
<pre>
kind version
</pre>

<p><strong>Expected output:</strong></p>
<pre>
kind v0.20.0 go1.21.0 darwin/arm64
</pre>

<hr>

<h2>🛰 4. Create Kubernetes Cluster using KIND</h2>

<h3>Step 4.1: Create Cluster</h3>
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

<h3>Step 4.2: Verify Cluster</h3>
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

<h2>🔧 5. Reconfigure Jenkins for KIND</h2>

<p><strong>Important:</strong> Jenkins was created in Phase-3 with <code>--network bridge</code>. We need to recreate it with <code>--network kind</code> to connect to the KIND cluster.</p>

<h3>Step 5.1: Stop and Remove Old Jenkins</h3>
<pre>
docker stop jenkins
docker rm jenkins
</pre>

<p><strong>Note:</strong> Your Jenkins data is safe in <code>~/jenkins_home</code></p>

<h3>Step 5.2: Run Jenkins with KIND Network</h3>
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

<p><strong>Key change:</strong> <code>--network kind</code> (was <code>--network bridge</code> in Phase-3)</p>

<h3>Step 5.3: Verify Jenkins is Running</h3>
<pre>
docker ps | grep jenkins
</pre>

<p>Access Jenkins UI:</p>
<pre>
http://localhost:8080
</pre>

<p><strong>Note:</strong> All your previous jobs and credentials are preserved!</p>

<hr>

<h2>🔨 6. Install kubectl Inside Jenkins</h2>

<h3>Step 6.1: Enter Jenkins Container</h3>
<pre>
docker exec -u root -it jenkins bash
</pre>

<h3>Step 6.2: Download kubectl</h3>
<pre>
curl -LO https://dl.k8s.io/release/$(curl -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl
</pre>

<h3>Step 6.3: Make kubectl Executable</h3>
<pre>
chmod +x kubectl
</pre>

<h3>Step 6.4: Move kubectl to PATH</h3>
<pre>
mv kubectl /usr/local/bin/
</pre>

<h3>Step 6.5: Verify kubectl Installation</h3>
<pre>
kubectl version --client
</pre>

<p><strong>Expected output:</strong></p>
<pre>
Client Version: vX.XX.X
</pre>

<h3>Step 6.6: Exit Container</h3>
<pre>
exit
</pre>

<hr>

<h2>🔐 7. Configure KIND Kubeconfig for Jenkins</h2>

<h3>Step 7.1: Generate Internal Kubeconfig</h3>

<p><strong>On your Mac (host machine):</strong></p>

<pre>
kind get kubeconfig --name cloudops --internal &gt; /tmp/kind-internal-config
</pre>

<p><strong>Why internal?</strong> Jenkins runs inside Docker and needs to use Docker DNS (<code>cloudops-control-plane</code>) instead of <code>localhost</code>.</p>

<h3>Step 7.2: Verify Internal Kubeconfig</h3>
<pre>
cat /tmp/kind-internal-config | grep server
</pre>

<p><strong>Expected output:</strong></p>
<pre>
server: https://cloudops-control-plane:6443
</pre>

<h3>Step 7.3: Copy to Jenkins Container</h3>
<pre>
docker cp /tmp/kind-internal-config jenkins:/var/jenkins_home/.kube/config
</pre>

<h3>Step 7.4: Set Default kubectl Path in Jenkins</h3>

<p>Enter Jenkins container:</p>
<pre>
docker exec -u root -it jenkins bash
</pre>

<p>Create .kube directory for root user:</p>
<pre>
mkdir -p /root/.kube
</pre>

<p>Copy config to default path:</p>
<pre>
cp /var/jenkins_home/.kube/config /root/.kube/config
</pre>

<p>Set proper permissions:</p>
<pre>
chmod 600 /root/.kube/config
</pre>

<p>Verify file exists:</p>
<pre>
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

<h3>Step 7.5: Verify kubectl Works in Jenkins</h3>
<pre>
docker exec -it jenkins kubectl get nodes
</pre>

<p><strong>Expected output:</strong></p>
<pre>
NAME                     STATUS   ROLES           AGE   VERSION
cloudops-control-plane   Ready    control-plane   XXm   vX.XX.X
</pre>

<p><strong>✅ If this works, Jenkins can now deploy to Kubernetes!</strong></p>

<hr>

<h2>📁 8. Create Kubernetes Manifests</h2>

<p>Create a <code>k8s/</code> folder in your GitHub repository with the following files:</p>

<h3>Project Structure</h3>
<pre>
cloudops-automation/
├── app.py
├── requirements.txt
├── Dockerfile
└── k8s/
    ├── namespace.yaml
    ├── configmap.yaml
    ├── deployment.yaml
    └── service.yaml
</pre>

<h3>8.1 Namespace (k8s/namespace.yaml)</h3>
<pre>
apiVersion: v1
kind: Namespace
metadata:
  name: cloudops
  labels:
    name: cloudops
</pre>

<h3>8.2 ConfigMap (k8s/configmap.yaml)</h3>
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

<h3>8.3 Deployment (k8s/deployment.yaml)</h3>
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

<h3>8.4 Service (k8s/service.yaml)</h3>
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

<p>Commit and push these files to GitHub:</p>
<pre>
git add k8s/
git commit -m "Add Kubernetes manifests"
git push origin main
</pre>

<hr>

<h2>🟦 9. Create Jenkins Deployment Job (cloudops-prod-deploy)</h2>

<h3>9.1 Create New Job</h3>
<ol>
<li>Go to Jenkins Dashboard</li>
<li>Click <strong>New Item</strong></li>
<li>Enter name: <strong>cloudops-prod-deploy</strong></li>
<li>Select <strong>Freestyle project</strong></li>
<li>Click <strong>OK</strong></li>
</ol>

<h3>9.2 Configure Source Code Management</h3>
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

<h3>9.3 Configure Build Triggers</h3>
<p>Enable:</p>
<ul>
<li>☑ <strong>Build after other projects are built</strong></li>
<li>Projects to watch: <code>cloudops-ci-build</code></li>
<li>Trigger only if build is stable</li>
</ul>

<p>This ensures deployment happens automatically after successful Docker build.</p>

<h3>9.4 Add Build Step (Execute Shell)</h3>
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

<h3>9.5 Save the Job</h3>
<p>Click <strong>Save</strong>.</p>

<hr>

<h2>🚀 10. Deploy to Kubernetes</h2>

<h3>Step 10.1: Manual Deployment Test</h3>
<ol>
<li>Go to Jenkins Dashboard</li>
<li>Click <strong>cloudops-prod-deploy</strong></li>
<li>Click <strong>Build Now</strong></li>
<li>Check <strong>Console Output</strong></li>
</ol>

<p><strong>Expected Console Output:</strong></p>
<pre>
🚀 CD JOB – Kubernetes Deployment
📦 Applying Kubernetes manifests...
namespace/cloudops created
configmap/cloudops-config created
deployment.apps/cloudops-app created
service/cloudops-service created
⏳ Waiting for deployment rollout...
deployment "cloudops-app" successfully rolled out
✅ Deployment completed successfully!
</pre>

<h3>Step 10.2: Verify Deployment</h3>
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

<h3>Step 10.3: Access Application</h3>
<p>Open browser:</p>
<pre>
http://localhost:30080
</pre>

<p><strong>Expected:</strong> You should see "CloudOps Sample App" running!</p>

<hr>

<h2>🔄 11. Test Complete CI/CD Pipeline</h2>

<h3>Full Automation Flow</h3>

<p>Make a change to your app and push:</p>

<pre>
echo "# Pipeline test" &gt;&gt; README.md
git add .
git commit -m "Test full CI/CD pipeline"
git push origin main
</pre>

<h3>What Happens Automatically:</h3>
<ol>
<li>GitHub sends webhook to Jenkins</li>
<li><strong>cloudops-ci-build</strong> triggers automatically</li>
<li>Docker image built and pushed to Docker Hub</li>
<li><strong>cloudops-prod-deploy</strong> triggers after CI success</li>
<li>Kubernetes pulls new image and updates pods</li>
<li>Application updated with zero downtime!</li>
</ol>

<hr>

<h2>🏁 12. Completion Checklist</h2>

<table border="1">
<tr>
<th>Step</th>
<th>Status</th>
<th>Verification</th>
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
<td>Jenkins reconnected to KIND</td>
<td>✅</td>
<td><code>docker inspect jenkins | grep kind</code></td>
</tr>
<tr>
<td>kubectl installed in Jenkins</td>
<td>✅</td>
<td><code>docker exec jenkins kubectl version</code></td>
</tr>
<tr>
<td>Jenkins can access KIND</td>
<td>✅</td>
<td><code>docker exec jenkins kubectl get nodes</code></td>
</tr>
<tr>
<td>K8s manifests created</td>
<td>✅</td>
<td>Files exist in <code>k8s/</code></td>
</tr>
<tr>
<td>CD job created</td>
<td>✅</td>
<td>Job <strong>cloudops-prod-deploy</strong> visible</td>
</tr>
<tr>
<td>Manual deployment works</td>
<td>✅</td>
<td>Build Now succeeds</td>
</tr>
<tr>
<td>Application accessible</td>
<td>✅</td>
<td><code>curl http://localhost:30080</code></td>
</tr>
<tr>
<td>Auto deployment works</td>
<td>✅</td>
<td>Git push triggers both jobs</td>
</tr>
</table>

<hr>

<h2>🎉 13. Phase 4 Complete</h2>

<p>Congratulations! You now have:</p>
<ul>
<li>✅ Full CI/CD pipeline from code to production</li>
<li>✅ Automated Docker builds (Phase-3)</li>
<li>✅ Automated Kubernetes deployments (Phase-4)</li>
<li>✅ Local Kubernetes cluster with KIND</li>
<li>✅ Production-ready DevOps workflow</li>
</ul>

<p><strong>Next Steps:</strong></p>
<ul>
<li>Add monitoring with Prometheus & Grafana</li>
<li>Implement autoscaling</li>
<li>Add ingress controller</li>
<li>Set up centralized logging</li>
</ul>

<hr>

<p><strong>— CloudOps Automation Project | Phase 4 Complete</strong></p>

</body>
</html>
