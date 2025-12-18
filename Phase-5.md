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

<h3>🟥 STEP 2 – Deploy Prometheus with RBAC</h3>

<h4>🎯 Objective</h4>
<p>Deploy Prometheus server with proper RBAC permissions to enable Kubernetes service discovery for metrics collection.</p>

<p><strong>2.1: Create directory structure</strong></p>
<pre>
mkdir -p monitoring/prometheus
cd monitoring/prometheus
</pre>

<p><strong>2.2: Create Prometheus RBAC</strong></p>
<p>📄 File: <code>monitoring/prometheus/prometheus-rbac.yaml</code></p>
<p>This file contains ServiceAccount, ClusterRole, and ClusterRoleBinding for Prometheus.</p>

<p><strong>2.3: Apply Prometheus RBAC</strong></p>
<pre>
kubectl apply -f monitoring/prometheus/prometheus-rbac.yaml
</pre>

<p><strong>2.4: Create Prometheus ConfigMap</strong></p>
<p>📄 File: <code>monitoring/prometheus/prometheus-config.yaml</code></p>

<p><strong>2.5: Create Prometheus Deployment</strong></p>
<p>📄 File: <code>monitoring/prometheus/prometheus-deployment.yaml</code></p>
<p><strong>Note:</strong> Ensure <code>serviceAccountName: prometheus</code> is added under <code>spec.template.spec</code></p>

<p><strong>2.6: Create Prometheus Service</strong></p>
<p>📄 File: <code>monitoring/prometheus/prometheus-service.yaml</code></p>

<p><strong>2.7: Apply Prometheus manifests</strong></p>
<pre>
kubectl apply -f monitoring/prometheus/
</pre>

<p><strong>2.8: Verify Prometheus Deployment</strong></p>
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

<h3>🟥 STEP 7 – Verify Prometheus Targets</h3>

<h4>🎯 Objective</h4>
<p>Update Prometheus scrape configuration to collect metrics from all exporters deployed in previous steps.</p>

<p><strong>7.1: Update Prometheus ConfigMap</strong></p>
<p>📄 File: <code>monitoring/prometheus/prometheus-config.yaml</code></p>
<p>Update the file to include scrape configs for Node Exporter, cAdvisor, and kube-state-metrics using Kubernetes service discovery.</p>

<p><strong>7.2: Apply Updated ConfigMap</strong></p>
<pre>
kubectl apply -f monitoring/prometheus/prometheus-config.yaml
</pre>

<p><strong>7.3: Restart Prometheus</strong></p>
<pre>
kubectl rollout restart deployment prometheus -n monitoring
</pre>

<p><strong>7.4: Verify Prometheus Targets</strong></p>
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

<p><strong>7.5: Quick PromQL Tests (Optional)</strong></p>
<p>In Prometheus UI → Graph, test these queries:</p>
<pre>
up
node_cpu_seconds_total
container_cpu_usage_seconds_total
kube_pod_status_phase
</pre>

<p><strong>Expected:</strong> Data appears for all queries, confirming metrics collection is working.</p>

<hr>

<h3>🟥 STEP 8 – Deploy Grafana</h3>

<h4>🎯 Objective</h4>
<p>Deploy Grafana inside the monitoring namespace for metrics visualization and dashboard creation.</p>

<p><strong>8.1: Create Grafana Deployment</strong></p>
<p>📄 File: <code>monitoring/grafana/grafana-deployment.yaml</code></p>

<p><strong>8.2: Create Grafana Service</strong></p>
<p>📄 File: <code>monitoring/grafana/grafana-service.yaml</code></p>

<p><strong>8.3: Apply Grafana Manifests</strong></p>
<pre>
kubectl apply -f monitoring/grafana/
</pre>

<p><strong>8.4: Verify Grafana Deployment</strong></p>
<pre>
kubectl get pods -n monitoring
kubectl get svc -n monitoring
</pre>

<p><strong>Expected output:</strong></p>
<pre>
grafana-xxxxx   1/1   Running
grafana         NodePort   3000:32000/TCP
</pre>

<p><strong>8.5: Access Grafana UI</strong></p>
<p>Due to KIND networking on macOS, use port-forward to access Grafana:</p>
<pre>
kubectl port-forward -n monitoring svc/grafana 3000:3000
</pre>

<p>Open browser: <code>http://localhost:3000</code></p>

<p><strong>Default Login:</strong></p>
<ul>
<li>Username: <code>admin</code></li>
<li>Password: <code>admin</code></li>
</ul>

<p><strong>Note:</strong> Change the password when prompted.</p>

<hr>

<h3>🟥 STEP 9 – Expose Grafana Service</h3>

<h4>🎯 Objective</h4>
<p>Connect Grafana to Prometheus to enable metrics querying and dashboard visualization.</p>

<p><strong>9.1: Navigate to Data Sources</strong></p>
<p>In Grafana UI:</p>
<ol>
<li>Click ⚙️ <strong>Configuration</strong></li>
<li>Click <strong>Data sources</strong></li>
<li>Click <strong>Add data source</strong></li>
<li>Select <strong>Prometheus</strong></li>
</ol>

<p><strong>9.2: Configure Prometheus Data Source</strong></p>
<ul>
<li>Name: <code>Prometheus</code></li>
<li>URL: <code>http://prometheus.monitoring.svc.cluster.local:9090</code></li>
</ul>

<p><strong>9.3: Save & Test</strong></p>
<p>Click <strong>Save & test</strong></p>
<p><strong>Expected message:</strong> "Data source is working"</p>

<hr>

<h3>🟥 STEP 10 – Add Prometheus Datasource in Grafana</h3>

<h4>🎯 Objective</h4>
<p>Import a pre-built Grafana dashboard to visualize Kubernetes cluster metrics including node CPU, memory, disk, and network usage.</p>

<p><strong>10.1: Open Dashboard Import</strong></p>
<p>In Grafana UI:</p>
<ol>
<li>Click ➕ <strong>Create</strong></li>
<li>Click <strong>Import</strong></li>
</ol>

<p><strong>10.2: Import Dashboard by ID</strong></p>
<p>Enter Dashboard ID: <code>1860</code></p>
<p>Click <strong>Load</strong></p>

<p><strong>10.3: Configure Import</strong></p>
<ul>
<li>Name: <code>Node Exporter Full</code> (or keep default)</li>
<li>Data Source: Select <strong>Prometheus</strong></li>
</ul>
<p>Click <strong>Import</strong></p>

<p><strong>10.4: Verify Dashboard</strong></p>
<p>Dashboard should display live metrics for:</p>
<ul>
<li>Node CPU usage</li>
<li>Node memory usage</li>
<li>Filesystem usage</li>
<li>Network I/O</li>
</ul>

<hr>

<h3>🟥 STEP 11 – Import Cluster Overview Dashboard</h3>

<h4>🎯 Objective</h4>
<p>Visualize pod-level metrics including CPU, memory, network, and Kubernetes workload health.</p>

<p><strong>11.1: Open Dashboard Import</strong></p>
<p>In Grafana UI:</p>
<ol>
<li>Click ➕ <strong>Create</strong></li>
<li>Click <strong>Import</strong></li>
</ol>

<p><strong>11.2: Import Dashboard by ID</strong></p>
<p>Enter Dashboard ID: <code>15760</code></p>
<p>Click <strong>Load</strong></p>

<p><strong>11.3: Configure Import</strong></p>
<ul>
<li>Name: <code>Kubernetes / Pods</code> (or keep default)</li>
<li>Data Source: Select <strong>Prometheus</strong></li>
</ul>
<p>Click <strong>Import</strong></p>

<p><strong>11.4: Verify Dashboard</strong></p>
<p>Dashboard filters:</p>
<ul>
<li>Namespace: <code>monitoring</code></li>
<li>Pod: Select any pod or <code>All</code></li>
</ul>

<p><strong>Expected:</strong> Pod list visible, network metrics visible. Some resource panels may show limited data in infrastructure-only setups (this is normal).</p>

<hr>

<h3>🟥 STEP 12 – Import Workloads Dashboard</h3>

<h4>🎯 Objective</h4>
<p>Prepare a future-ready application health dashboard to monitor HTTP metrics, error rates, latency, and availability.</p>

<p><strong>12.1: Create New Dashboard</strong></p>
<p>In Grafana UI:</p>
<ol>
<li>Go to <strong>Dashboards → New → New Dashboard</strong></li>
<li>Click <strong>Add a new panel</strong></li>
<li>Select Datasource: <strong>Prometheus</strong></li>
</ol>

<p><strong>12.2: Add Application Health Panels</strong></p>

<p><strong>Panel 1 – Application Availability</strong></p>
<pre>up</pre>

<p><strong>Panel 2 – HTTP Request Rate (Template)</strong></p>
<pre>sum(rate(http_requests_total[1m]))</pre>

<p><strong>Panel 3 – HTTP Error Rate (Template)</strong></p>
<pre>sum(rate(http_requests_total{status=~"5.."}[1m]))</pre>

<p><strong>Panel 4 – Application Latency (Template)</strong></p>
<pre>histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))</pre>

<p><strong>12.3: Save Dashboard</strong></p>
<ul>
<li>Name: <code>Application Health – Prometheus</code></li>
<li>Folder: <code>Monitoring</code></li>
</ul>
<p>Click <strong>Save</strong></p>

<p><strong>Note:</strong> Panels may show "No data" until applications expose Prometheus metrics endpoints.</p>

<hr>

<h3>🟥 STEP 13 – Create Application Health Dashboard</h3>

<h4>🎯 Objective</h4>
<p>Create a dashboard to visualize Kubernetes deployment behavior during rollouts, including pod availability, restarts, and resource usage.</p>

<p><strong>13.1: Create New Dashboard</strong></p>
<p>In Grafana UI:</p>
<ol>
<li>Go to <strong>Dashboards → New → New Dashboard</strong></li>
<li>Click <strong>Add a new panel</strong></li>
<li>Datasource: <strong>Prometheus</strong></li>
</ol>

<p><strong>13.2: Add Deployment Impact Panels</strong></p>

<p><strong>Panel 1 – Available vs Desired Replicas</strong></p>
<pre>kube_deployment_status_replicas_available</pre>

<p><strong>Panel 2 – Desired Replicas</strong></p>
<pre>kube_deployment_spec_replicas</pre>

<p><strong>Panel 3 – Pod Restart Count</strong></p>
<pre>increase(kube_pod_container_status_restarts_total[5m])</pre>

<p><strong>Panel 4 – CPU Usage Spike After Deployment</strong></p>
<pre>sum(rate(container_cpu_usage_seconds_total[2m])) by (pod)</pre>

<p><strong>Panel 5 – Memory Usage Spike</strong></p>
<pre>sum(container_memory_usage_bytes) by (pod)</pre>

<p><strong>13.3: Save Dashboard</strong></p>
<ul>
<li>Name: <code>Deployment Impact – Kubernetes</code></li>
<li>Folder: <code>Monitoring</code></li>
<li>Time range: <code>Last 1 hour</code></li>
<li>Refresh: <code>10s</code></li>
</ul>
<p>Click <strong>Save</strong></p>

<p><strong>Note:</strong> Panels populate with data during actual deployment rollouts from CI/CD pipeline.</p>

<hr>

<h3>🟥 STEP 14 – Create Deployment Impact Dashboard</h3>

<h4>🎯 Objective</h4>
<p>Configure Prometheus alert rules to detect infrastructure and workload anomalies.</p>

<p><strong>14.1: Create Prometheus Alert Rules</strong></p>
<p>📄 File: <code>monitoring/prometheus/prometheus-alerts.yaml</code></p>
<p>Define alert rules for pod availability, CPU usage, memory usage, and container restarts.</p>

<p><strong>14.2: Apply Alert Rules</strong></p>
<pre>
kubectl create configmap prometheus-alerts \
  --from-file=monitoring/prometheus/prometheus-alerts.yaml \
  -n monitoring
</pre>

<p><strong>14.3: Update Prometheus ConfigMap</strong></p>
<p>Add <code>rule_files</code> section to <code>prometheus-config.yaml</code> to load alert rules.</p>

<p><strong>14.4: Restart Prometheus</strong></p>
<pre>
kubectl rollout restart deployment prometheus -n monitoring
</pre>

<p><strong>14.5: Verify Alerts</strong></p>
<p>Access Prometheus UI:</p>
<pre>
kubectl port-forward -n monitoring svc/prometheus 9090:9090
</pre>
<p>Navigate to: <code>http://localhost:9090/alerts</code></p>
<p><strong>Expected:</strong> Alert rules loaded and visible.</p>

<hr>

<h3>🟥 STEP 15 – Configure Prometheus Alert Rules</h3>

<h4>🎯 Objective</h4>
<p>Deploy Alertmanager to handle alert routing and notifications.</p>

<p><strong>15.1: Create Alertmanager ConfigMap</strong></p>
<p>📄 File: <code>monitoring/alertmanager/alertmanager-config.yaml</code></p>

<p><strong>15.2: Create Alertmanager Deployment</strong></p>
<p>📄 File: <code>monitoring/alertmanager/alertmanager-deployment.yaml</code></p>

<p><strong>15.3: Create Alertmanager Service</strong></p>
<p>📄 File: <code>monitoring/alertmanager/alertmanager-service.yaml</code></p>

<p><strong>15.4: Apply Alertmanager Manifests</strong></p>
<pre>
kubectl apply -f monitoring/alertmanager/
</pre>

<p><strong>15.5: Verify Alertmanager Deployment</strong></p>
<pre>
kubectl get pods -n monitoring
</pre>

<p><strong>Expected output:</strong></p>
<pre>
alertmanager-xxxxx   1/1   Running
</pre>

<hr>

<h3>🟥 STEP 16 – Deploy Alertmanager</h3>

<h4>🎯 Objective</h4>
<p>Test alert functionality by simulating a pod failure or resource spike.</p>

<p><strong>16.1: Simulate Pod Down</strong></p>
<pre>
kubectl scale deployment grafana --replicas=0 -n monitoring
</pre>

<p><strong>16.2: Check Prometheus Alerts</strong></p>
<p>Access Prometheus UI and verify alert is firing:</p>
<pre>
kubectl port-forward -n monitoring svc/prometheus 9090:9090
</pre>
<p>Navigate to: <code>http://localhost:9090/alerts</code></p>

<p><strong>16.3: Restore Pod</strong></p>
<pre>
kubectl scale deployment grafana --replicas=1 -n monitoring
</pre>

<p><strong>16.4: Verify Alert Resolved</strong></p>
<p>Check that alert status changes to resolved in Prometheus UI.</p>

<hr>

<h3>🟥 STEP 17 – Test Alerts (CPU / Pod Down)</h3>

<h4>🎯 Objective</h4>
<p>Document all monitoring components, dashboards, and alert configurations for Phase 5.</p>

<p><strong>17.1: Update PHASE-5.md</strong></p>
<p>Document all steps, configurations, and verification procedures in the Phase 5 markdown file.</p>

<p><strong>17.2: Export Grafana Dashboards</strong></p>
<p>Export dashboard JSON files for version control:</p>
<ul>
<li>Node Exporter Full</li>
<li>Kubernetes Pods</li>
<li>Application Health</li>
<li>Deployment Impact</li>
</ul>

<p><strong>17.3: Document Alert Rules</strong></p>
<p>Include all Prometheus alert rule definitions and expected behavior in documentation.</p>

<p><strong>17.4: Commit to Repository</strong></p>
<pre>
git add monitoring/
git commit -m "Phase 5: Complete monitoring & observability stack"
git push origin main
</pre>

<hr>

<h3>🟥 STEP 18 – Document Dashboards & Alerts</h3>

<h4>🎯 Objective</h4>
<p>Perform end-to-end validation of the entire Phase 5 monitoring stack.</p>

<p><strong>18.1: Verify All Components Running</strong></p>
<pre>
kubectl get pods -n monitoring
</pre>
<p><strong>Expected:</strong> All pods in <code>Running</code> state.</p>

<p><strong>18.2: Verify Prometheus Targets</strong></p>
<p>All targets should be <strong>UP</strong> in Prometheus UI.</p>

<p><strong>18.3: Verify Grafana Dashboards</strong></p>
<p>Access all dashboards and confirm metrics are populating.</p>

<p><strong>18.4: Verify Alerts</strong></p>
<p>Confirm alert rules are loaded and can be triggered.</p>

<p><strong>18.5: Update Phase 5 Status</strong></p>
<p>Mark Phase 5 as <strong>Completed</strong> in project documentation.</p>

<hr>

<h3>🟥 STEP 19 – Phase 5 Validation Complete</h3>

<h4>🎯 Objective</h4>
<p>Final validation and sign-off for Phase 5 completion.</p>

<p><strong>19.1: Final Component Check</strong></p>
<pre>
kubectl get all -n monitoring
</pre>

<p><strong>19.2: Verify All Metrics & Dashboards</strong></p>
<p>Ensure all metrics are collecting and all dashboards are functional.</p>

<p><strong>19.3: Documentation Complete</strong></p>
<p>Confirm PHASE-5.md is updated with all steps and verification procedures.</p>

<p><strong>19.4: Phase 5 Sign-Off</strong></p>
<p>Phase 5 is now complete and ready for demo or migration to production (EKS).</p>

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
<li>✅ Grafana with multiple dashboards</li>
<li>✅ Alertmanager with configured alert rules</li>
<li>✅ All exporters configured and scraped by Prometheus</li>
<li>✅ Complete documentation and validation</li>
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
