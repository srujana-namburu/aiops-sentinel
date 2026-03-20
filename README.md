# 🚀 AIOps Sentinel — End-to-End Intelligent Incident Management System

AIOps Sentinel is a **production-grade, AI-driven incident intelligence platform** that simulates how modern SRE teams detect, analyze, and resolve system failures using **event-driven architecture, AI models, and observability pipelines**.

---

## 📌 Overview

AIOps Sentinel is designed to handle high-scale system incidents by decoupling ingestion, processing, and analysis using **Apache Kafka**, while leveraging **AI models for intelligent insights and automation**.

The system follows a **modular, scalable architecture** that supports real-time ingestion, asynchronous processing, AI-based analysis, and future self-healing capabilities.

---

## 🏗️ System Architecture

```text
                ┌───────────────┐
                │   Client/API  │
                └──────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Ingestion Layer │
              │   (FastAPI)     │
              └──────┬──────────┘
                     │
                     ▼
              ┌─────────────────┐
              │   Kafka Broker  │
              │ (Event Stream)  │
              └──────┬──────────┘
                     │
      ┌──────────────┼────────────────────┐
      ▼                                   ▼
┌───────────────┐                 ┌──────────────────┐
│ Consumer      │                 │ AI Analysis      │
│ (Processor)   │                 │ Service (LLM)    │
└──────┬────────┘                 └──────┬───────────┘
       │                                 │
       ▼                                 ▼
┌───────────────┐                 ┌──────────────────┐
│ Relational DB │                 │ Vector Database  │
│ (SQLite/Postgres)              │ (Embeddings)     │
└──────┬────────┘                 └──────┬───────────┘
       │                                 │
       ▼                                 ▼
┌────────────────────────────────────────────────────┐
│ Observability Layer (Logs, Metrics, Traces)        │
└────────────────────────────────────────────────────┘
```

---

## 🧩 Core Components

### 🔹 Ingestion Service (FastAPI)

* Accepts incident data via REST APIs
* Publishes events to Kafka
* Non-blocking, lightweight entry point

---

### 🔹 Kafka (Event Streaming Layer)

* Acts as a message broker
* Decouples ingestion and processing
* Enables asynchronous and scalable pipelines

---

### 🔹 Consumer Service

* Subscribes to Kafka topics
* Processes incoming events
* Persists incident data to database

---

### 🔹 Database Layer

* SQLite for local development
* PostgreSQL-ready for production
* Stores full incident lifecycle

---

### 🔹 AI Analysis Engine

* Uses LLMs to:

  * Analyze incidents
  * Suggest fixes
  * Identify root causes
* Populates `ai_analysis` field

---

### 🔹 Vector Database

* Stores embeddings of incidents
* Enables:

  * Semantic search
  * Similar incident detection

---

### 🔹 Observability Layer

* Metrics via Prometheus
* Structured logging
* Distributed tracing

---

### 🔹 Automation Layer

* Applies automated fixes
* Stores actions in `fix_applied`
* Enables self-healing workflows

---

## 🔄 End-to-End Workflow

1. Client sends incident → FastAPI
2. FastAPI publishes event → Kafka
3. Consumer reads event → stores in DB
4. AI engine analyzes incident → updates DB
5. System enriches incident with severity & insights
6. Observability tracks logs, metrics, traces
7. Automation layer applies fixes (if applicable)

---

## 📂 Project Structure

```text
aiops-sentinel/
│
├── ingestion-service/
│   ├── main.py                # FastAPI app (API layer)
│   ├── kafka_producer.py      # Kafka producer
│   ├── kafka_consumer.py      # Kafka consumer
│   ├── database.py            # DB models & session
│   ├── logger.py              # Logging setup
│
├── docker-compose.yml         # Kafka + Zookeeper
├── requirements.txt
├── README.md
```

---

## ⚙️ Tech Stack

| Layer            | Technology                |
| ---------------- | ------------------------- |
| API              | FastAPI                   |
| Messaging        | Apache Kafka              |
| Database         | SQLite / PostgreSQL       |
| ORM              | SQLAlchemy                |
| AI               | OpenAI / LLMs             |
| Vector DB        | FAISS / Pinecone          |
| Observability    | Prometheus, OpenTelemetry |
| Containerization | Docker                    |

---

## 🗄️ Data Model (Incident)

| Field             | Description           |
| ----------------- | --------------------- |
| display_id        | Auto-increment ID     |
| id                | UUID                  |
| service_name      | Service name          |
| error_message     | Error details         |
| error_count       | Frequency             |
| severity          | System/AI derived     |
| ai_analysis       | AI-generated insights |
| sre_decision      | Human/system action   |
| fix_applied       | Automated resolution  |
| correlation_id    | Request tracking      |
| trace_id          | Distributed tracing   |
| total_duration_ms | Processing time       |

---

## 🚀 Getting Started

### 1️⃣ Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/aiops-sentinel.git
cd aiops-sentinel
```

---

### 2️⃣ Setup Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### 3️⃣ Start Kafka

```bash
docker-compose up
```

---

### 4️⃣ Run Consumer

```bash
python kafka_consumer.py
```

---

### 5️⃣ Run API

```bash
uvicorn main:app --reload
```

---

### 6️⃣ Access API Docs

```
http://localhost:8000/docs
```

---

## 🧪 API Example

### Create Incident

```http
POST /incidents
```

```json
{
  "service_name": "payment-service",
  "error_message": "Out of memory error",
  "error_count": 15
}
```

### Response

```json
{
  "status": "QUEUED"
}
```

---

## 📈 Scalability & Design Decisions

* Event-driven architecture for loose coupling
* Kafka enables horizontal scaling
* Consumer-based processing allows parallel workloads
* Database abstraction supports easy migration
* AI layer decoupled for independent scaling

---

## 🔐 Production Readiness

* Stateless API layer
* Message-driven processing
* Fault-tolerant pipeline
* Extensible schema
* Observability hooks integrated

---

## 🎯 Use Cases

* Incident management systems
* AIOps platforms
* SRE automation tools
* Monitoring & alerting pipelines

---

## 👨‍💻 Author

**Srujana Namburu**

---

## ⭐ Support

If you found this project useful, give it a ⭐ on GitHub!
