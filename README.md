# CI/CD Final Project - Accounts Microservice

[![CI workflow](https://github.com/sak55shi/ci-cd-final-project/actions/workflows/workflow.yml/badge.svg)](https://github.com/sak55shi/ci-cd-final-project/actions/workflows/workflow.yml)

This project implements an Accounts microservice with automated continuous integration and continuous deployment.

## Technologies
- Python and Flask
- REST API
- Flake8 linting
- Nose unit tests
- Docker
- OpenShift and Tekton Pipelines
- GitHub Actions

## Continuous Integration
GitHub Actions checks out the repository, installs dependencies, runs Flake8 linting, and executes unit tests using nosetests.

## Continuous Deployment
The Tekton pipeline clones the repository, runs linting and tests, builds and pushes the container image, and deploys the application to OpenShift.

## Setup
Run the setup script in the lab environment:

\`\`\`bash
bash bin/setup.sh
\`\`\`

## License
Licensed under the Apache License 2.0. See [LICENSE](LICENSE).
