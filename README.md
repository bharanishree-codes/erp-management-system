# ERP Management System

A backend microservices platform for managing staff, student, and academic workflows — including multi-level approval chains and condition-based execution flows — built with FastAPI and optimized for performance and scalability.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)
![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1?logo=mysql)
![SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy-red)

## Overview

This ERP Management System is a microservices-based backend that streamlines academic and institutional operations — covering staff records, student data, and academic workflows. It replaces fragmented, manual processes with automated approval chains and condition-based execution, significantly improving processing speed and system responsiveness.

**Performance highlights:**
- 📈 **30% improvement** in system performance through query indexing and data structure optimization
- ⚡ **80% reduction** in data processing time via API and ETL pipeline optimization

## Features

- **Microservices architecture** — modular services for staff, student, and academic domains
- **Approval chains** — configurable multi-level, condition-based workflow execution
- **Secure access** — JWT authentication with Role-Based Access Control (RBAC)
- **Optimized data layer** — indexed queries and tuned schemas via SQLAlchemy/MySQL
- **API documentation** — full endpoint documentation via Swagger/OpenAPI
- **Production-ready** — built-in support for incident handling and maintenance workflows

## Tech Stack

| Layer | Technology |
|---|---|
| Backend Framework | FastAPI, Django REST Framework (DRF) |
| ORM | SQLAlchemy |
| Database | MySQL |
| Authentication | JWT |
| API Docs | Swagger / OpenAPI |
| Version Control | Git |

## Project Structure

```
ERP/
├── app/
│   ├── models/
│   │   ├── v1_media.py
│   │   ├── v1_payment.py
│   │   ├── v1_staff.py
│   │   └── v1_student.py
│   ├── routers/
│   │   ├── v1_auth.py
│   │   ├── v1_media.py
│   │   ├── v1_payment.py
│   │   ├── v1_rbac.py
│   │   ├── v1_staff.py
│   │   └── v1_student.py
│   ├── schemas/
│   │   ├── v1_auth.py
│   │   ├── v1_media.py
│   │   ├── v1_payment.py
│   │   ├── v1_staff.py
│   │   └── v1_student.py
│   ├── utils/                  # Shared helper functions
│   ├── database.py             # DB session & engine setup
│   └── dependencies.py         # Shared FastAPI dependencies (auth, RBAC checks)
├── database.py                 # Root-level DB connection config
├── main.py                     # FastAPI app entry point
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10+
- MySQL 8.0+
- pip / virtualenv

### Installation

```bash
# Clone the repository
- git clone [https://github.com/bharanishree-codes/erp-management-system.git](https://github.com/bharanishree-codes/erp-management-system.git)

cd erp-management-system

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the development server
uvicorn main:app --reload
```


## API Documentation

FastAPI provides interactive API docs automatically:

- Swagger UI: `https://fastapi.hcaschennai.edu.in/docs`

## Key Contributions

- Designed backend microservices for staff, student, and academic workflows with approval chains and condition-based execution
- Improved system performance by 30% through query indexing and data structure optimization
- Reduced data processing time by 80% via API and ETL pipeline optimization
- Implemented JWT and RBAC across all services
- Documented all endpoints using Swagger/OpenAPI
- Supported production incidents and maintenance requests through the deployment lifecycle

## Contact

**Bharani Shree R**
Email: bharanishree2002.08@gmail.com
LinkedIn: [linkedin.com/in/bharanishree](https://linkedin.com/in/bharanishree)
