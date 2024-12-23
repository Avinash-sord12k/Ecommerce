# E-Commerce Application

## Overview
This is a robust e-commerce application built with FastAPI, PostgreSQL, and Docker, providing a comprehensive backend solution for online shopping platforms.

## Project Structure
```
.
├── deploy                  # Deployment configurations
│   └── local               # Local deployment setup
│       ├── config          # Traefik configuration
│       ├── data            # Persistent data storage
│       ├── docker-compose.yml
│       └── scripts         # Deployment and testing scripts
├── fastapi                 # Backend application
│   ├── app                 # Main application modules
│   │   ├── cart            # Shopping cart functionality
│   │   ├── categories      # Product categorization
│   │   ├── products        # Product management
│   │   ├── roles           # User role management
│   │   └── tests           # Comprehensive test suite
│   └── Dockerfile          # Docker configuration
└── pyproject.toml          # Project configuration
```

## Key Features
- Comprehensive product management
- Shopping cart functionality
- Category and subcategory organization
- Role-based access control
- Robust testing framework

## Technologies
- Backend: FastAPI
- Database: PostgreSQL
- Containerization: Docker
- API Documentation: Swagger/OpenAPI
- Testing: Pytest

## Test Workflow Status
![Test Workflow](https://github.com/Ashish-Github193/Ecommerce/actions/workflows/github-actions.yml/badge.svg)

## Local Development Setup

### Prerequisites
- Docker
- Docker Compose

### Steps
1. Clone the repository
2. Natvigate to the repository
3. Build the application with these commands
```bash
chmod +x ./deploy/local/scripts/docker.build.sh
./deploy/local/scripts/docker.build.sh
```
4. Run the application with these commands
```bash
chmod +x ./deploy/local/scripts/docker.run.sh
./deploy/local/scripts/docker.run.sh
```

## Service Endpoints

After running the application, you can access the following services:

### Main Services
- FastAPI Application: http://fastapi.docker.localhost
- Traefik Dashboard: http://localhost:8003
- PGAdmin: http://pgadmin.docker.localhost

### API Documentation
- Swagger UI: http://fastapi.docker.localhost/api/docs
- ReDoc: http://fastapi.docker.localhost/api/redoc

### Notes
- Make sure to add the following entries to your `/etc/hosts` file:
  ```
  127.0.0.1    fastapi.docker.localhost
  127.0.0.1    pgadmin.docker.localhost
  ```
- For PGAdmin access:
  - Username: admin
  - Password: admin

## Running Tests
```bash
chmod +x ./deploy/local/scripts/docker.build.sh
./deploy/local/scripts/docker.build.sh

chmod +x ./deploy/local/scripts/pytest.run.sh
./deploy/local/scripts/pytest.run.sh
```

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
