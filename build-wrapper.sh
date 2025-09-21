#!/bin/bash

# Build script for Kokoro FastAPI Serverless Wrapper
set -e

# Configuration - CHANGE THESE TO YOUR VALUES
GITHUB_USERNAME="${GITHUB_USERNAME:-YOUR_USERNAME}"
IMAGE_NAME="kokoro-fastapi-serverless"
REGISTRY="ghcr.io/${GITHUB_USERNAME}"
TAG="${1:-latest}"

echo "Building ${IMAGE_NAME}:${TAG} (wrapper approach)..."
echo "Base image: ghcr.io/remsky/kokoro-fastapi-gpu:latest"
echo "Target registry: ${REGISTRY}"

# Check if username is set
if [ "${GITHUB_USERNAME}" = "YOUR_USERNAME" ]; then
    echo "❌ Please set your GitHub username:"
    echo "   export GITHUB_USERNAME=your-github-username"
    echo "   OR edit this script to replace YOUR_USERNAME"
    exit 1
fi

# Build the wrapper Docker image
docker build \
    -f Dockerfile.wrapper \
    -t "${IMAGE_NAME}:${TAG}" \
    -t "${REGISTRY}/${IMAGE_NAME}:${TAG}" \
    .

echo "✅ Build complete! Image tagged as:"
echo "  ${IMAGE_NAME}:${TAG}"
echo "  ${REGISTRY}/${IMAGE_NAME}:${TAG}"

echo ""
echo "📦 To push to GitHub Container Registry:"
echo "  1. Login: docker login ghcr.io -u ${GITHUB_USERNAME}"
echo "  2. Push:  docker push ${REGISTRY}/${IMAGE_NAME}:${TAG}"

echo ""
echo "🧪 To test locally:"
echo "  docker run --gpus all -p 8000:8000 ${IMAGE_NAME}:${TAG}"

echo ""
echo "🚀 For RunPod Serverless deployment:"
echo "  1. Push image to registry (commands above)"
echo "  2. Use image: ${REGISTRY}/${IMAGE_NAME}:${TAG}"
echo "  3. Configure GPU requirements in RunPod template"

echo ""
echo "💡 Alternative: Use GitHub Actions to build automatically"
echo "  See .github/workflows/build.yml for automated builds"