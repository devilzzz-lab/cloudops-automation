<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>

  <h1>CloudOps Automation — Project</h1>

  <p><strong>Status:</strong> <em>Phase 4 (Kubernetes Deployment using KIND)</em> <strong>completed</strong>. Phases 1–4 completed. Remaining Phases 5–6 pending.</p>

  <p>
    I have completed CI/CD automation using <strong>Jenkins</strong>, <strong>GitHub</strong>, <strong>Docker</strong>, and <strong>Docker Hub</strong>.
    Every commit to GitHub now triggers a fully automated build, test, containerization, image push, and Kubernetes deployment pipeline.
    Successfully deployed to a <strong>Kubernetes cluster created using KIND (Kubernetes IN Docker)</strong> with complete orchestration and automated rollout.
  </p>

  <hr>

  <h2>Highlights</h2>
  <ul>
    <li>Jenkins running in Docker with Docker CLI and kubectl installed</li>
    <li>GitHub → Jenkins webhook connection established via ngrok</li>
    <li>Freestyle jobs for CI (build) and CD (deploy) automation</li>
    <li>Automated Docker image build and push to Docker Hub with versioned tags</li>
    <li>Images verified successfully in Docker Hub</li>
    <li><strong>NEW:</strong> Kubernetes cluster created using <strong>KIND (Kubernetes IN Docker)</strong></li>
    <li><strong>NEW:</strong> Jenkins container connected to KIND Docker network with full cluster access</li>
    <li><strong>NEW:</strong> Production-grade Kubernetes manifests (Deployment, Service, StatefulSet, DaemonSet, ConfigMap, Secret, PVC)</li>
    <li><strong>NEW:</strong> Jenkins deploys applications automatically to KIND Kubernetes cluster using kubectl</li>
    <li><strong>NEW:</strong> Parameterized deployments with specific image tag selection</li>
    <li><strong>NEW:</strong> Zero-downtime rolling updates with automated rollout verification</li>
  </ul>

  <hr>

  <h2>Project Phases</h2>

  <h3>🟩 PHASE 1 – Project Setup &amp; Cloud Foundation</h3>
  <p><strong>Objective:</strong> Set up foundational AWS cloud &amp; local DevOps environment.</p>
  <ul>
    <li>Create AWS account, IAM roles, and policies</li>
    <li>Setup AWS services: S3, DynamoDB, SQS, SNS, CloudWatch</li>
    <li>Local setup: AWS CLI, Docker, kubectl</li>
    <li>Verify AWS connectivity via CLI</li>
  </ul>
  <p><strong>Deliverable:</strong> ✅ AWS infrastructure &amp; local DevOps environment ready</p>

  <h3>🟨 PHASE 2 – AWS Lambda Event Automation</h3>
  <p><strong>Objective:</strong> Automate S3 → Lambda → DynamoDB → SNS → SQS pipeline.</p>
  <ul>
    <li>Create Lambda function triggered by S3 uploads</li>
    <li>Store metadata in DynamoDB</li>
    <li>Send notifications via SNS</li>
    <li>Push messages to SQS</li>
    <li>Centralized logging in CloudWatch</li>
  </ul>
  <p><strong>Deliverable:</strong> ✅ Automated event-driven workflow deployed</p>

  <h3>🟦 PHASE 3 – Complete Development Environment Setup</h3>
  <p><strong>Objective:</strong> Build complete local CI/CD development environment with Docker, Kubernetes, and Jenkins.</p>
  <ul>
    <li>Install Docker Desktop on macOS</li>
    <li>Install and configure KIND (Kubernetes IN Docker)</li>
    <li>Create local Kubernetes cluster using KIND</li>
    <li>Setup Jenkins container with proper volume mounts and network configuration</li>
    <li>Install Docker CLI inside Jenkins container for image building</li>
    <li>Install kubectl inside Jenkins container for Kubernetes management</li>
    <li>Configure Jenkins access to KIND cluster via internal kubeconfig</li>
    <li>Connect Jenkins to KIND Docker network for cluster communication</li>
    <li>Configure GitHub and Docker Hub credentials in Jenkins</li>
    <li>Install required Jenkins plugins (Git, GitHub, Credentials, Pipeline)</li>
  </ul>
  <p><strong>Deliverable:</strong> ✅ Fully configured development environment with Docker + KIND + Jenkins integration</p>

  <h3>🟧 PHASE 4 – CI/CD Pipeline &amp; Kubernetes Deployment Automation</h3>
  <p><strong>Objective:</strong> Build end-to-end CI/CD pipeline with automated Docker builds and Kubernetes deployments.</p>
  <ul>
    <li>Create GitHub repository with application code and Kubernetes manifests</li>
    <li>Create CI build job (<code>cloudops-ci-build</code>) in Jenkins:
      <ul>
        <li>Checkout code from GitHub</li>
        <li>Build Docker image with versioned tags (build-${BUILD_NUMBER})</li>
        <li>Push images to Docker Hub (versioned + latest)</li>
        <li>Triggered automatically via GitHub webhook</li>
      </ul>
    </li>
    <li>Create CD deployment job (<code>cloudops-prod-deploy</code>) in Jenkins:
      <ul>
        <li>Parameterized build with IMAGE_TAG selection</li>
        <li>Apply Kubernetes manifests to KIND cluster</li>
        <li>Update deployment with specific image version</li>
        <li>Wait for rollout completion with timeout</li>
        <li>Verify pod status and service endpoints</li>
        <li>Triggered automatically after successful CI build</li>
      </ul>
    </li>
    <li>Setup ngrok for GitHub webhook access to local Jenkins</li>
    <li>Configure GitHub webhook for automatic pipeline triggering</li>
    <li>Implement production-grade Kubernetes manifests:
      <ul>
        <li>Namespace isolation</li>
        <li>Deployment with multiple replicas</li>
        <li>NodePort Service for external access</li>
        <li>StatefulSet for database with persistent storage</li>
        <li>DaemonSet for log collection</li>
        <li>ConfigMap for configuration management</li>
        <li>Secret for sensitive data</li>
        <li>PersistentVolumeClaim for storage</li>
      </ul>
    </li>
    <li>Test complete workflow: Git Push → Webhook → CI Build → CD Deploy → Live App</li>
    <li>Verify zero-downtime rolling updates</li>
    <li>Debug and troubleshoot using kubectl commands via Jenkins container</li>
  </ul>
  <p><strong>Deliverable:</strong> ✅ Production-ready CI/CD pipeline with automated Kubernetes deployment to KIND cluster</p>

  <h3>🟥 PHASE 5 – Monitoring &amp; Observability</h3>
  <p><strong>Objective:</strong> Implement monitoring, metrics, and alerting.</p>
  <ul>
    <li>Deploy Prometheus inside Kubernetes</li>
    <li>Configure exporters (Node Exporter, cAdvisor)</li>
    <li>Setup Grafana dashboards for Kubernetes and application metrics</li>
    <li>Integrate CloudWatch alarms and SNS alerts (future cloud migration)</li>
  </ul>
  <p><strong>Deliverable:</strong> ⏳ Pending</p>

  <h3>🟪 PHASE 6 – Documentation, Dashboard &amp; Demo</h3>
  <p><strong>Objective:</strong> Finalize documentation and demo materials.</p>
  <ul>
    <li>Architecture diagram (CI/CD + Kubernetes)</li>
    <li>Detailed documentation with screenshots</li>
    <li>Demo walkthrough recording</li>
    <li>Final README and repository cleanup</li>
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
        <td>AWS &amp; Local Foundation</td>
        <td>AWS, CLI, Docker</td>
        <td>✅ Complete</td>
      </tr>
      <tr>
        <td><strong>Phase 2</strong></td>
        <td>Event Automation</td>
        <td>Lambda, DynamoDB, SNS, SQS</td>
        <td>✅ Complete</td>
      </tr>
      <tr>
        <td><strong>Phase 3</strong></td>
        <td>Development Environment Setup</td>
        <td>Docker Desktop, KIND, Jenkins, kubectl</td>
        <td>✅ Complete</td>
      </tr>
      <tr>
        <td><strong>Phase 4</strong></td>
        <td>CI/CD Pipeline &amp; Kubernetes Deployment</td>
        <td>Jenkins, GitHub, Docker Hub, Kubernetes, ngrok</td>
        <td>✅ Complete</td>
      </tr>
      <tr>
        <td><strong>Phase 5</strong></td>
        <td>Monitoring &amp; Observability</td>
        <td>Prometheus, Grafana, CloudWatch</td>
        <td>⏳ Pending</td>
      </tr>
      <tr>
        <td><strong>Phase 6</strong></td>
        <td>Documentation &amp; Demo</td>
        <td>Markdown, Diagrams, Screenshots</td>
        <td>⏳ Pending</td>
      </tr>
    </tbody>
  </table>

  <hr>

  <h2>Technical Stack</h2>
  <ul>
    <li><strong>Cloud:</strong> AWS (S3, Lambda, DynamoDB, SNS, SQS, CloudWatch, IAM)</li>
    <li><strong>Containerization:</strong> Docker, Docker Hub</li>
    <li><strong>Orchestration:</strong> Kubernetes (KIND - Kubernetes IN Docker)</li>
    <li><strong>CI/CD:</strong> Jenkins (Dockerized), GitHub Webhooks, ngrok</li>
    <li><strong>Storage:</strong> PersistentVolumeClaims (PVCs), StatefulSets</li>
    <li><strong>Networking:</strong> NodePort Services, Docker Networks</li>
    <li><strong>Configuration:</strong> ConfigMaps, Secrets</li>
    <li><strong>Monitoring:</strong> Prometheus, Grafana (Planned)</li>
    <li><strong>Languages:</strong> Python, Bash, YAML</li>
    <li><strong>Tools:</strong> kubectl, Docker CLI, Git</li>
  </ul>

  <hr>

  <h2>CI/CD Pipeline Flow</h2>
  <pre>
Developer → Git Push → GitHub
                        ↓
                   Webhook (ngrok)
                        ↓
                     Jenkins
                        ↓
            ┌───────────┴───────────┐
            ↓                       ↓
    CI Job (Build)          CD Job (Deploy)
    - Checkout code         - Apply K8s manifests
    - Build Docker image    - Update deployment
    - Tag: build-X          - Rolling update
    - Push to Docker Hub    - Verify rollout
            ↓                       ↓
        Docker Hub          KIND Kubernetes Cluster
                                    ↓
                            Running Application
                            (http://localhost:30080)
  </pre>

  <hr>

  <p><strong>— CloudOps Automation Project</strong></p>

</body>
</html>
