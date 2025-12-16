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

<h2>✅ 7. Deliverable</h2>

<p>
<strong>Deliverable:</strong><br>
✅ End-to-end monitoring, visualization, and alerting system operational using
Prometheus and Grafana in a KIND Kubernetes environment
</p>

<hr>

<h2>🏁 8. Phase-5 Status</h2>

<p>
🟥 <strong>Phase-5 Completed</strong><br>
Monitoring &amp; Observability successfully implemented and validated.
</p>

<p>
<strong>Next:</strong> Proceed to <strong>Phase-6 – Documentation, Dashboards &amp; Demo</strong>
</p>

</body>
</html>
