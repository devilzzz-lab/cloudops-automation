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
This phase deploys the Dockerized CloudOps application to a local Kubernetes cluster
created using <strong>KIND (Kubernetes IN Docker)</strong>, with automated rollout from Jenkins.
</p>

<hr>

<h2>📌 1. Overview</h2>

<p>In this phase, you will:</p>
<ul>
  <li>✔ Create a Kubernetes cluster using KIND</li>
  <li>✔ Verify the cluster using kubectl</li>
  <li>✔ Define Kubernetes manifests in a <code>/k8s</code> folder</li>
  <li>✔ Configure Jenkins (Dockerized) with Docker + kubectl</li>
  <li>✔ Deploy applications to KIND from Jenkins</li>
  <li>✔ Verify application access using NodePort / port-forward</li>
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
        | Webhook
        v
------------------------------
        Jenkins (Docker)
  - Docker Build & Push
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
   KIND Kubernetes Cluster
------------------------------
 Namespace: cloudops
 - Deployment (App)
 - Service (NodePort)
 - StatefulSet (DB)
 - DaemonSet (Logs)
 - PVC (Storage)
------------------------------
</pre>

<hr>

<h2>🛰 3. Create Kubernetes Cluster using KIND</h2>

<h3>Step 1: Create Cluster</h3>

<pre><code>kind create cluster --name cloudops</code></pre>

<h3>Step 2: Verify Cluster</h3>

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

<h2>🧰 4. Kubernetes Manifests (k8s/ Folder)</h2>

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

<hr>

<h3>🧾 4.1 Namespace</h3>

<pre><code>
apiVersion: v1
kind: Namespace
metadata:
  name: cloudops
</code></pre>

<hr>

<h3>🧾 4.2 Deployment</h3>

<pre><code>
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
          ports:
            - containerPort: 8080
</code></pre>

<hr>

<h3>🧾 4.3 Service (NodePort)</h3>

<pre><code>
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
</code></pre>

<p>Access at: <code>http://localhost:30080</code></p>

<hr>

<h2>🔧 5. Deploy to KIND</h2>

<pre><code>
kubectl apply -f k8s/
kubectl get pods -n cloudops
kubectl get svc -n cloudops
</code></pre>

<hr>

<h2>🔄 6. Jenkins Integration (KIND)</h2>

<p>Jenkins runs as a Docker container and deploys directly to KIND.</p>

<h3>Key Points:</h3>
<ul>
  <li>Jenkins runs as <strong>root</strong></li>
  <li>Docker socket mounted</li>
  <li>kubectl installed inside Jenkins</li>
  <li>KIND internal kubeconfig used</li>
</ul>

<hr>

<h2>🔧 7. Jenkins + Docker + kubectl + KIND Setup</h2>

<h3>Run Jenkins</h3>

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

<hr>

<h3>Install Docker + kubectl in Jenkins</h3>

<pre><code>
docker exec -u root -it jenkins bash
apt-get update
apt-get install -y docker.io curl
curl -LO https://dl.k8s.io/release/$(curl -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl
chmod +x kubectl
mv kubectl /usr/local/bin/
exit
</code></pre>

<hr>

<h3>Configure KIND Internal Kubeconfig</h3>

<pre><code>
kind get kubeconfig --name cloudops --internal > /tmp/kind-internal-config
docker cp /tmp/kind-internal-config jenkins:/var/jenkins_home/.kube/config
docker exec -u root -it jenkins bash
mkdir -p /root/.kube
cp /var/jenkins_home/.kube/config /root/.kube/config
exit
</code></pre>

<hr>

<h3>Final Verification</h3>

<pre><code>
docker exec -it jenkins docker ps
docker exec -it jenkins kubectl get nodes
</code></pre>

<p><strong>Expected:</strong></p>
<pre>
cloudops-control-plane   Ready
</pre>

<hr>

<h2>🎉 PHASE 4 COMPLETION</h2>

<ul>
  <li>✅ KIND Kubernetes cluster running</li>
  <li>✅ Jenkins deploys directly to Kubernetes</li>
  <li>✅ Docker builds & pushes automated</li>
  <li>✅ Production-style CI/CD achieved</li>
</ul>

<hr>

<h2>🧠 Interview Answer (Golden)</h2>

<blockquote>
“Jenkins runs inside Docker and deploys to a KIND Kubernetes cluster using an internal kubeconfig.
Docker builds, image pushes, and Kubernetes rollouts are fully automated.”
</blockquote>

<hr>

<p><strong>— CloudOps Automation Project</strong></p>

</body>
</html>
