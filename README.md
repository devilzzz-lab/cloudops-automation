<html lang="en">
<head>
  <meta charset="utf-8" />
</head>
<body>


  <h1>CloudOps Automation — Project</h1>


  <p><strong>Status:</strong> <em>Phase 4 (Kubernetes Deployment on AWS EKS)</em> <strong>in progress</strong>. Phases 1-3 completed. Remaining Phases 5-6 pending.</p>


  <p>I have completed CI/CD automation using <strong>Jenkins</strong>, <strong>GitHub</strong>, <strong>Docker</strong>, and <strong>Docker Hub</strong>. Every commit to GitHub now triggers a fully automated build, test, containerization, and image push pipeline. Currently deploying to <strong>Amazon EKS</strong> with Kubernetes orchestration.</p>


  <h2>Highlights</h2>
  <ul>
    <li>Jenkins running in Docker with plugins configured</li>
    <li>GitHub → Jenkins webhook connection established</li>
    <li>Freestyle job + automated Docker Build + Push</li>
    <li>Images pushed and verified in Docker Hub</li>
    <li>Local container deployment tested successfully</li>
    <li><strong>NEW:</strong> AWS EKS cluster created with Kubernetes 1.34</li>
    <li><strong>NEW:</strong> Kubernetes manifests for production-grade deployments</li>
  </ul>


  <h2>Project 1 — PHASES</h2>


  <h3>🟩 PHASE 1 – Project Setup & Cloud Foundation</h3>
  <p><strong>Objective:</strong> Set up foundational AWS cloud & local DevOps environment.</p>
  <ul>
    <li>Create AWS account, IAM roles, and policies</li>
    <li>Setup AWS services: S3, DynamoDB, SQS, SNS, CloudWatch</li>
    <li>Local setup: AWS CLI, Docker, kubectl, Minikube/EKS</li>
    <li>Verify AWS connectivity via CLI</li>
  </ul>
  <p><strong>Deliverable:</strong> ✅ AWS infrastructure & local DevOps environment ready</p>


  <h3>🟨 PHASE 2 – AWS Lambda Event Automation</h3>
  <p><strong>Objective:</strong> Automate S3 → Lambda → DynamoDB → SNS → SQS pipeline.</p>
  <ul>
    <li>Create Lambda function triggered by S3 uploads</li>
    <li>Log metadata into DynamoDB</li>
    <li>Send alerts via SNS</li>
    <li>Push messages into SQS</li>
    <li>Write logs to CloudWatch</li>
  </ul>
  <p><strong>Deliverable:</strong> ✅ Automated event workflow deployed</p>


  <h3>🟦 PHASE 3 – CI/CD Pipeline (Jenkins + GitHub + Docker)</h3>
  <p><strong>Objective:</strong> Build CI/CD pipeline for automated containerization.</p>
  <ul>
    <li>Setup Jenkins in Docker</li>
    <li>Integrate GitHub + Webhooks</li>
    <li>Integrate Docker build + Docker Hub push</li>
    <li>Create build → test → dockerize → push pipeline</li>
  </ul>
  <p><strong>Deliverable:</strong> ✅ Jenkins pipeline automatically builds & pushes container images on every GitHub commit</p>


  <h3>🟧 PHASE 4 – Kubernetes Deployment on AWS EKS</h3>
  <p><strong>Objective:</strong> Deploy Dockerized CloudOps application to a managed Kubernetes cluster (Amazon EKS) and automate rollout from Jenkins.</p>
  <ul>
    <li>Create and configure Amazon EKS cluster (control plane + node group) with:
      <ul>
        <li>Kubernetes version 1.34 with Standard support</li>
        <li>Custom configuration (not Auto Mode)</li>
        <li>IAM roles for cluster and nodes</li>
        <li>VPC networking across multiple Availability Zones</li>
        <li>Public and private API endpoint access</li>
        <li>Default add-ons: CoreDNS, kube-proxy, VPC CNI, node-monitoring-agent</li>
      </ul>
    </li>
    <li>Connect <code>kubectl</code> to EKS cluster using <code>aws eks update-kubeconfig</code></li>
    <li>Create Kubernetes manifests under <code>/k8s</code> folder:
      <ul>
        <li><code>namespace.yaml</code> - Isolate cloudops resources</li>
        <li><code>deployment.yaml</code> - Application deployment with 2 replicas, readiness/liveness probes</li>
        <li><code>service.yaml</code> - LoadBalancer service for external access</li>
        <li><code>configmap.yaml</code> - Environment configuration (APP_ENV, LOG_LEVEL)</li>
        <li><code>secret.yaml</code> - Sensitive data (DB passwords, API keys)</li>
        <li><code>storageclass-gp3.yaml</code> - EBS gp3 storage provisioner with WaitForFirstConsumer binding</li>
        <li><code>pvc.yaml</code> - Persistent volume claims (5Gi)</li>
        <li><code>statefulset-db.yaml</code> - PostgreSQL database with persistent storage</li>
        <li><code>daemonset-logs.yaml</code> - Fluent-bit logging agent on each node</li>
        <li><code>ingress.yaml</code> - (Optional) ALB ingress controller</li>
      </ul>
    </li>
    <li>Update Jenkins Freestyle jobs (Dev / Test / Prod) to:
      <ul>
        <li>Pull code from GitHub</li>
        <li>Build Docker image with build number tag</li>
        <li>Push to Docker Hub (both tagged and latest)</li>
        <li>Configure kubeconfig for EKS using AWS CLI</li>
        <li>Deploy to EKS using <code>kubectl apply -f k8s/</code></li>
        <li>Verify rollout status with <code>kubectl rollout status</code></li>
      </ul>
    </li>
    <li>Implement environment-safe rollout patterns:
      <ul>
        <li>Separate Dev/Test/Prod Jenkins jobs for isolated environments</li>
        <li>Option to extend to Blue-Green deployment (multiple deployments + services)</li>
        <li>Option to extend to Canary deployment (weighted traffic splitting)</li>
      </ul>
    </li>
    <li>Validate Kubernetes resources and application accessibility:
      <ul>
        <li>Verify all pods are Running</li>
        <li>Confirm Service has external LoadBalancer endpoint</li>
        <li>Test application via LoadBalancer DNS/IP</li>
        <li>Verify StatefulSet DB is healthy with PVC bound</li>
        <li>Confirm DaemonSet logging agent runs on all nodes</li>
      </ul>
    </li>
  </ul>
  <p><strong>Deliverable:</strong> ⏳ In Progress (70% complete)
    <ul>
      <li>✅ EKS cluster control plane created (Status: Active)</li>
      <li>✅ IAM roles configured (cluster + node roles)</li>
      <li>✅ VPC networking with 5 subnets across AZs</li>
      <li>✅ All Kubernetes manifests created</li>
      <li>⏳ Node group creation pending</li>
      <li>⏳ Jenkins EKS deployment jobs configuration pending</li>
      <li>⏳ End-to-end deployment testing pending</li>
    </ul>
  </p>


  <h3>🟥 PHASE 5 – Monitoring & Observability</h3>
  <p><strong>Objective:</strong> Complete monitoring, metrics & alerting stack.</p>
  <ul>
    <li>Prometheus setup inside K8s</li>
    <li>Node Exporter, cAdvisor, CloudWatch Exporter</li>
    <li>Grafana dashboards (EC2, Lambda, K8s, App Health)</li>
    <li>CloudWatch Alarms + SNS alerts</li>
  </ul>
  <p><strong>Deliverable:</strong> ⏳ Pending</p>


  <h3>🟪 PHASE 6 – Documentation, Dashboard & Demo</h3>
  <p><strong>Objective:</strong> Create final documentation & demo system.</p>
  <ul>
    <li>Architecture diagram</li>
    <li>Documentation for AWS, Jenkins, K8s, Monitoring</li>
    <li>Demo recording (optional)</li>
    <li>Final README + GitHub repository organization</li>
  </ul>
  <p><strong>Deliverable:</strong> ⏳ Pending</p>


  <h3>🧱 Summary Table</h3>
  <table border="1" cellpadding="5">
    <thead>
      <tr>
        <th>Phase</th>
        <th>Focus Area</th>
        <th>Tools</th>
        <th>Status</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Phase 1</strong></td>
        <td>Setup — AWS & Local Foundation</td>
        <td>AWS, CLI, Docker</td>
        <td>✅ Complete</td>
      </tr>
      <tr>
        <td><strong>Phase 2</strong></td>
        <td>Event Automation — Lambda, DynamoDB, SNS, SQS</td>
        <td>Lambda, boto3, S3, CloudWatch</td>
        <td>✅ Complete</td>
      </tr>
      <tr>
        <td><strong>Phase 3</strong></td>
        <td>CI/CD — Jenkins Pipeline, Docker Builds</td>
        <td>Jenkins, GitHub, Docker, Docker Hub</td>
        <td>✅ Complete</td>
      </tr>
      <tr>
        <td><strong>Phase 4</strong></td>
        <td>Orchestration — Kubernetes Deployment on AWS EKS</td>
        <td>EKS, kubectl, Kubernetes manifests, gp3 EBS</td>
        <td>⏳ In Progress (70%)</td>
      </tr>
      <tr>
        <td><strong>Phase 5</strong></td>
        <td>Monitoring — Metrics & Alerts</td>
        <td>Prometheus, Grafana, CloudWatch</td>
        <td>⏳ Pending</td>
      </tr>
      <tr>
        <td><strong>Phase 6</strong></td>
        <td>Docs & Demo — Final Documentation</td>
        <td>Markdown, Diagrams, Screenshots</td>
        <td>⏳ Pending</td>
      </tr>
    </tbody>
  </table>


  <h2>Project Files</h2>
  <ul>
    <li><a href="./README.md">README.md</a> — Main project description</li>
    <li><a href="./Phase-1.md">Phase-1.md</a> — AWS Foundation & Setup</li>
    <li><a href="./Phase-2.md">Phase-2.md</a> — Lambda Event Automation</li>
    <li><a href="./Phase-3.md">Phase-3.md</a> — CI/CD Pipeline (Jenkins + Docker)</li>
    <li><a href="./Phase-4.md">Phase-4.md</a> — Kubernetes Deployment on AWS EKS (In Progress)</li>
    <li><a href="./screenshots/phase4/">screenshots/phase4/</a> — EKS cluster creation screenshots</li>
  </ul>


  <h2>Next Steps</h2>
  <p>Currently working on:</p>
  <ul>
    <li><strong>Phase 4:</strong> Complete node group creation with gp3 volumes, configure Jenkins EKS deployment jobs, test end-to-end Kubernetes deployment</li>
    <li><strong>Phase 5:</strong> Setup Prometheus + Grafana monitoring stack inside EKS cluster with CloudWatch integration</li>
    <li><strong>Phase 6:</strong> Create architecture diagrams, finalize documentation with screenshots, prepare demo recording</li>
  </ul>


  <h2>Technical Stack</h2>
  <ul>
    <li><strong>Cloud:</strong> AWS (EKS, EC2, S3, Lambda, DynamoDB, SNS, SQS, CloudWatch, IAM, EBS gp3)</li>
    <li><strong>Containerization:</strong> Docker, Docker Hub</li>
    <li><strong>Orchestration:</strong> Kubernetes 1.34 (AWS EKS), kubectl</li>
    <li><strong>CI/CD:</strong> Jenkins (Dockerized), GitHub Webhooks</li>
    <li><strong>Storage:</strong> EBS gp3 volumes, Persistent Volume Claims</li>
    <li><strong>Networking:</strong> VPC, LoadBalancer, Security Groups, Multi-AZ deployment</li>
    <li><strong>Monitoring:</strong> Prometheus, Grafana, CloudWatch (Planned)</li>
    <li><strong>Languages:</strong> Python, Bash, YAML</li>
  </ul>


  <p>— <strong>Devil (CloudOps Automation)</strong></p>


</body>
</html>
