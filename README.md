# Kubernetes Job Execution Platform

## Screenshots

### Job Submission UI:

<img width="1509" height="912" alt="Screenshot 2026-03-16 at 8 37 49 PM" src="https://github.com/user-attachments/assets/a7c91f5b-ee9c-428d-9ac1-6a3bda887e71" />
<img width="1506" height="847" alt="Screenshot 2026-03-16 at 8 38 27 PM" src="https://github.com/user-attachments/assets/67300463-2afc-409b-9b0f-f8297c102616" />


### Kubernetes Pods: 

<img width="630" height="168" alt="Screenshot 2026-03-16 at 8 41 06 PM" src="https://github.com/user-attachments/assets/115bb9d4-4a49-47b9-a2bb-80259654d1a7" />




## Overview
This project is a **Kubernetes-based Job Execution Platform** that allows users to submit containerized jobs through a web interface, monitor job execution status, and retrieve logs from Kubernetes job pods. The system uses a **FastAPI backend** to interact with the Kubernetes API and a **Streamlit frontend** for the user interface. The platform demonstrates container orchestration, job management, and Kubernetes resource interaction.

---

## System Architecture

User → Streamlit Frontend → FastAPI Backend → Kubernetes API → Job Pod

Browser
   │
   ▼
Frontend (Streamlit)
   │
   ▼
Backend API (FastAPI)
   │
   ▼
Kubernetes API Server
   │
   ▼
Job Controller
   │
   ▼
Pod → Container → Execute Job


## Tech Stack

### Backend
- Python
- FastAPI
- Kubernetes Python Client

### Frontend
- Streamlit

### Containerization
- Docker

### Orchestration
- Kubernetes  
- Minikube (Local Kubernetes Cluster)

### Database
- SQLite

---

## Features

- Submit Kubernetes jobs using container images
- Monitor job execution status
- Fetch logs from job pods
- View all submitted jobs
- Backend integration with Kubernetes API
- Dockerized backend and frontend services
- Kubernetes deployment using YAML configuration files

---

## Project Structure

## Project Structure

```
k8s-job-platform
│
├── backend
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── routes.py
│   ├── job_service.py
│   ├── k8s_client.py
│   ├── db_manager.py
│
├── frontend
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app.py
│
├── k8s
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── frontend-deployment.yaml
│   ├── frontend-service.yaml
│   ├── db-pvc.yaml
│
├── rbac.yaml
├── main.py
└── README.md
```

---

## System Workflow

1. User submits a job through the **Streamlit UI**.  
2. The frontend sends a request to the **FastAPI backend**.  
3. The backend creates a **Kubernetes Job** using the Kubernetes Python client.  
4. Kubernetes creates a **Pod** to execute the job container.  
5. The container runs the specified command.  
6. The backend fetches **job status and logs** from Kubernetes.  
7. Job details are stored and updated in the **SQLite database**.

---

## Kubernetes Resources Used

The project uses the following Kubernetes resources:

- **Deployment** – Manages frontend and backend pods
- **Service** – Provides network access to pods
- **NodePort** – Exposes the frontend application outside the cluster
- **RBAC** – Grants the backend permission to interact with the Kubernetes API
- **Job** – Executes containerized tasks

---

## Running the Project

### 1. Start Minikube

```bash
minikube start
```

---

### 2. Deploy Kubernetes Resources

```bash
kubectl apply -f k8s/
kubectl apply -f rbac.yaml
```

This deploys:

- Backend Deployment and Service
- Frontend Deployment and Service
- RBAC permissions for Kubernetes API access

---

### 3. Access the Application

```bash
minikube service frontend-service
```

This opens the **Streamlit UI** in your browser.

---

## Example Job Input

Example job submitted through the UI:

```
Job Name: test-job
Image: python:3.11
Command: python -c "print('Hello from Kubernetes')"
CPU: 500m
Memory: 256Mi
Namespace: default
```

---

## Example Kubernetes Output

Check running pods:

```bash
kubectl get pods
```

Example output:

```
frontend-xxxxx   Running
backend-xxxxx    Running
test-job-xxxxx   Completed
```

---

## Viewing Job Logs

Logs are retrieved from Kubernetes job pods using the backend API.

Example output:

```
Hello from Kubernetes
```

---

## Future Improvements

- Persistent database using PostgreSQL
- Job retry mechanism
- User authentication
- Job history dashboard
- Kubernetes job cleanup automation

---

## Author

**Karthik B**  
B.Tech Computer Science – PES University  

GitHub:  
https://github.com/Karthik2003B

---

## Repository Link

https://github.com/Karthik2003B/k8s-job-platform
