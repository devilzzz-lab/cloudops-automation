<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>

<h1>🔍 Kubernetes Debug & Operations Commands Guide (README.md)</h1>

<p><strong>Version:</strong> Core Kubernetes Operations<br>
<strong>Module:</strong> Debugging, Troubleshooting & Management<br>
<strong>Project:</strong> CloudOps Automation, CI/CD &amp; Monitoring System</p>

<hr>

<h2>📌 1. Overview</h2>
<p>This guide covers essential Kubernetes commands for debugging, troubleshooting, and managing your CloudOps application deployed on Kubernetes. Master these commands to efficiently diagnose and resolve production issues [web:1].</p>

<p>Key areas covered:</p>
<ul>
  <li>✔ Log inspection and monitoring</li>
  <li>✔ Pod restart and rollout strategies</li>
  <li>✔ Resource inspection and debugging</li>
  <li>✔ Network troubleshooting</li>
  <li>✔ Scaling and cleanup operations</li>
</ul>

<hr>

<h2>🧪 2. LOG COMMANDS (MOST IMPORTANT)</h2>

<h3>📌 Basic Log Operations</h3>

<table border="1">
  <tr>
    <th>Command</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><code>kubectl logs cloudops-app-c9759b4d8-b585j -n cloudops</code></td>
    <td>View logs of a pod [web:1]</td>
  </tr>
  <tr>
    <td><code>kubectl logs cloudops-app-c9759b4d8-b585j -c cloudops-app -n cloudops</code></td>
    <td>View logs of a specific container (if multi-container pod) [web:1]</td>
  </tr>
  <tr>
    <td><code>kubectl logs -f cloudops-app-c9759b4d8-b585j -n cloudops</code></td>
    <td>Follow logs in real-time (like tail -f) [web:1]</td>
  </tr>
  <tr>
    <td><code>kubectl logs cloudops-app-c9759b4d8-b585j --previous -n cloudops</code></td>
    <td>View logs from previous crashed container [web:1]</td>
  </tr>
  <tr>
    <td><code>kubectl logs cloudops-app-c9759b4d8-b585j --tail=100 -n cloudops</code></td>
    <td>View last 100 lines of logs [web:1]</td>
  </tr>
  <tr>
    <td><code>kubectl logs cloudops-app-c9759b4d8-b585j --since=1h -n cloudops</code></td>
    <td>View logs from last 1 hour [web:1]</td>
  </tr>
</table>

<hr>

<h2>🔁 3. RESTART COMMANDS (VERY COMMON)</h2>

<h3>🔄 Restart Deployment (BEST WAY)</h3>

<table border="1">
  <tr>
    <th>Command</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><code>kubectl rollout restart deployment cloudops-app -n cloudops</code></td>
    <td>Gracefully restart all pods in deployment [web:1]</td>
  </tr>
  <tr>
    <td><code>kubectl rollout status deployment cloudops-app -n cloudops</code></td>
    <td>Check rollout status and progress [web:1]</td>
  </tr>
  <tr>
    <td><code>kubectl rollout history deployment cloudops-app -n cloudops</code></td>
    <td>View deployment revision history [web:1]</td>
  </tr>
  <tr>
    <td><code>kubectl rollout undo deployment cloudops-app -n cloudops</code></td>
    <td>Rollback to previous deployment version [web:1]</td>
  </tr>
</table>

<h3>❌ Can You Restart a Service?</h3>
<p><strong>NO.</strong> Services cannot be restarted because they are not processes [web:1]. They are network endpoints that route traffic to pods. You restart <strong>pods</strong>, not services.</p>

<hr>

<h2>🧨 4. DELETE POD (AUTO-RECREATED)</h2>

<table border="1">
  <tr>
    <th>Command</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><code>kubectl delete pod cloudops-app-c9759b4d8-b585j -n cloudops</code></td>
    <td>Delete ONE pod (Kubernetes immediately creates a new one) [web:1]</td>
  </tr>
  <tr>
    <td><code>kubectl delete pod -l app=cloudops-app -n cloudops</code></td>
    <td>Delete ALL app pods matching label [web:1]</td>
  </tr>
  <tr>
    <td><code>kubectl delete pod cloudops-app-c9759b4d8-b585j --now -n cloudops</code></td>
    <td>Delete pod immediately with no grace period [web:1]</td>
  </tr>
</table>

<p><strong>💡 Note:</strong> When you delete a pod managed by a Deployment, Kubernetes automatically creates a replacement pod to maintain desired replica count.</p>

<hr>

<h2>🔄 5. WHY POD NAME CHANGES? (INTERVIEW Q)</h2>

<h3>Example Pod Name Breakdown</h3>

<pre>
cloudops-app-c9759b4d8-b585j
</pre>

<table border="1">
  <tr>
    <th>Part</th>
    <th>Meaning</th>
  </tr>
  <tr>
    <td><code>cloudops-app</code></td>
    <td>Deployment name</td>
  </tr>
  <tr>
    <td><code>c9759b4d8</code></td>
    <td>ReplicaSet hash (unique to this version)</td>
  </tr>
  <tr>
    <td><code>b585j</code></td>
    <td>Random pod ID (unique per pod instance)</td>
  </tr>
</table>

<h3>🔁 When Pod Names Change:</h3>
<ul>
  <li>Image changes</li>
  <li>ConfigMap changes</li>
  <li>Deployment restarted</li>
  <li>Pod template updated</li>
</ul>

<p><strong>➡ Result:</strong> New ReplicaSet created → new hash → new pod names.</p>

<p><strong>Interview Answer:</strong> "Pod names change because Deployments create new ReplicaSets during updates, and each ReplicaSet has a unique hash identifier."</p>

<hr>

<h2>🧱 6. WHY StatefulSet POD NAME DOES NOT CHANGE?</h2>

<h3>Your DB Pod:</h3>
<pre>
cloudops-db-0
</pre>

<p>StatefulSet guarantees:</p>
<ul>
  <li>✅ Stable name</li>
  <li>✅ Stable network identity</li>
  <li>✅ Stable persistent storage</li>
</ul>

<p>That's why: <code>cloudops-db-0</code> ❌ <strong>never changes.</strong></p>

<p><strong>Interview Answer:</strong> "StatefulSets maintain stable pod identity, unlike Deployments. This is critical for stateful applications like databases that require consistent network identities and persistent storage."</p>

<hr>

<h2>🔍 7. INSPECTION COMMANDS (DEBUGGING)</h2>

<h3>Pod Information</h3>

<table border="1">
  <tr>
    <th>Command</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><code>kubectl get pods -n cloudops</code></td>
    <td>List all pods in namespace [web:1]</td>
  </tr>
  <tr>
    <td><code>kubectl get pods -n cloudops -o wide</code></td>
    <td>List pods with additional details (node, IP) [web:1]</td>
  </tr>
  <tr>
    <td><code>kubectl describe pod cloudops-app-c9759b4d8-b585j -n cloudops</code></td>
    <td>Show detailed pod information including events [web:1]</td>
  </tr>
  <tr>
    <td><code>kubectl get pod cloudops-app-c9759b4d8-b585j -n cloudops -o yaml</code></td>
    <td>View complete pod specification in YAML [web:1]</td>
  </tr>
  <tr>
    <td><code>kubectl get pods -n cloudops --watch</code></td>
    <td>Watch pod status changes in real-time [web:1]</td>
  </tr>
</table>

<h3>Deployment & Service Information</h3>

<table border="1">
  <tr>
    <th>Command</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><code>kubectl describe deployment cloudops-app -n cloudops</code></td>
    <td>Show deployment details and events [web:1]</td>
  </tr>
  <tr>
    <td><code>kubectl describe service cloudops-service -n cloudops</code></td>
    <td>Show service configuration and endpoints [web:1]</td>
  </tr>
  <tr>
    <td><code>kubectl get events -n cloudops --sort-by='.lastTimestamp'</code></td>
    <td>View recent events sorted by timestamp [web:1]</td>
  </tr>
  <tr>
    <td><code>kubectl top pods -n cloudops</code></td>
    <td>Show CPU and memory usage of pods [web:1]</td>
  </tr>
  <tr>
    <td><code>kubectl get all -n cloudops</code></td>
    <td>List all resources in namespace [web:1]</td>
  </tr>
</table>

<hr>

<h2>🧪 8. EXEC INTO POD (DEBUG INSIDE)</h2>

<table border="1">
  <tr>
    <th>Command</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><code>kubectl exec -it cloudops-app-c9759b4d8-b585j -n cloudops -- /bin/sh</code></td>
    <td>Execute interactive shell inside pod [web:1]</td>
  </tr>
  <tr>
    <td><code>kubectl exec -it cloudops-app-c9759b4d8-b585j -n cloudops -- /bin/bash</code></td>
    <td>Execute bash shell (if available) [web:1]</td>
  </tr>
  <tr>
    <td><code>kubectl exec cloudops-app-c9759b4d8-b585j -n cloudops -- env</code></td>
    <td>Check environment variables [web:1]</td>
  </tr>
  <tr>
    <td><code>kubectl exec cloudops-app-c9759b4d8-b585j -n cloudops -- ls -la /app</code></td>
    <td>List files in specific directory [web:1]</td>
  </tr>
</table>

<h3>Inside Pod Commands:</h3>
<pre>
# Check environment variables
env

# Check network connections
netstat -tuln

# Check DNS resolution
nslookup cloudops-service

# Exit shell
exit
</pre>

<hr>

<h2>🌐 9. NETWORK DEBUGGING</h2>

<table border="1">
  <tr>
    <th>Command</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><code>kubectl get endpoints -n cloudops</code></td>
    <td>Check service endpoints [web:1]</td>
  </tr>
  <tr>
    <td><code>kubectl get svc -n cloudops</code></td>
    <td>List all services [web:1]</td>
  </tr>
  <tr>
    <td><code>kubectl port-forward cloudops-app-c9759b4d8-b585j 8080:3000 -n cloudops</code></td>
    <td>Forward local port to pod port for testing [web:1]</td>
  </tr>
  <tr>
    <td><code>kubectl exec cloudops-app-c9759b4d8-b585j -n cloudops -- nslookup cloudops-service</code></td>
    <td>Test DNS resolution inside pod [web:1]</td>
  </tr>
</table>

<hr>

<h2>🔥 10. SCALE TESTING (IMPORTANT)</h2>

<table border="1">
  <tr>
    <th>Command</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><code>kubectl scale deployment cloudops-app --replicas=4 -n cloudops</code></td>
    <td>Scale UP to 4 replicas [web:1]</td>
  </tr>
  <tr>
    <td><code>kubectl scale deployment cloudops-app --replicas=1 -n cloudops</code></td>
    <td>Scale DOWN to 1 replica [web:1]</td>
  </tr>
  <tr>
    <td><code>kubectl autoscale deployment cloudops-app --min=2 --max=10 -n cloudops</code></td>
    <td>Auto-scale deployment based on CPU [web:1]</td>
  </tr>
</table>

<hr>

<h2>🧹 11. APPLY AGAIN (SAFE REDEPLOY)</h2>

<table border="1">
  <tr>
    <th>Command</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><code>kubectl apply -f k8s/</code></td>
    <td>Apply all manifests (Kubernetes updates only what changed) [web:1]</td>
  </tr>
  <tr>
    <td><code>kubectl diff -f k8s/</code></td>
    <td>Preview changes before applying [web:1]</td>
  </tr>
  <tr>
    <td><code>kubectl apply -f k8s/deployment.yaml</code></td>
    <td>Apply specific manifest file [web:1]</td>
  </tr>
</table>

<hr>

<h2>🧼 12. CLEANUP COMMANDS</h2>

<table border="1">
  <tr>
    <th>Command</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><code>kubectl delete deployment cloudops-app -n cloudops</code></td>
    <td>Delete deployment (and all its pods) [web:1]</td>
  </tr>
  <tr>
    <td><code>kubectl delete service cloudops-service -n cloudops</code></td>
    <td>Delete service [web:1]</td>
  </tr>
  <tr>
    <td><code>kubectl delete -f k8s/</code></td>
    <td>Delete all resources defined in manifests [web:1]</td>
  </tr>
  <tr>
    <td><code>kubectl delete namespace cloudops</code></td>
    <td>⚠️ DANGER: Delete entire namespace and all resources [web:1]</td>
  </tr>
</table>

<hr>

<h2>💡 13. TROUBLESHOOTING WORKFLOW</h2>

<h3>Step-by-Step Debug Process:</h3>

<ol>
  <li>
    <p><strong>Check pod status:</strong></p>
    <pre>kubectl get pods -n cloudops</pre>
  </li>
  <li>
    <p><strong>Describe problematic pod:</strong></p>
    <pre>kubectl describe pod &lt;pod-name&gt; -n cloudops</pre>
  </li>
  <li>
    <p><strong>Check logs:</strong></p>
    <pre>kubectl logs &lt;pod-name&gt; -n cloudops</pre>
  </li>
  <li>
    <p><strong>Check previous logs if crashed:</strong></p>
    <pre>kubectl logs &lt;pod-name&gt; --previous -n cloudops</pre>
  </li>
  <li>
    <p><strong>Exec into pod if running:</strong></p>
    <pre>kubectl exec -it &lt;pod-name&gt; -n cloudops -- /bin/sh</pre>
  </li>
  <li>
    <p><strong>Check events:</strong></p>
    <pre>kubectl get events -n cloudops --sort-by='.lastTimestamp'</pre>
  </li>
</ol>

<hr>

<h2>⚠️ 14. COMMON ISSUES & DEBUG COMMANDS</h2>

<table border="1">
  <tr>
    <th>Issue</th>
    <th>Debug Command</th>
    <th>What to Look For</th>
  </tr>
  <tr>
    <td>Pod not starting</td>
    <td><code>kubectl describe pod &lt;pod-name&gt; -n cloudops</code></td>
    <td>Check Events section for errors [web:1]</td>
  </tr>
  <tr>
    <td>CrashLoopBackOff</td>
    <td><code>kubectl logs &lt;pod-name&gt; --previous -n cloudops</code></td>
    <td>Application crash logs [web:1]</td>
  </tr>
  <tr>
    <td>ImagePullBackOff</td>
    <td><code>kubectl describe pod &lt;pod-name&gt; -n cloudops</code></td>
    <td>Image name/tag errors, registry access [web:1]</td>
  </tr>
  <tr>
    <td>Service not accessible</td>
    <td><code>kubectl get endpoints &lt;service-name&gt; -n cloudops</code></td>
    <td>Check if endpoints exist [web:1]</td>
  </tr>
  <tr>
    <td>ConfigMap not loaded</td>
    <td><code>kubectl exec &lt;pod-name&gt; -n cloudops -- env</code></td>
    <td>Verify environment variables [web:1]</td>
  </tr>
  <tr>
    <td>High memory/CPU</td>
    <td><code>kubectl top pods -n cloudops</code></td>
    <td>Resource usage metrics [web:1]</td>
  </tr>
</table>

<hr>

<h2>🧠 15. FINAL INTERVIEW CHEAT ANSWERS</h2>

<table border="1">
  <tr>
    <th>Question</th>
    <th>Answer</th>
  </tr>
  <tr>
    <td>How do you restart an app in Kubernetes?</td>
    <td>Using <code>kubectl rollout restart deployment &lt;name&gt;</code> - this performs a graceful rolling restart [web:1]</td>
  </tr>
  <tr>
    <td>Why do pod names change?</td>
    <td>Because Deployments create new ReplicaSets during updates, and each ReplicaSet has a unique hash identifier</td>
  </tr>
  <tr>
    <td>Why don't StatefulSet pods change names?</td>
    <td>StatefulSets maintain stable pod identity and persistent storage, providing ordinal naming (pod-0, pod-1, etc.)</td>
  </tr>
  <tr>
    <td>How do you check pod logs?</td>
    <td><code>kubectl logs &lt;pod-name&gt; -n &lt;namespace&gt;</code> for current logs, add <code>--previous</code> flag for crashed containers [web:1]</td>
  </tr>
  <tr>
    <td>How do you debug a failing pod?</td>
    <td>1. Check status with <code>get pods</code> 2. Describe pod for events 3. Check logs 4. Exec into pod if running [web:1]</td>
  </tr>
  <tr>
    <td>Can you restart a Kubernetes Service?</td>
    <td>No, services are not processes and cannot be restarted. You restart pods, not services [web:1]</td>
  </tr>
</table>

<hr>

<h2>🔥 16. YOU ARE OFFICIALLY DONE WITH CORE KUBERNETES</h2>

<p>Congratulations! You now have a complete understanding of Kubernetes debugging and operations.</p>

<h3>Next Steps:</h3>
<ol>
  <li>✅ Add Jenkins automation (CI/CD Pipeline)</li>
  <li>✅ Add Prometheus + Grafana (Monitoring)</li>
  <li>✅ Do rolling update demo</li>
  <li>✅ Prepare interview Q&amp;A from your project</li>
</ol>

<p><strong>Choose your next phase:</strong></p>
<ul>
  <li><strong>Next: Jenkins</strong> - Automate your deployments with CI/CD</li>
  <li><strong>Next: Monitoring</strong> - Set up Prometheus and Grafana for observability</li>
</ul>

<hr>

<h2>📚 Quick Reference Summary</h2>

<table border="1">
  <tr>
    <th>Category</th>
    <th>Most Important Commands</th>
  </tr>
  <tr>
    <td>Logs</td>
    <td><code>kubectl logs -f &lt;pod&gt; -n cloudops</code></td>
  </tr>
  <tr>
    <td>Restart</td>
    <td><code>kubectl rollout restart deployment &lt;name&gt; -n cloudops</code></td>
  </tr>
  <tr>
    <td>Debug</td>
    <td><code>kubectl describe pod &lt;pod&gt; -n cloudops</code></td>
  </tr>
  <tr>
    <td>Exec</td>
    <td><code>kubectl exec -it &lt;pod&gt; -n cloudops -- /bin/sh</code></td>
  </tr>
  <tr>
    <td>Scale</td>
    <td><code>kubectl scale deployment &lt;name&gt; --replicas=N -n cloudops</code></td>
  </tr>
  <tr>
    <td>Status</td>
    <td><code>kubectl get pods -n cloudops -o wide</code></td>
  </tr>
</table>

</body>
</html>
