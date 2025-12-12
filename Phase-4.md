<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>

<h1>🟧 PHASE 4 – Kubernetes Deployment on Docker Desktop</h1>

<p><strong>Version:</strong> Phase 4<br>
<strong>Module:</strong> Kubernetes Deployment &amp; Local Orchestration<br>
<strong>Project:</strong> CloudOps Automation, CI/CD &amp; Monitoring System</p>

<p>This phase deploys your Dockerized CloudOps application to a local Kubernetes cluster (Docker Desktop Kubernetes) with automated rollout from Jenkins.</p>

<hr>

<h2>📌 1. Overview</h2>

<p>In this phase, you will:</p>
<ul>
  <li>✔ Enable Kubernetes inside Docker Desktop</li>
  <li>✔ Verify local Kubernetes cluster using kubectl</li>
  <li>✔ Define Kubernetes manifests in a /k8s folder</li>
  <li>✔ Create three Jenkins Freestyle jobs (Dev / Test / Prod)</li>
  <li>✔ Each Jenkins job will:
    <ul>
      <li>Pull code from GitHub</li>
      <li>Build a Docker image</li>
      <li>Push image to Docker Hub</li>
      <li>Run <code>kubectl apply -f k8s/</code> to deploy to local cluster</li>
    </ul>
  </li>
  <li>✔ Verify the application is reachable via NodePort / port-forwarding</li>
</ul>

<hr>

<h2>🧩 2. Architecture Diagram</h2>

<pre>
Developer (Git Push)
        |
        v
------------------------------
        GitHub Repo
------------------------------
        |
        |  Webhook (push)
        v
------------------------------
            Jenkins
      [Freestyle Jobs]
  Dev / Test / Prod Deploy
  - Docker Build &amp; Push
  - kubectl apply -f k8s/
------------------------------
        |
        v
------------------------------
   Docker Hub (Registry)
------------------------------
        |
        v
------------------------------
  Docker Desktop Kubernetes
     (Local Cluster)
------------------------------
   | Namespace: cloudops
   | Deployment (App)
   | Service (NodePort/LoadBalancer)
   | StatefulSet (DB, uses PVC)
   | DaemonSet (Logging Agent)
   | PV/PVC (Local storage)
------------------------------
</pre>

<hr>

<h2>🛰 3. Enable Kubernetes in Docker Desktop</h2>

<h3>🧠 3.1 Enable Kubernetes Cluster</h3>

<h4>Step 1: Open Docker Desktop Settings</h4>
<ol>
  <li>Open Docker Desktop application on your Mac</li>
  <li>Click on the <strong>gear icon (⚙️)</strong> in the top-right corner to open Settings</li>
  <li>Navigate to <strong>Kubernetes</strong> section from the left sidebar</li>
</ol>

<h4>Step 2: Enable Kubernetes</h4>
<ul>
  <li>Check the box: <strong>Enable Kubernetes</strong></li>
  <li>Click <strong>Apply &amp; Restart</strong></li>
  <li>Docker Desktop will download Kubernetes images and start a single-node cluster</li>
  <li>Wait 2-5 minutes for the setup to complete</li>
</ul>

<h4>Step 3: Verify Kubernetes is Running</h4>
<p>You should see <strong>Kubernetes running</strong> indicator (green) in Docker Desktop Dashboard footer.</p>

<hr>

<h3>🧠 3.2 Verify Kubernetes Cluster</h3>

<h4>Step 1: Check Kubernetes Version</h4>
<pre><code>kubectl version --short</code></pre>

<h4>Step 2: Check Cluster Info</h4>
<pre><code>kubectl cluster-info</code></pre>

<p>You should see:</p>
<pre>
Kubernetes control plane is running at https://kubernetes.docker.internal:6443
CoreDNS is running at https://kubernetes.docker.internal:6443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
</pre>

<h4>Step 3: Check Nodes</h4>
<pre><code>kubectl get nodes</code></pre>

<p>Expected output:</p>
<pre>
NAME             STATUS   ROLES           AGE   VERSION
docker-desktop   Ready    control-plane   5m    v1.31.0
</pre>

<h4>Step 4: Check Current Context</h4>
<pre><code>kubectl config current-context</code></pre>

<p>Should return: <code>docker-desktop</code></p>

<hr>

<h2>🧰 4. Kubernetes Manifests (k8s/ Folder)</h2>

<p>In your repo (<code>cloudops-automation/</code>), create:</p>

<pre>
cloudops-automation/
├── app.py
├── requirements.txt
├── Dockerfile
├── PHASE-1.md
├── PHASE-2.md
├── PHASE-3.md
├── PHASE-4.md
└── k8s/
    ├── namespace.yaml
    ├── deployment.yaml
    ├── service.yaml
    ├── configmap.yaml
    ├── secret.yaml
    ├── pvc.yaml
    ├── statefulset-db.yaml
    ├── daemonset-logs.yaml
    └── ingress.yaml (optional)
</pre>

<hr>

<h3>🧾 4.1 Namespace</h3>

<pre><code># k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: cloudops
</code></pre>

<hr>

<h3>🧾 4.2 ConfigMap</h3>

<pre><code># k8s/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: cloudops-config
  namespace: cloudops
data:
  APP_ENV: "production"
  LOG_LEVEL: "info"
</code></pre>

<hr>

<h3>🧾 4.3 Secret</h3>

<pre><code># k8s/secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: cloudops-secret
  namespace: cloudops
type: Opaque
stringData:
  DB_PASSWORD: "super-secret"
  API_KEY: "your-api-key"
</code></pre>

<hr>

<h3>🧾 4.4 Deployment (Application)</h3>

<pre><code># k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cloudops-app
  namespace: cloudops
spec:
  replicas: 2
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
          image: devilzz/cloudops-app:latest
          ports:
            - containerPort: 8080
          envFrom:
            - configMapRef:
                name: cloudops-config
            - secretRef:
                name: cloudops-secret
</code></pre>

<hr>

<h3>🧾 4.5 Service (NodePort for Local Access)</h3>

<pre><code># k8s/service.yaml
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
</code></pre>

<p><strong>Note:</strong> With Docker Desktop, you can access the app at <code>http://localhost:30080</code></p>

<hr>

<h3>🧾 4.6 PVC (PersistentVolumeClaim)</h3>

<pre><code># k8s/pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: cloudops-pvc
  namespace: cloudops
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
</code></pre>

<hr>

<h3>🧾 4.7 StatefulSet (DB Example)</h3>

<pre><code># k8s/statefulset-db.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: cloudops-db
  namespace: cloudops
spec:
  serviceName: "cloudops-db"
  replicas: 1
  selector:
    matchLabels:
      app: cloudops-db
  template:
    metadata:
      labels:
        app: cloudops-db
    spec:
      containers:
        - name: postgres
          image: postgres:15
          env:
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: cloudops-secret
                  key: DB_PASSWORD
          ports:
            - containerPort: 5432
          volumeMounts:
            - name: data
              mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 5Gi
</code></pre>

<hr>

<h3>🧾 4.8 DaemonSet (Logging Agent Example)</h3>

<pre><code># k8s/daemonset-logs.yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: cloudops-logs
  namespace: cloudops
spec:
  selector:
    matchLabels:
      app: cloudops-logs
  template:
    metadata:
      labels:
        app: cloudops-logs
    spec:
      containers:
        - name: fluent-bit
          image: fluent/fluent-bit:latest
</code></pre>

<hr>

<h3>🧾 4.9 Ingress (Optional – NGINX)</h3>

<pre><code># k8s/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: cloudops-ingress
  namespace: cloudops
spec:
  rules:
    - http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: cloudops-service
                port:
                  number: 80
</code></pre>

<hr>

<h2>🔧 5. Deploy to Local Kubernetes Cluster</h2>

<h3>Step 1: Apply All Manifests</h3>
<pre><code>kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/pvc.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/statefulset-db.yaml
kubectl apply -f k8s/daemonset-logs.yaml</code></pre>

<p>Or apply all at once:</p>
<pre><code>kubectl apply -f k8s/</code></pre>

<h3>Step 2: Verify Deployment</h3>
<pre><code># Check namespace
kubectl get ns

# Check all resources in cloudops namespace
kubectl get all -n cloudops

# Check pods status
kubectl get pods -n cloudops

# Check service
kubectl get svc -n cloudops

# Check PVC
kubectl get pvc -n cloudops</code></pre>

<h3>Step 3: Access the Application</h3>
<p>If using NodePort service:</p>
<pre><code># Access at http://localhost:30080
curl http://localhost:30080</code></pre>

<p>Or use port-forwarding:</p>
<pre><code>kubectl port-forward -n cloudops svc/cloudops-service 8080:80</code></pre>
<p>Then access at <code>http://localhost:8080</code></p>

<hr>

<h2>🔄 6. Jenkins Integration (Execute Shell Jobs)</h2>

<h3>🧠 6.1 Jenkins Job Configuration</h3>

<h4>Create Three Freestyle Jobs:</h4>
<ol>
  <li><strong>cloudops-dev-deploy</strong></li>
  <li><strong>cloudops-test-deploy</strong></li>
  <li><strong>cloudops-prod-deploy</strong></li>
</ol>

<h4>Job Configuration (Example: Dev Deploy)</h4>

<p><strong>Source Code Management:</strong></p>
<ul>
  <li>Git Repository URL: <code>https://github.com/yourusername/cloudops-automation.git</code></li>
  <li>Branch: <code>*/dev</code> (or */main for prod)</li>
</ul>

<p><strong>Build Triggers:</strong></p>
<ul>
  <li>✅ GitHub hook trigger for GITScm polling</li>
</ul>

<p><strong>Build Steps → Execute Shell:</strong></p>

<pre><code>#!/bin/bash
set -e

# Variables
IMAGE_NAME="devilzz/cloudops-app"
TAG="dev-${BUILD_NUMBER}"

echo "=== Building Docker Image ==="
docker build -t ${IMAGE_NAME}:${TAG} .
docker tag ${IMAGE_NAME}:${TAG} ${IMAGE_NAME}:latest

echo "=== Pushing to Docker Hub ==="
docker push ${IMAGE_NAME}:${TAG}
docker push ${IMAGE_NAME}:latest

echo "=== Deploying to Kubernetes ==="
kubectl config use-context docker-desktop
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/pvc.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/statefulset-db.yaml
kubectl apply -f k8s/daemonset-logs.yaml

echo "=== Verifying Deployment ==="
kubectl get pods -n cloudops
kubectl get svc -n cloudops

echo "=== Deployment Complete ==="
</code></pre>

<hr>

<h2>📊 7. Notion Task Table (Phase-4 Checklist)</h2>

<table border="1" cellpadding="8" cellspacing="0">
  <thead>
    <tr>
      <th>Step</th>
      <th>Status</th>
      <th>Verification</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Enable Kubernetes in Docker Desktop</td>
      <td>⬜</td>
      <td>Kubernetes running indicator green</td>
    </tr>
    <tr>
      <td>Verify kubectl works</td>
      <td>⬜</td>
      <td><code>kubectl get nodes</code> shows docker-desktop</td>
    </tr>
    <tr>
      <td>Create k8s/ folder in GitHub</td>
      <td>⬜</td>
      <td>Files visible in repo</td>
    </tr>
    <tr>
      <td>Apply namespace.yaml</td>
      <td>⬜</td>
      <td><code>kubectl get ns</code> shows cloudops</td>
    </tr>
    <tr>
      <td>Apply configmap + secret</td>
      <td>⬜</td>
      <td><code>kubectl get cm,secret -n cloudops</code></td>
    </tr>
    <tr>
      <td>Apply pvc</td>
      <td>⬜</td>
      <td>PVC Bound</td>
    </tr>
    <tr>
      <td>Apply statefulset-db</td>
      <td>⬜</td>
      <td>DB pod Running</td>
    </tr>
    <tr>
      <td>Apply deployment + service</td>
      <td>⬜</td>
      <td>App pods Running &amp; Service created</td>
    </tr>
    <tr>
      <td>Apply daemonset-logs</td>
      <td>⬜</td>
      <td>One pod per node</td>
    </tr>
    <tr>
      <td>(Optional) Apply ingress</td>
      <td>⬜</td>
      <td>Ingress routes traffic at localhost</td>
    </tr>
    <tr>
      <td>Test app via NodePort</td>
      <td>⬜</td>
      <td><code>curl http://localhost:30080</code> works</td>
    </tr>
    <tr>
      <td>Create Jenkins Dev job (Execute Shell)</td>
      <td>⬜</td>
      <td>Job visible, no errors</td>
    </tr>
    <tr>
      <td>Create Jenkins Test job</td>
      <td>⬜</td>
      <td>Job visible, no errors</td>
    </tr>
    <tr>
      <td>Create Jenkins Prod job</td>
      <td>⬜</td>
      <td>Job visible, no errors</td>
    </tr>
    <tr>
      <td>GitHub webhook to Jenkins</td>
      <td>⬜</td>
      <td>Push triggers build</td>
    </tr>
    <tr>
      <td>Dev job deploys successfully</td>
      <td>⬜</td>
      <td>App reachable via localhost:30080</td>
    </tr>
    <tr>
      <td>Test job deploys successfully</td>
      <td>⬜</td>
      <td>Verified</td>
    </tr>
    <tr>
      <td>Prod job deploys successfully</td>
      <td>⬜</td>
      <td>Verified</td>
    </tr>
    <tr>
      <td>Documentation updated (PHASE-4.md)</td>
      <td>⬜</td>
      <td>File committed to repo</td>
    </tr>
  </tbody>
</table>

<hr>

<h2>🎉 PHASE 4 Completed Successfully (When all boxes are ✅)</h2>

<p>After completion, you will have:</p>
<ul>
  <li>✔ Local Kubernetes cluster running in Docker Desktop</li>
  <li>✔ Kubernetes workloads (Deployment, Service, StatefulSet, DaemonSet, PVC)</li>
  <li>✔ /k8s manifests tracked in GitHub</li>
  <li>✔ Jenkins Freestyle jobs for Dev / Test / Prod</li>
  <li>✔ Automatic build + push + deploy to local Kubernetes using Execute Shell</li>
  <li>✔ Cloud-native deployment layer for your CloudOps Automation project</li>
</ul>

<hr>

<h2>🛠 Troubleshooting</h2>

<h3>Issue: Pods stuck in Pending state</h3>
<pre><code>kubectl describe pod &lt;pod-name&gt; -n cloudops</code></pre>
<p>Check for resource constraints or PVC binding issues</p>

<h3>Issue: Service not accessible</h3>
<pre><code># Check service
kubectl get svc -n cloudops

# Check endpoints
kubectl get endpoints -n cloudops

# Port forward directly to pod
kubectl port-forward -n cloudops pod/&lt;pod-name&gt; 8080:8080</code></pre>

<h3>Issue: kubectl context wrong</h3>
<pre><code># List contexts
kubectl config get-contexts

# Switch to docker-desktop
kubectl config use-context docker-desktop</code></pre>

</body>
</html>
