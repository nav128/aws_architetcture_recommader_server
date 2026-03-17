mongo docker =`docker run --name mongodb -d -p 27017:27017 -v {C:\Users\win10\Documents\Moshe\data}:/data/db -e MONGODB_INITDB_ROOT_USERNAME=user -e MONGODB_INITDB_ROOT_PASSWORD=pass mongodb/mongodb-community-server:8.0-ubi8`


## Prerequisites
- Python 3.12+ (for local development)
- Docker & Docker Compose
- OpenAI API Key
- GitHub Token - Recomended

## Setup

### 1. Environment Variables
Copy `.env_example` to `.env` and fill in your credentials:

```bash
cp env_example .env
```

Edit `.env`:
```
MONGODB_URI=mongodb://user:pass@localhost:27017/?authSource=admin
OPENAI_API_KEY=your_openai_key_here
GITHUB_TOKEN=your_github_token_here
```

---

## Running Locally

### Option A: Manual MongoDB Docker + Local FastAPI
*** You can remove the volume mounting from the mongodb run if you do not care fore persistency
**Step 1: Start MongoDB Container**
```powershell
docker run --name mongodb -d -p 27017:27017 -v {your_local_path_for_mongodb_data}:/data/db -e MONGO_INITDB_ROOT_USERNAME=user -e MONGO_INITDB_ROOT_PASSWORD=pass mongo:8.0
```

**Step 2: Install Dependencies**
```powershell
pip instal setuptools && pip install -e .
```

**Step 3: Run FastAPI Server**
```powershell
cd src
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Server runs at: `http://localhost:8000`

---

## Running with Docker Compose

**All-in-one setup (MongoDB + FastAPI)**

```powershell
docker-compose up --build
```

This will:
- Start MongoDB container on port `27017`
- Build and start FastAPI app on port `8000`
- Auto-connect both services

Server runs at: `http://localhost:8000`

To stop:
```powershell
docker-compose down
```

---

## Testing the API

### Health Check
```powershell
curl http://localhost:8000/healthz
```

### Get Recommendations
```powershell
curl -X POST http://localhost:8000/recommendations `
  -H "Content-Type: application/json" `
  -d '{
    "use_case": "web_application",
    "scale": "medium",
    "traffic_pattern": "burst",
    "latency_sensitivity": "high",
    "processing_style": "request_response",
    "data_intensity": "medium",
    "availability_requirement": "high",
    "ops_preference": "balanced",
    "budget_sensitivity": "medium"
  }'
```

### Scrape AWS Architectures (First Time)
```powershell
curl http://localhost:8000/scrape-and-save
```

### Get All Architectures
```powershell
curl http://localhost:8000/architectures
```

---

## Stopping Containers

**Stop MongoDB (if running manually):**
```powershell
docker stop mongodb
docker rm mongodb
```

**Stop all Docker Compose services:**
```powershell
docker-compose down
```

---

## Troubleshooting

- **MongoDB connection error:** Ensure MongoDB container is running on port 27017
- **OpenAI API error:** Verify API key is valid in `.env`
- **Port already in use:** Change port in `docker-compose.yml` or command line
