
#!/usr/bin/env bash
set -euo pipefail

IMAGE="ghcr.io/zeeshan40132/gke-gitops-platform:latest"
CLUSTER="gitops-local"
RELEASE="gitops-platform"
CHART="helm/gitops-platform"

echo "==> Pulling latest application image"
docker pull "$IMAGE"

echo "==> Loading image into kind cluster"
kind load docker-image "$IMAGE" --name "$CLUSTER"

echo "==> Deploying with Helm"
helm upgrade --install "$RELEASE" "$CHART" \
  --wait \
  --timeout 180s

echo "==> Waiting for Kubernetes rollout"
kubectl rollout status deployment/gitops-platform-app \
  --timeout=180s

echo "==> Checking application health"
curl --fail --silent --show-error \
  http://localhost:30080/health

echo
echo "==> Deployment successful!"
