<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>

  <h1>CloudOps Automation — Project</h1>

  <p><strong>Status:</strong> <em>Phase 4 (Kubernetes Deployment using KIND)</em> <strong>in progress</strong>. Phases 1–3 completed. Remaining Phases 5–6 pending.</p>

  <p>
    I have completed CI/CD automation using <strong>Jenkins</strong>, <strong>GitHub</strong>, <strong>Docker</strong>, and <strong>Docker Hub</strong>.
    Every commit to GitHub now triggers a fully automated build, test, containerization, and image push pipeline.
    Currently deploying to a <strong>Kubernetes cluster created using KIND (Kubernetes IN Docker)</strong> with Kubernetes orchestration.
  </p>

  <hr>

  <h2>Highlights</h2>
  <ul>
    <li>Jenkins running in Docker with required plugins configured</li>
    <li>GitHub → Jenkins webhook connection established</li>
    <li>Freestyle jobs for CI and CD automation</li>
    <li>Automated Docker image build and push to Docker Hub</li>
    <li>Images verified successfully in Docker Hub</li>
    <li>Local container deployment validated</li>
    <li><strong>NEW:</strong> Kubernetes cluster created using <strong>KIND (Kubernetes IN Docker)</strong> with Kubernetes v1.34</li>
    <li><strong>NEW:</strong> Jenkins container connected to KIND Docker network for Kubernetes access</li>
    <li><strong>NEW:</strong> Production-grade Kubernetes manifests (Deployment, Service, StatefulSet, DaemonSet, ConfigMap, Secret, PVC)</li>
    <li><strong>NEW:</strong> Jenkins deploys applications directly to the KIND Kubernetes cluster using kubectl</li>
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

  <h3>🟦 PHASE 3 – CI/CD Pipeline (Jenkins + GitHub + Docker)</h3>
  <p><strong>Objective:</strong> Build CI/CD pipeline for automated containerization.</p>
  <ul>
    <li>Setup Jenkins inside Docker container</li>
    <li>Integrate GitHub with Jenkins using webhooks</li>
    <li>Automate Docker image build and push to Docker Hub</li>
    <li>End-to-end CI pipeline triggered on every GitHub commit</li>
  </ul>
  <p><strong>Deliverable:</strong> ✅ Fully automated CI pipeline for container build and push</p>

  <h3>🟧 PHASE 4 – Kubernetes Deployment using KIND</h3>
  <p><strong>Objective:</strong> Deploy the Dockerized CloudOps application to a local Kubernetes cluster created using <strong>KIND (Kubernetes IN Docker)</strong>, with automated rollout from Jenkins.</p>
  <ul>
    <li>Create Kubernetes cluster using KIND</li>
    <li>Configure Jenkins container with kubectl and Docker CLI</li>
    <li>Connect Jenkins container to KIND Docker network</li>
    <li>Generate and use KIND internal kubeconfig for Jenkins access</li>
    <li>Create Kubernetes manifests inside <code>/k8s</code> directory</li>
    <li>Automate deployments from Jenkins (CI → CD → Kubernetes)</li>
    <li>Perform rolling updates and rollout verification using kubectl</li>
  </ul>
  <p><strong>Deliverable:</strong> ⏳ Automated deployment of the containerized CloudOps application to KIND Kubernetes via Jenkins CI/CD pipeline.</p>

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
        <td>CI/CD Pipeline</td>
        <td>Jenkins, GitHub, Docker, Docker Hub</td>
        <td>✅ Complete</td>
      </tr>
      <tr>
        <td><strong>Phase 4</strong></td>
        <td>Kubernetes Deployment (KIND)</td>
        <td>KIND, kubectl, Kubernetes manifests</td>
        <td>⏳ In Progress (80%)</td>
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
    <li><strong>Orchestration:</strong> Kubernetes 1.34 using KIND</li>
    <li><strong>CI/CD:</strong> Jenkins (Dockerized), GitHub Webhooks</li>
    <li><strong>Storage:</strong> PersistentVolumeClaims (PVCs)</li>
    <li><strong>Networking:</strong> NodePort / Port-forward (local KIND cluster)</li>
    <li><strong>Monitoring:</strong> Prometheus, Grafana (Planned)</li>
    <li><strong>Languages:</strong> Python, Bash, YAML</li>
  </ul>

  <hr>

  <p><strong>— CloudOps Automation Project</strong></p>

</body>
</html>
