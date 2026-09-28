# 🥌 Curling Mobile Game — LiveOps & Backend Microservices

[![FastAPI](https://img.shields.io/badge/FastAPI-Python%203.11-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://curling-backend-services-733463952924.asia-south1.run.app)
[![Cloud Run](https://img.shields.io/badge/Google%20Cloud-Cloud%20Run-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white)](https://cloud.google.com/run)
[![Cloud SQL](https://img.shields.io/badge/Cloud%20SQL-MySQL-00758F?style=for-the-badge&logo=mysql&logoColor=white)](https://cloud.google.com/sql)

FastAPI microservice backend for **Curling Mobile Game**, deployed continuously to **Google Cloud Run**.

---

## 🌐 Live Service Endpoints

* **Base URL:** `https://curling-backend-services-733463952924.asia-south1.run.app`
* **Landing Page:** `GET /`
* **AdMob Auth:** `GET /app-ads.txt`
* **Timeshift Sync:** `GET /api/time`
* **Admin Timeshift:** `POST /api/admin/timeshift`
* **1v1 Matchmaking:** `WS /ws/matchmaking`
* **Health Check:** `GET /health`

---

## 🚀 Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure `.env`:
   ```env
   DB_TYPE=mysql
   DB_USER=your_user
   DB_PASSWORD=your_password
   DB_HOST=8.234.65.93
   DB_PORT=3306
   DB_NAME=curling_db
   ```
3. Run local server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```
