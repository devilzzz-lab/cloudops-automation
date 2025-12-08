<html lang="en">
<head>
  <meta charset="utf-8" />
</head>
<body>

  <h1>CloudOps Automation — Project</h1>

  <p><strong>Status:</strong> <em>Phase 3 (CI/CD Pipeline)</em> <strong>completed</strong>. Remaining Phases 4, 5, 6 are in progress.</p>

  <p>I have completed CI/CD automation using <strong>Jenkins</strong>, <strong>GitHub</strong>, <strong>Docker</strong>, and <strong>Docker Hub</strong>. Every commit to GitHub now triggers a fully automated build, test, containerization, and image push pipeline.</p>

  <h2>Highlights</h2>
  <ul>
    <li>Jenkins running in Docker with plugins configured</li>
    <li>GitHub → Jenkins webhook connection established</li>
    <li>Freestyle job + automated Docker Build + Push</li>
    <li>Images pushed and verified in Docker Hub</li>
    <li>Local container deployment tested successfully</li>
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
  <p><strong>Deliverable:</strong> ✔ AWS infrastructure & local DevOps environment ready</p>

  <h3>🟨 PHASE 2 – AWS Lambda Event Automation</h3>
  <p><strong>Objective:</strong> Automate S3 → Lambda → DynamoDB → SNS → SQS pipeline.</p>
  <ul>
    <li>Create Lambda function triggered by S3 uploads</li>
    <li>Log metadata into DynamoDB</li>
    <li>Send alerts via SNS</li>
    <li>Push messages into SQS</li>
    <li>Write logs to CloudWatch</li>
  </ul>
  <p><strong>Deliverable:</strong> ✔ Automated event workflow deployed</p>

  <h3>🟦 PHASE 3 – CI/CD Pipeline (Jenkins + GitHub + Docker)</h3>
  <p><strong>Objective:</strong> Build CI/CD pipeline for automated containerization.</p>
  <ul>
    <li>Setup Jenkins in Docker</li>
    <li>Integrate GitHub + Webhooks</li>
    <li>Integrate Docker build + Docker Hub push</li>
    <li>Create build → test → dockerize → push pipeline</li>
  </ul>
  <p><strong>Deliverable:</strong> ✔ Jenkins pipeline automatically builds & pushes image</p>

  <h3>🟧 PHASE 4 – Container Deployment & Orchestration (Kubernetes)</h3>
  <p><strong>Objective:</strong> Deploy containers into Kubernetes.</p>
  <ul>
    <li>Setup Kubernetes cluster (Minikube/EKS)</li>
    <li>Create deployment.yaml, service.yaml, configmap.yaml</li>
    <li>Auto-deploy from Jenkins pipeline</li>
    <li>Blue-Green / Canary rollout options</li>
  </ul>
  <p><strong>Deliverable:</strong> Pending</p>

  <h3>🟥 PHASE 5 – Monitoring & Observability</h3>
  <p><strong>Objective:</strong> Complete monitoring, metrics & alerting stack.</p>
  <ul>
    <li>Prometheus setup inside K8s</li>
    <li>Node Exporter, cAdvisor, CloudWatch Exporter</li>
    <li>Grafana dashboards (EC2, Lambda, K8s, App Health)</li>
    <li>CloudWatch Alarms + SNS alerts</li>
  </ul>
  <p><strong>Deliverable:</strong> Pending</p>

  <h3>🟪 PHASE 6 – Documentation, Dashboard & Demo</h3>
  <p><strong>Objective:</strong> Create final documentation & demo system.</p>
  <ul>
    <li>Architecture diagram</li>
    <li>Documentation for AWS, Jenkins, K8s, Monitoring</li>
    <li>Demo recording (optional)</li>
    <li>Final README + GitHub repository organization</li>
  </ul>
  <p><strong>Deliverable:</strong> Pending</p>

  <h3>🧱 Summary Table</h3>
  <p>
    <strong>Phase 1:</strong> Setup — AWS & Local Foundation — Tools: AWS, CLI, Docker<br/>
    <strong>Phase 2:</strong> Event Automation — Lambda, DynamoDB, SNS, SQS — Tools: Lambda, boto3<br/>
    <strong>Phase 3:</strong> CI/CD — Jenkins Pipeline, Docker Builds — Tools: Jenkins, GitHub, Docker<br/>
    <strong>Phase 4:</strong> Orchestration — Kubernetes Deployment — Tools: EKS/Minikube<br/>
    <strong>Phase 5:</strong> Monitoring — Metrics & Alerts — Tools: Prometheus, Grafana, CloudWatch<br/>
    <strong>Phase 6:</strong> Docs & Demo — Final Documentation — Tools: Markdown, Diagrams
  </p>

  <h2>Project Files</h2>
  <ul>
    <li><a href="./README.md">README.md</a> — Main project description</li>
    <li><a href="./Phase-1.md">Phase-1.md</a></li>
    <li><a href="./Phase-2.md">Phase-2.md</a></li>
    <li><a href="./Phase-3.md">Phase-3.md</a></li>
    <li><a href="./Phase-4.md">Phase-4.md</a></li>
  </ul>

  <h2>Next Steps</h2>
  <p>Currently working on: Phase 4 → Phase 5 → Phase 6 (Kubernetes, Monitoring & Documentation). More updates coming as the system evolves.</p>

  <p>— <strong>Devil (CloudOps Automation)</strong></p>

</body>
</html>
