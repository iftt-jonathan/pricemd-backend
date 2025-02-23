#!/usr/bin/env bash
LAMBDA_PATH="./lambda"

echo "Zipping lambdas..."
zip -r lambda-output.zip $LAMBDA_PATH || exit 1

if [ ! -f .terraform.lock.hcl ]; then
  echo "Lock file does not exist. Running terraform init..."
  terraform init || exit 1
else
  echo "Lock file found. Skipping init."
fi

echo "Deploying infrastructure..."
terraform apply -auto-approve