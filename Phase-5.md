<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>

<h1>🟥 PHASE-5: Monitoring &amp; Observability (PHASE-5.md)</h1>

<p>
<strong>Version:</strong> Phase 5<br>
<strong>Module:</strong> Kubernetes Monitoring &amp; Observability<br>
<strong>Project:</strong> CloudOps Automation, CI/CD &amp; Monitoring System
</p>

<hr>

<h2>📌 1. Overview</h2>

<p>
Phase-5 focuses on implementing <strong>production-style monitoring, metrics collection, visualization, and alerting</strong>
for Kubernetes workloads and applications deployed through the CI/CD pipeline.
</p>

<p>
This phase introduces a complete observability stack using <strong>Prometheus</strong> and <strong>Grafana</strong>,
deployed directly inside the <strong>KIND (Kubernetes IN Docker)</strong> cluster.
</p>

<p>
Monitoring ensures continuous visibility into:
</p>

<ul>
  <li>Kubernetes cluster health</li>
  <li>Pod and container resource utilization</li>
  <li>Application performance and availability</li>
  <li>Deployment stability after Jenkins-driven rollouts</li>
</ul>

<hr>

<h2>🧩 2. Scope &amp; Architecture</h2>

<p>
The monitoring stack is deployed inside the existing KIND Kubernetes cluster and integrates seamlessly
with the CI/CD pipeline built in Phase-4.
</p>

<pre>
KIND Kubernetes Cluster
│
├── Prometheus
│   ├── Node Exporter
│   ├── cAdvisor
│   ├── kube-state-metrics
│   └── Application /metrics endpoint
│
├── Grafana
│   └── Dashboards (Cluster, Pods, Application, Deployments)
│
└── Alertmanager
    └── Email / Slack Notifications
</pre>

<p>
This architecture enables real-time monitoring and alerting without relying on external cloud services.
CloudWatch and SNS integration is documented as a future extension for EKS migration.
</p>

<hr>

<h2>📊 3. Monitoring Components</h2>

<h3>🔹 Metrics Collection (Prometheus)</h3>

<p>
Prometheus is deployed as a Kubernetes service and configured to scrape metrics from multiple sources:
</p>

<ul>
  <li><strong>Node Exporter</strong> – Node-level CPU, memory, disk, and network metrics</li>
  <li><strong>cAdvisor</strong> – Container-level CPU and memory usage</li>
  <li><strong>kube-state-metrics</strong> – Pod status, replicas, restarts, deployment health</li>
  <li><strong>Application Metrics Endpoint</strong> – HTTP requests, latency, error rates, uptime</li>
</ul>

<hr>

<h2>📈 4. Visualization (Grafana)</h2>

<p>
Grafana is deployed inside Kubernetes and configured with Prometheus as the primary data source.
</p>

<h3>📊 Dashboards Implemented</h3>

<h4>1. Kubernetes Cluster Overview</h4>
<ul>
  <li>Node CPU &amp; memory utilization</li>
  <li>Pod distribution per node</li>
  <li>Overall cluster health indicators</li>
</ul>

<h4>2. Kubernetes Workloads Monitoring</h4>
<ul>
  <li>Pod CPU and memory usage</li>
  <li>Pod restart counts</li>
  <li>Replica availability vs desired state</li>
</ul>

<h4>3. Application Health Dashboard</h4>
<ul>
  <li>HTTP request rate</li>
  <li>Error rates (4xx / 5xx)</li>
  <li>Response latency</li>
  <li>Application uptime</li>
</ul>

<h4>4. Deployment Impact Dashboard</h4>
<ul>
  <li>Pod availability during rolling updates</li>
  <li>Resource usage spikes after deployments</li>
  <li>Error rate comparison before and after Jenkins deployments</li>
</ul>

<hr>

<h2>🚨 5. Alerting</h2>

<p>
Prometheus alert rules are configured to detect anomalies and operational issues in real time.
</p>

<ul>
  <li>Pod down or unavailable</li>
  <li>High CPU usage (&gt; 80%)</li>
  <li>High memory consumption</li>
  <li>Frequent container restarts</li>
</ul>

<p>
Alerts are routed via <strong>Alertmanager</strong> to notification channels such as email or Slack.
</p>

<p>
<strong>Note:</strong> Cloud-based alerting using <strong>AWS CloudWatch + SNS</strong> is documented
as a future enhancement when migrating from KIND to EKS.
</p>

<hr>

<h2>🎯 6. Key Outcomes</h2>

<ul>
  <li>Real-time visibility into Kubernetes cluster health</li>
  <li>Continuous monitoring of application performance</li>
  <li>Validation of CI/CD deployment stability</li>
  <li>Early detection of failures and resource saturation</li>
  <li>Cloud-ready observability design aligned with AWS migration</li>
</ul>

<hr>

<h2>🛠 7. Step-by-Step Implementation</h2>

<h3>🟥 STEP 1 – Create Monitoring Namespace</h3>

<h4>🎯 Objective</h4>
<p>Create a dedicated Kubernetes namespace for all monitoring components (Prometheus, Grafana, Alertmanager, exporters).</p>

<h4>Commands</h4>

<p><strong>1.1: Create monitoring namespace</strong></p>
<pre>
kubectl create namespace monitoring
</pre>

<p><strong>1.2: Verify namespace creation</strong></p>
<pre>
kubectl get namespaces
</pre>

<p><strong>Expected output:</strong></p>
<pre>
NAME              STATUS   AGE
default           Active   XXd
kube-system       Active   XXd
monitoring        Active   XXs
</pre>

<hr>

<h3>🟥 STEP 2 – Deploy Prometheus in Kubernetes</h3>

<h4>🎯 Objective</h4>
<p>Deploy Prometheus server inside the monitoring namespace to collect Kubernetes, node, and container metrics.</p>

<p><strong>2.1: Create directory structure</strong></p>
<pre>
mkdir -p monitoring/prometheus
cd monitoring/prometheus
</pre>

<p><strong>2.2: Create Prometheus ConfigMap</strong></p>
<p>📄 File: <code>monitoring/prometheus/prometheus-config.yaml</code></p>

<p><strong>2.3: Create Prometheus Deployment</strong></p>
<p>📄 File: <code>monitoring/prometheus/prometheus-deployment.yaml</code></p>

<p><strong>2.4: Create Prometheus Service</strong></p>
<p>📄 File: <code>monitoring/prometheus/prometheus-service.yaml</code></p>

<p><strong>2.5: Apply Prometheus manifests</strong></p>
<pre>
kubectl apply -f monitoring/prometheus/
</pre>

<p><strong>2.6: Verify Prometheus Deployment</strong></p>
<pre>
kubectl get pods -n monitoring
kubectl get svc -n monitoring
</pre>

<hr>

<h3>🟥 STEP 3 – Verify Prometheus Service &amp; UI</h3>

<h4>🎯 Objective</h4>
<p>Confirm that Prometheus service is reachable, UI loads correctly, and Prometheus is scraping itself successfully.</p>

<p><strong>3.1: Port-forward Prometheus service</strong></p>
<pre>
kubectl port-forward -n monitoring svc/prometheus 9090:9090
</pre>

<p><strong>3.2: Access Prometheus UI</strong></p>
<p>Open browser: <code>http://localhost:9090</code></p>

<p><strong>3.3: Verify Prometheus Targets</strong></p>
<p>In Prometheus UI: Click <strong>Status → Targets</strong></p>
<p>Expected: Target <code>localhost:9090</code> shows Status: <strong>UP</strong> (green)</p>

<p><strong>3.4: Quick Metrics Test</strong></p>
<p>In Prometheus UI → Graph, run query: <code>up</code></p>
<p>Expected result: Value = 1 for Prometheus target</p>

<hr>

<h3>🟥 STEP 4 – Deploy Node Exporter</h3>

<h4>🎯 Objective</h4>
<p>Deploy Node Exporter to collect node-level metrics: CPU, memory, disk, and network I/O.</p>

<p><strong>4.1: Create Node Exporter manifest</strong></p>
<p>📄 File: <code>monitoring/node-exporter.yaml</code></p>

<p><strong>4.2: Apply Node Exporter</strong></p>
<pre>
kubectl apply -f monitoring/node-exporter.yaml
</pre>

<p><strong>4.3: Verify Node Exporter Pods</strong></p>
<pre>
kubectl get pods -n monitoring
</pre>

<hr>

<h3>🟥 STEP 5 – Deploy cAdvisor</h3>

<h4>🎯 Objective</h4>
<p>Deploy cAdvisor to collect container-level metrics: container CPU, memory usage, and resource limits per pod.</p>

<p><strong>5.1: Create cAdvisor manifest</strong></p>
<p>📄 File: <code>monitoring/cadvisor.yaml</code></p>

<p><strong>5.2: Apply cAdvisor</strong></p>
<pre>
kubectl apply -f monitoring/cadvisor.yaml
</pre>

<p><strong>5.3: Verify cAdvisor Pods</strong></p>
<pre>
kubectl get pods -n monitoring
</pre>

<p><strong>5.4: (Optional) Verify cAdvisor UI</strong></p>
<pre>
kubectl port-forward -n monitoring pod/cadvisor-xxxxx 18080:8080
</pre>
<p>Open browser: <code>http://localhost:18080</code></p>

<hr>

<h3>🟥 STEP 6 – Deploy kube-state-metrics</h3>

<h4>🎯 Objective</h4>
<p>Deploy kube-state-metrics to collect Kubernetes object-level metrics: pod status, deployment health, replica counts, and restart counts.</p>

<p><strong>6.1: Create kube-state-metrics manifest</strong></p>
<p>📄 File: <code>monitoring/kube-state-metrics.yaml</code></p>

<p><strong>6.2: Apply kube-state-metrics</strong></p>
<pre>
kubectl apply -f monitoring/kube-state-metrics.yaml
</pre>

<p><strong>6.3: Verify kube-state-metrics Pod</strong></p>
<pre>
kubectl get pods -n monitoring
</pre>

<p><strong>Expected output:</strong></p>
<pre>
kube-state-metrics-xxxxx   1/1   Running
cadvisor-xxxxx             1/1   Running
node-exporter-xxxxx        1/1   Running
prometheus-xxxxx           1/1   Running
</pre>

<hr>

<h3>🟥 STEP 7 – Configure Prometheus to Scrape All Exporters</h3>

<h4>🎯 Objective</h4>
<p>Update Prometheus scrape configuration to collect metrics from Node Exporter, cAdvisor, kube-state-metrics, and Prometheus itself.</p>

<p><strong>7.1: Update Prometheus ConfigMap</strong></p>
<p>📄 File: <code>monitoring/prometheus/prometheus-config.yaml</code></p>
<p>Update the file to include scrape configs for all exporters using Kubernetes service discovery.</p>

<p><strong>7.2: Create Prometheus RBAC</strong></p>
<p>📄 File: <code>monitoring/prometheus/prometheus-rbac.yaml</code></p>
<p>Create ServiceAccount, ClusterRole, and ClusterRoleBinding to allow Prometheus to discover pods via Kubernetes API.</p>

<p><strong>Contents:</strong></p>
<ul>
<li>ServiceAccount: <code>prometheus</code></li>
<li>ClusterRole with permissions to list/watch pods, services, endpoints</li>
<li>ClusterRoleBinding to bind the role to the ServiceAccount</li>
</ul>

<p><strong>7.3: Update Prometheus Deployment</strong></p>
<p>📄 File: <code>monitoring/prometheus/prometheus-deployment.yaml</code></p>
<p>Add <code>serviceAccountName: prometheus</code> under <code>spec.template.spec</code> to attach RBAC permissions.</p>

<p><strong>Key addition:</strong></p>
<pre>
spec:
  template:
    spec:
      serviceAccountName: prometheus
      containers:
        - name: prometheus
          ...
</pre>

<p><strong>7.4: Apply Updated Configuration</strong></p>
<pre>
kubectl apply -f monitoring/prometheus/prometheus-config.yaml
kubectl apply -f monitoring/prometheus/prometheus-rbac.yaml
kubectl apply -f monitoring/prometheus/prometheus-deployment.yaml
</pre>

<p><strong>7.5: Restart Prometheus</strong></p>
<pre>
kubectl rollout restart deployment prometheus -n monitoring
</pre>

<p><strong>7.6: Verify Prometheus Targets</strong></p>
<p>Port-forward Prometheus service:</p>
<pre>
kubectl port-forward -n monitoring svc/prometheus 9090:9090
</pre>

<p>Open browser: <code>http://localhost:9090</code></p>
<p>Navigate to: <strong>Status → Targets</strong></p>

<p><strong>Expected result:</strong></p>
<ul>
<li>prometheus → <strong>UP</strong> (green)</li>
<li>node-exporter → <strong>UP</strong> (green)</li>
<li>cadvisor → <strong>UP</strong> (green)</li>
<li>kube-state-metrics → <strong>UP</strong> (green)</li>
</ul>

<p><strong>7.7: Quick PromQL Tests (Optional)</strong></p>
<p>In Prometheus UI → Graph, test these queries:</p>
<pre>
up
node_cpu_seconds_total
container_cpu_usage_seconds_total
kube_pod_status_phase
</pre>

<p><strong>Expected:</strong> Data appears for all queries, confirming metrics collection is working.</p>

<hr>

<h2>✅ 8. Deliverable</h2>

<p>
<strong>Deliverable:</strong><br>
✅ End-to-end monitoring, visualization, and alerting system operational using
Prometheus and Grafana in a KIND Kubernetes environment
</p>

<p>Successfully deployed components:</p>
<ul>
<li>✅ Monitoring namespace</li>
<li>✅ Prometheus server with RBAC</li>
<li>✅ Node Exporter (node-level metrics)</li>
<li>✅ cAdvisor (container-level metrics)</li>
<li>✅ kube-state-metrics (Kubernetes object metrics)</li>
<li>✅ All exporters configured and scraped by Prometheus</li>
</ul>

<hr>

<h2>🏁 9. Phase-5 Status</h2>

<p>
🟥 <strong>Phase-5 Completed</strong><br>
Monitoring &amp; Observability successfully implemented and validated.
</p>

<p>
<strong>Next:</strong> Proceed to <strong>Phase-6 – Documentation, Dashboards &amp; Demo</strong>
</p>

<hr>

<p><strong>— CloudOps Automation Project | Phase 5: Monitoring &amp; Observability</strong></p>

</body>
</html>
