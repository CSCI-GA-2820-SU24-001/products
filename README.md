# NYU DevOps Project Template

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Build Status](https://github.com/CSCI-GA-2820-SU24-001/products/actions/workflows/ci.yml/badge.svg)](https://github.com/CSCI-GA-2820-SU24-001/products/actions)
[![codecov](https://codecov.io/gh/CSCI-GA-2820-SU24-001/products/graph/badge.svg?token=64ffa5c4-25d2-40e6-be4a-1262d2bd4046)](https://codecov.io/gh/CSCI-GA-2820-SU24-001/products)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)

CSCI-GA.2820-003 DevOps and Agile Methodologies Summer 2024

## Overview

This project aims to represent the store items that customers can buy. This service will become a part of an e-commerce website.

## Contents

The project contains the following:

```text
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to gix Windows CRLF issues
.devcontainers/     - Folder with support for VSCode Remote Containers
dot-env-example     - copy to .env to use environment variables
pyproject.toml      - Poetry list of Python libraries required by your code
wsgi.py             - WSGI entry point for the application

features/                  - BDD features package
├── steps                  - step definitions for BDD
│   ├── products_steps.py  - BDD steps for products
│   ├── web_steps.py       - BDD steps for web interactions
├── environment.py         - BDD environment setup
└── products.feature       - BDD feature file

service/                   - service python package
├── __init__.py            - package initializer
├── config.py              - configuration parameters
├── models.py              - module with business models
├── routes.py              - module with service routes
└── common                 - common code package
    ├── cli_commands.py    - Flask command to recreate all tables
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    └── status.py          - HTTP status constants
└── static                      - static files package
    ├── css                     - CSS files
    ├── images                  - Image files
    ├── js                      - JavaScript files
    │   ├── bootstrap.min.js    - Bootstrap library for responsive design
    │   ├── jquery-3.6.0.min.js - jQuery library for simplified JavaScript operations
    │   └── rest_api.js         - JavaScript file for interacting with the REST API
    └── index.html              - Main HTML file for the web interface

tests/                     - test cases package
├── __init__.py            - package initializer
├── factories.py           - Factory for testing with fake objects
├── test_cli_commands.py   - test suite for the CLI
├── test_models.py         - test suite for business models
└── test_routes.py         - test suite for service routes
```

## Automatic Setup

1. clone repository

   ```
   $ git clone git@github.com:CSCI-GA-2820-SU24-001/products.git
   $ cd products
   ```

2. choose "reopen in Docker container" in VSCode

## Manual Setup

You can also clone this repository and then copy and paste the starter code into your project repo folder on your local computer. Be careful not to copy over your own `README.md` file so be selective in what you copy.

There are 4 hidden files that you will need to copy manually if you use the Mac Finder or Windows Explorer to copy files from this folder into your repo folder.

These should be copied using a bash shell as follows:

```bash
    cp .gitignore  ../<your_repo_folder>/
    cp .flaskenv ../<your_repo_folder>/
    cp .gitattributes ../<your_repo_folder>/
```

## APIs

The products service provides the following API endpoints:

| Operation              | Method | URL                       |
| ---------------------- | ------ | ------------------------- |
| **List all products**  | GET    | `/api/products`               |
| **Create a product**   | POST   | `/api/products`               |
| **Read a product**     | GET    | `/api/products/{id}`          |
| **Update a product**   | PUT    | `/api/products/{id}`          |
| **Delete a product**   | DELETE | `/api/products/{id}`          |
| **Purchase a product** | PUT    | `/api/products/{id}/purchase` |

## Running the Tests

To run the tests for this project, you can use the following command:

```bash
make test
```

This command will run the test suite using `pytest` and ensure that all the tests pass.

## Running the Service

To run the shopcarts service locally, you can use the following command:

```bash
honcho start
```

The service will start and be accessible at `http://localhost:8080`. To change the port, update the environment variable in the `.flaskenv` file.

## Deploy on Kubernetes Locally

To deploy the shopcarts service on Kubernetes locally, follow these steps:

* In order to create the cluster run:

```bash
make cluster
```

* To delete a cluster run
  
```bash
make cluster-rm
```

* Build the Docker image:

```bash
docker build -t product:latest .
```

* Tag the Docker image:

```bash
docker tag product:latest cluster-registry:5000/product:latest
```

* Push the Docker image to the cluster registry:

```bash
docker push cluster-registry:5000/product:latest
```

* Apply the Kubernetes configurations:

```bash
kubectl apply -f k8s/
```

The service will start and be accessible at `http://localhost:8080`.

## Swagger API Documentation

This service includes Swagger API documentation to help you understand and interact with the API. You can access the Swagger UI at the `/apidocs` endpoint of the deployed service. 


## License

Copyright (c) 2016, 2024 [John Rofrano](https://www.linkedin.com/in/JohnRofrano/). All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the New York University (NYU) masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by [John Rofrano](https://cs.nyu.edu/~rofrano/), Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.