<h1 align="center">Your wish is AI model's command</h1>

## Tech Stack
- Python
- React
- Websocket
- OpenAI's Whisper

## To Run
- ```frontend``` use port 3000
- ```backend``` use port 8080

### 1. Prepare project structure
```plaintext
autumn/
├── .autumn-venv/
├── runtime/
├── src/
│   ├── backend/
│   └── frontend/
├── .env
├── docker-compose.yaml
└── README.md
```

### 1. Docker
```bash
docker compose up --build
```
- Docker should have at least 4GB of RAM

### 2. Shellscript on your machine
```bash
# download whisper model
./runtime/backend.sh download-whisper-model

# start backend
./runtime/backend.sh start

# start frontend
./runtime/frontend.sh start
```

## Author - Binh Nguyen
- **[Github](https://github.com/binhnguyen00)**
- **[Gmail](mailto:jackjack2000.kahp@gmail.com)**