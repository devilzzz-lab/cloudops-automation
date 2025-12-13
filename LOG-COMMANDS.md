🧪 1️⃣ LOG COMMANDS (MOST IMPORTANT)
📌 Logs of a pod
kubectl logs cloudops-app-c9759b4d8-b585j -n cloudops
📌 Logs of a container (if multi-container pod)
kubectl logs cloudops-app-c9759b4d8-b585j -c cloudops-app -n cloudops
📌 Follow logs (like tail -f)
kubectl logs -f cloudops-app-c9759b4d8-b585j -n cloudops
📌 Previous crash logs
kubectl logs cloudops-app-c9759b4d8-b585j --previous -n cloudops
🔁 2️⃣ RESTART COMMANDS (VERY COMMON)
🔄 Restart Deployment (BEST WAY)
kubectl rollout restart deployment cloudops-app -n cloudops
🔍 Check rollout status
kubectl rollout status deployment cloudops-app -n cloudops
❌ Restart Service?
❌ Services cannot be restarted
They are not processes.
👉 You restart pods, not services.
🧨 3️⃣ DELETE POD (AUTO-RECREATED)
Delete ONE pod
kubectl delete pod cloudops-app-c9759b4d8-b585j -n cloudops
👉 Kubernetes immediately creates a new pod.
Delete ALL app pods
kubectl delete pod -l app=cloudops-app -n cloudops
🔄 4️⃣ WHY POD NAME CHANGES? (INTERVIEW Q)
Example pod name:
cloudops-app-c9759b4d8-b585j
Breakdown:
Part	Meaning
cloudops-app	Deployment name
c9759b4d8	ReplicaSet hash
b585j	Random pod ID
🔁 When:
Image changes
ConfigMap changes
Deployment restarted
➡ New ReplicaSet created → new hash → new pod names.
🧱 5️⃣ WHY StatefulSet POD NAME DOES NOT CHANGE?
Your DB pod:
cloudops-db-0
StatefulSet guarantees:
Stable name
Stable network identity
Stable storage
That’s why:
cloudops-db-0
❌ never changes.
Interview answer:
“StatefulSets maintain stable pod identity, unlike Deployments.”
🧹 6️⃣ APPLY AGAIN (SAFE REDEPLOY)
Apply everything again
kubectl apply -f k8s/
Kubernetes updates only what changed.
🔍 7️⃣ INSPECTION COMMANDS (DEBUGGING)
Get pods
kubectl get pods -n cloudops
Describe pod (events)
kubectl describe pod cloudops-app-c9759b4d8-b585j -n cloudops
Check deployment
kubectl describe deployment cloudops-app -n cloudops
🧪 8️⃣ EXEC INTO POD (DEBUG INSIDE)
kubectl exec -it cloudops-app-c9759b4d8-b585j -n cloudops -- /bin/sh
Inside pod:
env
netstat -tuln
Exit:
exit
🔥 9️⃣ SCALE TESTING (IMPORTANT)
Scale UP
kubectl scale deployment cloudops-app --replicas=4 -n cloudops
Scale DOWN
kubectl scale deployment cloudops-app --replicas=1 -n cloudops
🧼 🔟 CLEANUP COMMANDS
Delete deployment
kubectl delete deployment cloudops-app -n cloudops
Delete namespace (DANGER ⚠️)
kubectl delete namespace cloudops
🧠 FINAL INTERVIEW CHEAT ANSWERS
Q: How do you restart an app in Kubernetes?
Using kubectl rollout restart deployment <name>
Q: Why pod names change?
Because Deployments create new ReplicaSets during updates.
Q: Why StatefulSet pods don’t change?
They have stable identity and persistent storage.
🔥 YOU ARE OFFICIALLY DONE WITH CORE KUBERNETES
Next we can:
1️⃣ Add Jenkins automation
2️⃣ Add Prometheus + Grafana
3️⃣ Do rolling update demo
4️⃣ Prepare interview Q&A from your project
Say:
Next: Jenkins
or
Next: Monitoring