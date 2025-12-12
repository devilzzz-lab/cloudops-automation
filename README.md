<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>

  <h1>CloudOps Automation — Project</h1>

  <p><strong>Status:</strong> <em>Phase 4 (Kubernetes Deployment on AWS EKS)</em> <strong>in progress</strong>. Phases 1-3 completed. Remaining Phases 5-6 pending.</p>

  <p>I have completed CI/CD automation using <strong>Jenkins</strong>, <strong>GitHub</strong>, <strong>Docker</strong>, and <strong>Docker Hub</strong>. Every commit to GitHub now triggers a fully automated build, test, containerization, and image push pipeline. Currently deploying to <strong>Amazon EKS</strong> with Kubernetes orchestration.</p>

  <hr>

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

  <hr>

  <h2>Project Phases</h2>

  <h3>🟩 PHASE 1 – Project Setup &amp; Cloud Foundation</h3>
  <p><strong>Objective:</strong> Set up foundational AWS cloud &amp; local DevOps environment.</p>
  <ul>
    <li>Create AWS account, IAM roles, and policies</li>
    <li>Setup AWS services: S3, DynamoDB, SQS, SNS, CloudWatch</li>
    <li>Local setup: AWS CLI, Docker, kubectl, Minikube/EKS</li>
    <li>Verify AWS connectivity via CLI</li>
  </ul>
  <p><strong>Deliverable:</strong> ✅ AWS infrastructure &amp; local DevOps environment ready</p>

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
  <p><strong>Deliverable:</strong> ✅ Jenkins pipeline automatically builds &amp; pushes container images on every GitHub commit</p>

  <h3>🟧 PHASE 4 – Kubernetes Deployment using Docker Desktop</h3>
  <p><strong>Objective:</strong> Deploy the Dockerized CloudOps application to a local Kubernetes cluster (Docker Desktop Kubernetes) with automated rollout from Jenkins.</p>
  <ul>
    <li>Enable Kubernetes inside Docker Desktop and verify using <code>kubectl get nodes</code>.</li>
    <li>Create Kubernetes manifests in <code>/k8s</code>: <code>namespace.yaml</code>, <code>deployment.yaml</code>, <code>service.yaml</code>, <code>configmap.yaml</code>, <code>secret.yaml</code>, <code>pvc.yaml</code> (optional), and <code>ingress.yaml</code> (optional).</li>
    <li>Update Jenkins jobs (Dev / Test / Prod) to:
      <ul>
        <li>Build Docker images</li>
        <li>Push images to Docker Hub</li>
        <li>Deploy to the local Kubernetes cluster using <code>kubectl apply -f k8s/</code></li>
      </ul>
    </li>
  </ul>
  <p><strong>Deliverable:</strong> ⏳ Automated deployment of the containerized CloudOps application to Docker Desktop Kubernetes via Jenkins CI/CD pipeline.</p>

  <h3>🟥 PHASE 5 – Monitoring &amp; Observability</h3>
  <p><strong>Objective:</strong> Complete monitoring, metrics &amp; alerting stack.</p>
  <ul>
    <li>Prometheus setup inside K8s</li>
    <li>Node Exporter, cAdvisor, CloudWatch Exporter</li>
    <li>Grafana dashboards (EC2, Lambda, K8s, App Health)</li>
    <li>CloudWatch Alarms + SNS alerts</li>
  </ul>
  <p><strong>Deliverable:</strong> ⏳ Pending</p>

  <h3>🟪 PHASE 6 – Documentation, Dashboard &amp; Demo</h3>
  <p><strong>Objective:</strong> Create final documentation &amp; demo system.</p>
  <ul>
    <li>Architecture diagram</li>
    <li>Documentation for AWS, Jenkins, K8s, Monitoring</li>
    <li>Demo recording (optional)</li>
    <li>Final README + GitHub repository organization</li>
  </ul>
  <p><strong>Deliverable:</strong> ⏳ Pending</p>

  <hr>

  <h2>Summary Table</h2>
  <table border="1" cellpadding="8" cellspacing="0">
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
        <td>Setup — AWS &amp; Local Foundation</td>
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
        <td>Monitoring — Metrics &amp; Alerts</td>
        <td>Prometheus, Grafana, CloudWatch</td>
        <td>⏳ Pending</td>
      </tr>
      <tr>
        <td><strong>Phase 6</strong></td>
        <td>Docs &amp; Demo — Final Documentation</td>
        <td>Markdown, Diagrams, Screenshots</td>
        <td>⏳ Pending</td>
      </tr>
    </tbody>
  </table>

  <hr>

  <h2>Project Files</h2>
  <ul>
    <li><a href="./README.md">README.md</a> — Main project description</li>
    <li><a href="./Phase-1.md">Phase-1.md</a> — AWS Foundation &amp; Setup</li>
    <li><a href="./Phase-2.md">Phase-2.md</a> — Lambda Event Automation</li>
    <li><a href="./Phase-3.md">Phase-3.md</a> — CI/CD Pipeline (Jenkins + Docker)</li>
    <li><a href="./Phase-4.md">Phase-4.md</a> — Kubernetes Deployment on AWS EKS (In Progress)</li>
    <li><a href="./screenshots/phase4/">screenshots/phase4/</a> — EKS cluster creation screenshots</li>
  </ul>

  <hr>

  <h2>Next Steps</h2>
  <p>Currently working on:</p>
  <ul>
    <li><strong>Phase 4:</strong> Complete node group creation with gp3 volumes, configure Jenkins EKS deployment jobs, test end-to-end Kubernetes deployment</li>
    <li><strong>Phase 5:</strong> Setup Prometheus + Grafana monitoring stack inside EKS cluster with CloudWatch integration</li>
    <li><strong>Phase 6:</strong> Create architecture diagrams, finalize documentation with screenshots, prepare demo recording</li>
  </ul>

  <hr>

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

  <hr>

  <p><strong>— CloudOps Automation Project</strong></p>

</body>
</html>
