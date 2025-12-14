<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kubernetes Debug Commands Cheat Sheet</title>
</head>
<body>
    <h1>🔍 Kubernetes Debug Commands Reference</h1>
    
    <h2>📋 Pod Information & Status</h2>
    <table border="1" cellpadding="10" cellspacing="0">
        <thead>
            <tr>
                <th>Command</th>
                <th>Description</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><code>kubectl get pods -n cloudops</code></td>
                <td>List all pods in the namespace</td>
            </tr>
            <tr>
                <td><code>kubectl get pods -n cloudops -o wide</code></td>
                <td>List pods with additional details (node, IP, etc.)</td>
            </tr>
            <tr>
                <td><code>kubectl describe pod &lt;pod-name&gt; -n cloudops</code></td>
                <td>Show detailed information including events and status</td>
            </tr>
            <tr>
                <td><code>kubectl get pods --all-namespaces</code></td>
                <td>List all pods across all namespaces</td>
            </tr>
            <tr>
                <td><code>kubectl get pods -n cloudops --watch</code></td>
                <td>Watch pod status in real-time</td>
            </tr>
        </tbody>
    </table>

    <h2>📝 Log Commands</h2>
    <table border="1" cellpadding="10" cellspacing="0">
        <thead>
            <tr>
                <th>Command</th>
                <th>Description</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><code>kubectl logs &lt;pod-name&gt; -n cloudops</code></td>
                <td>View logs of a pod</td>
            </tr>
            <tr>
                <td><code>kubectl logs &lt;pod-name&gt; -c &lt;container-name&gt; -n cloudops</code></td>
                <td>View logs of specific container in multi-container pod</td>
            </tr>
            <tr>
                <td><code>kubectl logs -f &lt;pod-name&gt; -n cloudops</code></td>
                <td>Follow logs in real-time (like tail -f)</td>
            </tr>
            <tr>
                <td><code>kubectl logs &lt;pod-name&gt; --previous -n cloudops</code></td>
                <td>View logs from previous crashed container</td>
            </tr>
            <tr>
                <td><code>kubectl logs &lt;pod-name&gt; --tail=100 -n cloudops</code></td>
                <td>View last 100 lines of logs</td>
            </tr>
            <tr>
                <td><code>kubectl logs &lt;pod-name&gt; --since=1h -n cloudops</code></td>
                <td>View logs from last 1 hour</td>
            </tr>
        </tbody>
    </table>

    <h2>🔧 Interactive Debugging</h2>
    <table border="1" cellpadding="10" cellspacing="0">
        <thead>
            <tr>
                <th>Command</th>
                <th>Description</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><code>kubectl exec -it &lt;pod-name&gt; -n cloudops -- /bin/sh</code></td>
                <td>Execute shell inside pod for debugging</td>
            </tr>
            <tr>
                <td><code>kubectl exec -it &lt;pod-name&gt; -n cloudops -- /bin/bash</code></td>
                <td>Execute bash shell (if available)</td>
            </tr>
            <tr>
                <td><code>kubectl exec &lt;pod-name&gt; -n cloudops -- env</code></td>
                <td>Check environment variables inside pod</td>
            </tr>
            <tr>
                <td><code>kubectl exec &lt;pod-name&gt; -n cloudops -- ls -la /app</code></td>
                <td>List files in specific directory</td>
            </tr>
            <tr>
                <td><code>kubectl debug &lt;pod-name&gt; -it --image=busybox -n cloudops</code></td>
                <td>Create debug container attached to pod</td>
            </tr>
        </tbody>
    </table>

    <h2>🔍 Resource Inspection</h2>
    <table border="1" cellpadding="10" cellspacing="0">
        <thead>
            <tr>
                <th>Command</th>
                <th>Description</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><code>kubectl describe deployment &lt;deployment-name&gt; -n cloudops</code></td>
                <td>Show deployment details and events</td>
            </tr>
            <tr>
                <td><code>kubectl describe service &lt;service-name&gt; -n cloudops</code></td>
                <td>Show service details and endpoints</td>
            </tr>
            <tr>
                <td><code>kubectl get events -n cloudops --sort-by='.lastTimestamp'</code></td>
                <td>View recent events sorted by time</td>
            </tr>
            <tr>
                <td><code>kubectl top pods -n cloudops</code></td>
                <td>Show CPU and memory usage of pods</td>
            </tr>
            <tr>
                <td><code>kubectl top nodes</code></td>
                <td>Show node resource usage</td>
            </tr>
        </tbody>
    </table>

    <h2>🌐 Network Debugging</h2>
    <table border="1" cellpadding="10" cellspacing="0">
        <thead>
            <tr>
                <th>Command</th>
                <th>Description</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><code>kubectl get endpoints -n cloudops</code></td>
                <td>Check service endpoints</td>
            </tr>
            <tr>
                <td><code>kubectl get svc -n cloudops</code></td>
                <td>List all services</td>
            </tr>
            <tr>
                <td><code>kubectl describe svc &lt;service-name&gt; -n cloudops</code></td>
                <td>Show service configuration and endpoints</td>
            </tr>
            <tr>
                <td><code>kubectl port-forward &lt;pod-name&gt; 8080:3000 -n cloudops</code></td>
                <td>Forward local port to pod port for testing</td>
            </tr>
            <tr>
                <td><code>kubectl exec &lt;pod-name&gt; -n cloudops -- nslookup &lt;service-name&gt;</code></td>
                <td>Test DNS resolution inside pod</td>
            </tr>
        </tbody>
    </table>

    <h2>📊 ConfigMap & Secret Debugging</h2>
    <table border="1" cellpadding="10" cellspacing="0">
        <thead>
            <tr>
                <th>Command</th>
                <th>Description</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><code>kubectl get configmap -n cloudops</code></td>
                <td>List all ConfigMaps</td>
            </tr>
            <tr>
                <td><code>kubectl describe configmap &lt;configmap-name&gt; -n cloudops</code></td>
                <td>Show ConfigMap contents</td>
            </tr>
            <tr>
                <td><code>kubectl get secret -n cloudops</code></td>
                <td>List all secrets</td>
            </tr>
            <tr>
                <td><code>kubectl describe secret &lt;secret-name&gt; -n cloudops</code></td>
                <td>Show secret metadata (not values)</td>
            </tr>
            <tr>
                <td><code>kubectl get configmap &lt;configmap-name&gt; -n cloudops -o yaml</code></td>
                <td>View ConfigMap in YAML format</td>
            </tr>
        </tbody>
    </table>

    <h2>⚠️ Troubleshooting Pod Issues</h2>
    <table border="1" cellpadding="10" cellspacing="0">
        <thead>
            <tr>
                <th>Command</th>
                <th>Description</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><code>kubectl get pods -n cloudops | grep -v Running</code></td>
                <td>Find pods not in Running state</td>
            </tr>
            <tr>
                <td><code>kubectl get pods -n cloudops --field-selector=status.phase!=Running</code></td>
                <td>List non-running pods</td>
            </tr>
            <tr>
                <td><code>kubectl describe pod &lt;pod-name&gt; -n cloudops | grep -A 10 Events</code></td>
                <td>Check recent pod events</td>
            </tr>
            <tr>
                <td><code>kubectl get pod &lt;pod-name&gt; -n cloudops -o yaml</code></td>
                <td>View complete pod specification</td>
            </tr>
            <tr>
                <td><code>kubectl rollout history deployment &lt;deployment-name&gt; -n cloudops</code></td>
                <td>View deployment revision history</td>
            </tr>
        </tbody>
    </table>

    <h2>🔄 Resource State Commands</h2>
    <table border="1" cellpadding="10" cellspacing="0">
        <thead>
            <tr>
                <th>Command</th>
                <th>Description</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><code>kubectl get all -n cloudops</code></td>
                <td>List all resources in namespace</td>
            </tr>
            <tr>
                <td><code>kubectl api-resources</code></td>
                <td>List all available resource types</td>
            </tr>
            <tr>
                <td><code>kubectl explain pod.spec.containers</code></td>
                <td>Get documentation for resource fields</td>
            </tr>
            <tr>
                <td><code>kubectl diff -f k8s/</code></td>
                <td>Preview changes before applying</td>
            </tr>
        </tbody>
    </table>

    <h2>💡 Quick Debug Workflow</h2>
    <ol>
        <li>Check pod status: <code>kubectl get pods -n cloudops</code></li>
        <li>Describe problematic pod: <code>kubectl describe pod &lt;pod-name&gt; -n cloudops</code></li>
        <li>Check logs: <code>kubectl logs &lt;pod-name&gt; -n cloudops</code></li>
        <li>Check previous logs if crashed: <code>kubectl logs &lt;pod-name&gt; --previous -n cloudops</code></li>
        <li>Exec into pod if running: <code>kubectl exec -it &lt;pod-name&gt; -n cloudops -- /bin/sh</code></li>
        <li>Check events: <code>kubectl get events -n cloudops --sort-by='.lastTimestamp'</code></li>
    </ol>

    <h2>🎯 Common Issues & Debug Commands</h2>
    <table border="1" cellpadding="10" cellspacing="0">
        <thead>
            <tr>
                <th>Issue</th>
                <th>Debug Command</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Pod not starting</td>
                <td><code>kubectl describe pod &lt;pod-name&gt; -n cloudops</code></td>
            </tr>
            <tr>
                <td>CrashLoopBackOff</td>
                <td><code>kubectl logs &lt;pod-name&gt; --previous -n cloudops</code></td>
            </tr>
            <tr>
                <td>ImagePullBackOff</td>
                <td><code>kubectl describe pod &lt;pod-name&gt; -n cloudops | grep -A 5 Events</code></td>
            </tr>
            <tr>
                <td>Service not accessible</td>
                <td><code>kubectl get endpoints &lt;service-name&gt; -n cloudops</code></td>
            </tr>
            <tr>
                <td>ConfigMap not loaded</td>
                <td><code>kubectl exec &lt;pod-name&gt; -n cloudops -- env</code></td>
            </tr>
            <tr>
                <td>High memory/CPU</td>
                <td><code>kubectl top pods -n cloudops</code></td>
            </tr>
        </tbody>
    </table>

</body>
</html>
