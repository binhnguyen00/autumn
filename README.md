<h1 align="center">Your wish is AI model's command</h1>

## Tech Stack
- Python
- React
- Websocket
- OpenAI's Whisper

## Getting Started
### 1. Clone repository
```bash
git clone https://github.com/binhnguyen00/autumn.git
```
### 2. [runtime](./runtime) is a quick way to start project for development
### 3. [docker](./docker-compose.yaml) is a production-ready setup
### 4. Prepare project structure
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
### 5. Prepare environment variables
- **For Docker**, copy ```.sample.env``` to ```.env``` and fill in your values
  ```bash
  cp .sample.env .env
  ```
- **For Shellscript**, copy ```.sample.env``` to ```.env``` and fill in your values
  ```bash
  cp ./runtime/env.example.sh ./runtime/env.sh
  ```

## Run Project
- ```frontend``` use port 3000
- ```backend``` use port 8080

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