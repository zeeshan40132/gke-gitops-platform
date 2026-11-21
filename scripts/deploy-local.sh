
#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: bash scripts/deploy-local.sh <image-tag>"
  echo "Example: bash scripts/deploy-local.sh sha-1105fbb5d66c4fd54fd24d4488ec63402fb3a09c"
  exit 1
fi

IMAGE_REPOSITORY="ghcr.io/zeeshan40132/gke-gitops-platform"
IMAGE_TAG="$1"
IMAGE="${IMAGE_REPOSITORY}:${IMAGE_TAG}"

CLUSTER="gitops-local"
RELEASE="gitops-platform"
CHART="helm/gitops-platform"

echo "==> Deploying image: $IMAGE"

echo "==> Pulling image"
docker pull --platform linux/amd64 "$IMAGE"

echo "==> Loading image into kind"
kind load docker-image "$IMAGE" --name "$CLUSTER"

echo "==> Deploying with Helm"
helm upgrade --install "$RELEASE" "$CHART" \
  --set-string image.repository="$IMAGE_REPOSITORY" \
  --set-string image.tag="$IMAGE_TAG" \
  --wait \
  --timeout 180s

echo "==> Waiting for rollout"
kubectl rollout status deployment/gitops-platform-app \
  --timeout=180s

echo "==> Checking application health"
curl --fail --silent --show-error \
  http://localhost:30080/health

echo
echo "==> Deployment successful: $IMAGE"
