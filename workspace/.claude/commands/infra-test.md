# Infrastructure Test Generator

Diseña tests para infraestructura: Kubernetes, Docker, Terraform, CI/CD pipelines.

## Instrucciones

1. **Identifica componentes** — ¿Qué infraestructura se va a testear?
2. **Define assertions** — ¿Qué debe cumplirse?
3. **Crea scenarios** — Tests para cada componente
4. **Genera scripts** — Código ejecutable de validación
5. **Integra con CI** — Cómo ejecutar en pipelines

## Output Format

### Kubernetes Tests

```yaml
# tests/infra/k8s/deployment.test.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: k8s-tests
data:
  test-deployment.sh: |
    #!/bin/bash
    set -e

    NAMESPACE="${NAMESPACE:-default}"
    DEPLOYMENT="${DEPLOYMENT:-app}"

    echo "Testing deployment: $DEPLOYMENT in $NAMESPACE"

    # Test 1: Deployment exists
    kubectl get deployment $DEPLOYMENT -n $NAMESPACE || exit 1

    # Test 2: All replicas ready
    READY=$(kubectl get deployment $DEPLOYMENT -n $NAMESPACE -o jsonpath='{.status.readyReplicas}')
    DESIRED=$(kubectl get deployment $DEPLOYMENT -n $NAMESPACE -o jsonpath='{.spec.replicas}')
    [ "$READY" -eq "$DESIRED" ] || exit 1

    # Test 3: No restarts in last hour
    RESTARTS=$(kubectl get pods -n $NAMESPACE -l app=$DEPLOYMENT -o jsonpath='{.items[*].status.containerStatuses[*].restartCount}')
    for r in $RESTARTS; do
      [ "$r" -lt 3 ] || exit 1
    done

    # Test 4: Resource limits set
    kubectl get deployment $DEPLOYMENT -n $NAMESPACE -o jsonpath='{.spec.template.spec.containers[*].resources.limits}' | grep -q "memory" || exit 1

    echo "All tests passed!"
```

### Kubernetes with kubectl-assert

```bash
# Using kubectl-assert plugin
kubectl assert exist deployment/myapp -n production
kubectl assert condition deployment/myapp Available=True
kubectl assert jsonpath deployment/myapp '{.spec.replicas}' -eq 3
kubectl assert pods -l app=myapp --field-selector=status.phase=Running
```

### Docker Image Tests

```dockerfile
# tests/infra/docker/Dockerfile.test
FROM myapp:latest AS test

# Test 1: Required binaries exist
RUN which node && which npm

# Test 2: App directory structure
RUN test -d /app && test -f /app/package.json

# Test 3: No root user
RUN test "$(id -u)" != "0"

# Test 4: Health check works
HEALTHCHECK --interval=5s --timeout=3s \
  CMD curl -f http://localhost:3000/health || exit 1

# Test 5: Required env vars documented
RUN env | grep -q "NODE_ENV"
```

### Container Structure Tests (Google)

```yaml
# tests/infra/docker/structure-test.yaml
schemaVersion: 2.0.0

metadataTest:
  user: "node"
  workdir: "/app"
  exposedPorts: ["3000"]

commandTests:
  - name: "node is installed"
    command: "node"
    args: ["--version"]
    expectedOutput: ["v20"]

  - name: "app starts"
    command: "node"
    args: ["dist/main.js", "--help"]
    exitCode: 0

fileExistenceTests:
  - name: "package.json exists"
    path: "/app/package.json"
    shouldExist: true

  - name: "no dev dependencies"
    path: "/app/node_modules/.bin/jest"
    shouldExist: false

fileContentTests:
  - name: "correct node version"
    path: "/app/.nvmrc"
    expectedContents: ["20"]
```

### Terraform Tests

```hcl
# tests/infra/terraform/main.tftest.hcl

variables {
  environment = "test"
  region      = "us-east-1"
}

run "validate_vpc" {
  command = plan

  assert {
    condition     = aws_vpc.main.cidr_block == "10.0.0.0/16"
    error_message = "VPC CIDR block is incorrect"
  }

  assert {
    condition     = aws_vpc.main.enable_dns_hostnames == true
    error_message = "DNS hostnames should be enabled"
  }
}

run "validate_subnets" {
  command = plan

  assert {
    condition     = length(aws_subnet.private) == 3
    error_message = "Should have 3 private subnets"
  }

  assert {
    condition     = length(aws_subnet.public) == 3
    error_message = "Should have 3 public subnets"
  }
}

run "security_group_rules" {
  command = plan

  assert {
    condition     = !contains([for rule in aws_security_group.web.ingress : rule.cidr_blocks], ["0.0.0.0/0"])
    error_message = "Security group should not allow all inbound traffic"
  }
}
```

### CI/CD Pipeline Tests

```yaml
# .github/workflows/infra-tests.yml
name: Infrastructure Tests

on:
  pull_request:
    paths:
      - 'infra/**'
      - 'k8s/**'
      - 'Dockerfile'

jobs:
  docker-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build image
        run: docker build -t app:test .

      - name: Run structure tests
        uses: plexsystems/container-structure-test-action@v0.3.0
        with:
          image: app:test
          config: tests/infra/docker/structure-test.yaml

  terraform-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: hashicorp/setup-terraform@v3

      - name: Terraform Init
        run: terraform init
        working-directory: infra/

      - name: Terraform Test
        run: terraform test
        working-directory: infra/

  k8s-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Create kind cluster
        uses: helm/kind-action@v1

      - name: Deploy manifests
        run: kubectl apply -f k8s/

      - name: Wait for ready
        run: kubectl wait --for=condition=available deployment --all --timeout=120s

      - name: Run tests
        run: ./tests/infra/k8s/run-tests.sh
```

### Chaos Engineering Tests

```yaml
# tests/infra/chaos/pod-failure.yaml
apiVersion: chaos-mesh.org/v1alpha1
kind: PodChaos
metadata:
  name: pod-failure-test
spec:
  action: pod-failure
  mode: one
  selector:
    namespaces:
      - production
    labelSelectors:
      app: myapp
  duration: "30s"
---
# Validation script
# After chaos: verify service recovered
# - Health endpoint returns 200
# - No data loss
# - Alerts triggered correctly
```

## Test Categories

| Category | Tools | Focus |
|----------|-------|-------|
| K8s Manifests | kubectl, kubeval, kubeconform | YAML validity, best practices |
| K8s Runtime | kubectl-assert, kuttl | Live cluster state |
| Docker | container-structure-test, dive | Image content, size |
| Terraform | terraform test, tflint | Plan validation |
| Helm | helm lint, helm test | Chart correctness |
| Chaos | chaos-mesh, litmus | Resilience |

## Consideraciones

- Ejecuta tests en clusters efímeros (kind, k3d)
- Usa namespaces aislados para tests
- Limpia recursos después de cada test
- Testea rollback y recovery
- Valida políticas de seguridad (OPA/Gatekeeper)
