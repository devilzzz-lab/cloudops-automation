<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>

  <h1>CloudOps Automation — Project</h1>

  <p><strong>Status:</strong> <em>Phase 5 (Monitoring & Observability)</em> <strong>in progress</strong>. Phases 1–4 completed. Phase 5 started. Phase 6 pending.</p>

  <p>
    I have completed CI/CD automation using <strong>Jenkins</strong>, <strong>GitHub</strong>, <strong>Docker</strong>, and <strong>Docker Hub</strong>.
    Every commit to GitHub now triggers a fully automated build, test, containerization, image push, and Kubernetes deployment pipeline.
    Successfully deployed to a <strong>Kubernetes cluster created using KIND (Kubernetes IN Docker)</strong> with complete orchestration and automated rollout.
    Currently implementing <strong>monitoring and observability</strong> using Prometheus and Grafana for comprehensive cluster and application metrics.
  </p>

  <hr>

  <h2>Highlights</h2>
  <ul>
    <li>Jenkins running in Docker with Docker CLI and kubectl installed</li>
    <li>GitHub → Jenkins webhook connection established via ngrok</li>
    <li>Freestyle jobs for CI (build) and CD (deploy) automation</li>
    <li>Automated Docker image build and push to Docker Hub with versioned tags</li>
    <li>Images verified successfully in Docker Hub</li>
    <li>Kubernetes cluster created using <strong>KIND (Kubernetes IN Docker)</strong></li>
    <li>Jenkins container connected to KIND Docker network with full cluster access</li>
    <li>Production-grade Kubernetes manifests (Deployment, Service, StatefulSet, DaemonSet, ConfigMap, Secret, PVC)</li>
    <li>Jenkins deploys applications automatically to KIND Kubernetes cluster using kubectl</li>
    <li>Parameterized deployments with specific image tag selection</li>
    <li>Zero-downtime rolling updates with automated rollout verification</li>
    <li><strong>NEW:</strong> Prometheus deployed for metrics collection and monitoring</li>
    <li><strong>NEW:</strong> Grafana deployed with Prometheus integration for visualization</li>
    <li><strong>NEW:</strong> Real-time cluster health and application performance monitoring</li>
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
  <p><strong>Objective:</strong> Build local CI/CD environment with Docker, Kubernetes and Jenkins.</p>
  <ul>
    <li>Install Docker Desktop and KIND (Kubernetes IN Docker)</li>
    <li>Create local Kubernetes cluster and verify access</li>
    <li>Run Jenkins in Docker with Docker CLI and kubectl installed</li>
    <li>Connect Jenkins container to KIND network and kubeconfig</li>
    <li>Configure GitHub and Docker Hub credentials plus required plugins</li>
  </ul>
  <p><strong>Deliverable:</strong> ✅ Local Docker + KIND + Jenkins environment ready for CI/CD</p>

  <h3>🟧 PHASE 4 – CI/CD Pipeline &amp; Kubernetes Deployment Automation</h3>
  <p><strong>Objective:</strong> Implement end-to-end CI/CD from GitHub to Kubernetes using Jenkins.</p>
  <ul>
    <li>Create GitHub repo with app code and Kubernetes manifests</li>
    <li>CI job: build Docker image on each commit and push to Docker Hub (versioned tags)</li>
    <li>CD job: parameterized deployment (IMAGE_TAG) to KIND cluster using kubectl</li>
    <li>Integrate GitHub webhooks via ngrok for automatic pipeline triggers</li>
    <li>Validate rolling updates, pod status and service access on KIND</li>
  </ul>
  <p><strong>Deliverable:</strong> ✅ Production-ready CI/CD pipeline with automated Kubernetes deployment to KIND cluster</p>

  <h3>🟥 PHASE 5 – Monitoring &amp; Observability</h3>
  <p><strong>Objective:</strong> Implement real-time monitoring, metrics, dashboards, and alerting for Kubernetes workloads and applications.</p>

  <ul>
    <li>Deploy Prometheus inside KIND Kubernetes cluster for metrics collection</li>
    <li>Configure exporters: Node Exporter, cAdvisor, kube-state-metrics</li>
    <li>Expose application metrics endpoint and scrape via Prometheus</li>
    <li>Setup Grafana with Prometheus as data source</li>
    <li>Create dashboards for cluster health, pod metrics, and application performance</li>
    <li>Configure Prometheus alerts for pod failures and resource saturation</li>
    <li>Implement AlertManager for notification routing</li>
    <li>Integrate monitoring with CI/CD pipeline for deployment tracking</li>
  </ul>

  <p><strong>Deliverable:</strong> ⏳ In Progress - Prometheus and Grafana deployed, dashboards and alerting configuration ongoing</p>

  <h3>🟪 PHASE 6 – Documentation, Dashboard &amp; Demo</h3>
  <p><strong>Objective:</strong> Finalize documentation and demo materials.</p>
  <ul>
    <li>Architecture diagram (CI/CD + Kubernetes + Monitoring)</li>
    <li>Detailed documentation with screenshots</li>
    <li>Demo walkthrough recording</li>
    <li>Final README and repository cleanup</li>
    <li>Performance metrics and monitoring dashboard showcase</li>
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
        <td>Prometheus, Grafana, AlertManager, Exporters</td>
        <td>⏳ In Progress (60%)</td>
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
    <li><strong>Networking:</strong> NodePort Services, Docker Networks, Port-Forward</li>
    <li><strong>Configuration:</strong> ConfigMaps, Secrets</li>
    <li><strong>Monitoring:</strong> Prometheus, Grafana, AlertManager, Node Exporter, kube-state-metrics</li>
    <li><strong>Languages:</strong> Python, Bash, YAML, PromQL</li>
    <li><strong>Tools:</strong> kubectl, Docker CLI, Git, Helm (for monitoring stack)</li>
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
                                    ↓
                         Prometheus (Metrics Collection)
                                    ↓
                         Grafana (Visualization)
  </pre>

  <hr>

  <h2>Monitoring Architecture</h2>
  <pre>
KIND Kubernetes Cluster
    ↓
┌───────────────────────────────────┐
│  Application Pods                 │
│  - Expose /metrics endpoint       │
└───────────────┬───────────────────┘
                ↓
┌───────────────────────────────────┐
│  Prometheus Server                │
│  - Scrapes metrics every 15s      │
│  - Stores time-series data        │
│  - Evaluates alert rules          │
└───────────────┬───────────────────┘
                ↓
        ┌───────┴────────┐
        ↓                ↓
┌───────────────┐  ┌─────────────┐
│ Grafana       │  │ AlertManager│
│ - Dashboards  │  │ - Alerts    │
│ - Queries     │  │ - Routing   │
└───────────────┘  └─────────────┘
  </pre>

  <hr>

  <p><strong>— CloudOps Automation Project</strong></p>

</body>
</html>
