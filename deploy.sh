#!/usr/bin/env bash
LAMBDA_PATH="./lambdas"
TERRAFORM_PATH="./deployment"
VENV_PATH="./.venv"

set -e

if [ ! -d .venv ]; then
  echo "VENV not found. Running setup..."
  source setup.sh
else
  echo "VENV found. Skipping setup."
fi

echo "Zipping lambda layer..."
mkdir $TERRAFORM_PATH/python
cp -pr $VENV_PATH/lib $TERRAFORM_PATH/python/
(
  cd $TERRAFORM_PATH
  zip -FSr lambda-layer.zip python
  rm -r python
)

echo "Zipping lambdas..."
zip -FSr $TERRAFORM_PATH/lambda-output.zip $LAMBDA_PATH*

(
  cd $TERRAFORM_PATH

  if [ ! -f .terraform.lock.hcl ]; then
    echo "Lock file does not exist. Running terraform init..."
    terraform init
  else
    echo "Lock file found. Skipping init."
  fi

  echo "Deploying infrastructure..."
  terraform apply -auto-approve
)