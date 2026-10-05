# FastAPI Enterprise Serverless Architecture on AWS ECS Fargate

An automated, highly available, and production-ready serverless hosting architecture for a Python FastAPI application. Code updates pushed to the repository automatically go through linting and test assertions before deploying via an automated zero-downtime rolling update configuration on AWS.

## 🚀 Architectural Architecture Overview

```text
               [ Public Internet Ingress ]
                            │
                            ▼ (Port 80 - HTTP)
         ┌─────────────────────────────────────┐
         │  Application Load Balancer (ALB)   │  ◄── Public Subnets
         └─────────────────────────────────────┘
                            │
                            ▼ (Port Forwarding / Translation: 80 ──> 8000)
         ┌─────────────────────────────────────┐
         │     Target Group (fastapi-tg)       │  ◄── Routing Matrix
         └─────────────────────────────────────┘
                            │
                            ▼ (Target Verification)
   ┌─────────────────────────────────────────────────┐
   │        AWS ECS Fargate Cluster (api-cluster)    │  ◄── Compute Layer
   │                                                 │
   │  [ Fargate Task Node 1 ]   [ Fargate Task Node 2]│
   │      (us-east-1a zone)         (us-east-1b zone)│
   │  Container Name: main      Container Name: main │
   └─────────────────────────────────────────────────┘
```

### Key Components Built
1. **Isolated Networking Layer (VPC):** Configured with segmented Public/Private Subnets across multiple Availability Zones (`us-east-1a` and `us-east-1b`) to ensure continuous resilience.
2. **Compute Isolation Framework:** Application workloads are hosted on serverless **AWS Fargate** profiles, secured using structured Security Group routing rules that ensure the containers only accept traffic originating from the Load Balancer proxy node.
3. **Traffic Distribution Gateway:** An **Application Load Balancer (ALB)** intercepts public web traffic on port `80` and translates the data streams directly down to internal port `8000` mapped onto active target IPs.
4. **Automated Delivery Pipeline:** Leverages official GitHub Actions runner states to authenticate with Docker Hub and seamlessly update AWS configurations via **OpenID Connect (OIDC)** temporary session handshakes instead of storing static root keys.

---

## 🛠️ Automated CI/CD Lifecycle Flow

Every single push or merge event directed into the primary production branch initiates this sequence within the pipeline:

1. **Syntax Integrity Evaluation (`test-and-lint`):** Pulls the runtime repository workspace, initializes a cached Python instance environment, runs `flake8` to assert syntax layout code parameters, and processes the test suite via `pytest`.
2. **Container Composition (`build-and-push`):** Builds a multi-stage optimized Docker production container footprint, updates image tags with the specific Git Commit shorthand SHA footprint, and pushes the production image to Docker Hub.
3. **AWS OIDC Verification Gate:** Requests a secure identity token exchange, logs into your AWS account dynamically, extracts your deployment cluster's current Task Definition file schema template, and replaces the target container tag with the newly compiled image ID.
4. **Zero-Downtime Service Stability Deployment:** Submits the modified blueprint structure back to AWS ECS. The cluster spins up your new code version containers, runs real-time health checks on the `/health` route parameters, and seamlessly routes incoming client requests over to the updated cluster tasks while gracefully draining connections to older tasks.

---

## 📂 Core Pipeline Reference Code

The automated workflow engine runs via the configuration stored directly inside your project path at `.github/workflows/ci.yml`:

```yaml
name: FastAPI CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test-and-lint:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
          cache-dependency-path: 'project-api/requirements.txt' 

      - name: Install dependencies
        working-directory: ./project-api
        run: |
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
          pip install pytest httpx flake8 

      - name: Lint with flake8
        working-directory: ./project-api
        run: |
          flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
          flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

      - name: Run tests with pytest
        working-directory: ./project-api
        env:
          PYTHONPATH: .
        run: |
          pytest

  build-and-push:
    needs: test-and-lint
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    
    permissions:
      id-token: write
      contents: read
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: \${{ vars.DOCKERHUB_USERNAME }}
          password: \${{ secrets.DOCKERHUB_TOKEN }}

      - name: Build and push Docker image
        uses: docker/build-push-action@v6
        with:
          context: ./project-api
          push: true
          tags: |
            \${{ vars.DOCKERHUB_USERNAME }}/fastapi-app:latest
            \({{ vars.DOCKERHUB_USERNAME }}/fastapi-app:\){{ github.sha }}

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: \${{ secrets.AWS_ROLE_ARN }}
          aws-region: \${{ vars.AWS_REGION }}

      - name: Download active task definition
        run: |
          aws ecs describe-task-definition --task-definition fastapi-task --query taskDefinition > task-definition.json

      - name: Fill in the new image ID in the Amazon ECS task definition
        id: render-task-def
        uses: aws-actions/amazon-ecs-render-task-definition@v1
        with:
          task-definition: task-definition.json
          container-name: main 
          image: \({{ vars.DOCKERHUB_USERNAME }}/fastapi-app:\){{ github.sha }}

      - name: Deploy Amazon ECS task definition
        uses: aws-actions/amazon-ecs-deploy-task-definition@v2
        with:
          task-definition: \${{ steps.render-task-def.outputs.task-definition }}
          service: fastapi-task-service-44vbmspx 
          cluster: api-cluster                  
          wait-for-service-stability: true      
```

---

## 📈 Budget Tracking & Financial Estimates (us-east-1)
* **Application Load Balancer Base Operation Cost:** ~$16.43/month
* **ECS Fargate Compute Container Node allocation (Single Active Task Base):** ~$5.50/month
* **CloudWatch Management Streams & Core Metrics Log Capture Allocation:** ~$1.00 - $3.00/month
* **Total Estimated Cost:** **~$22.93 - $24.93/month** *(Compute cost scales up linearly if Desired Task capacity limits are expanded to higher numbers for production scaling).*
