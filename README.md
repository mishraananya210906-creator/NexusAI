# NexusAI — Intelligent Support Assistant

An AI-powered customer support system that combines Retrieval-Augmented Generation (RAG) and Machine Learning to answer customer queries and intelligently classify support tickets.

## Overview

NexusAI is an intelligent support workspace designed to simplify customer service operations. It retrieves answers from support documentation and automatically categorizes customer tickets based on their content.

## Features

- **AI Support Assistant:** Answers customer questions using Retrieval-Augmented Generation (RAG).
- **Source Citations:** Displays the support documents used to generate answers.
- **Smart Ticket Classification:** Predicts ticket categories and priorities using machine learning.
- **Department Assignment:** Identifies the appropriate support department.
- **Analytics Dashboard:** Displays ticket distribution and model evaluation metrics.
- **REST API:** Provides backend endpoints for AI queries and ticket classification.
- **Rate Limiting:** Applies request limits to API endpoints.

## Technology Stack

| Component | Technologies |
|---|---|
| Frontend | React, JavaScript, CSS |
| Backend | Python, FastAPI |
| Machine Learning | Scikit-learn, TF-IDF, Logistic Regression |
| RAG | FastEmbed, FAISS, BM25 |
| Language Model Training | QLoRA, LoRA, DPO |
| API | REST API |
| Development | VS Code, Google Colab |

## System Architecture

1. A user interacts with the React frontend.
2. The frontend sends requests to the FastAPI backend.
3. The AI Assistant retrieves relevant information from support documents.
4. The ticket classifier predicts the category and priority of submitted tickets.
5. Results are returned to the frontend and displayed in the dashboard.

## Machine Learning Models

NexusAI uses two TF-IDF and Logistic Regression classifiers:

- Category Classifier
- Priority Classifier

### Evaluation Results

| Metric | Category Classifier | Priority Classifier |
|---|---:|---:|
| Accuracy | 84% | 60% |
| Macro F1-Score | 0.8367 | 0.5931 |

**Dataset:** 100 synthetic support tickets across five categories.

These are preliminary results from a small synthetic dataset and may differ on real-world data.

## AI Model Training Experiments

Training experiments were conducted using Google Colab:

- Supervised Fine-Tuning (SFT)
- Quantized LoRA (QLoRA)
- Direct Preference Optimization (DPO)

The resulting adapters were saved separately. They are experimental artifacts and are not currently loaded into the local application.

## Project Structure

```text
NexusAI/
├── api/
├── configs/
├── data/
│   ├── raw/
│   ├── processed/
│   └── evaluation/
├── docs/
├── frontend/
├── models/
├── notebooks/
├── src/
│   ├── rag/
│   ├── triage/
│   ├── training/
│   ├── evaluation/
│   └── inference/
├── tests/
├── .env.example
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd NexusAI
```

### 2. Create a Python virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install backend dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root and add your own API key:

```env
NEXUSAI_API_KEY=your_secret_api_key
```

Never upload your actual `.env` file or API key to GitHub.

### 5. Start the backend

```bash
python -m uvicorn api.main:app --reload
```

Backend API documentation:

`http://127.0.0.1:8000/docs`

### 6. Start the frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in your terminal, usually:

`http://localhost:5173`

## API Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/health` | GET | Health check |
| `/ask` | POST | Ask the AI Assistant |
| `/triage` | POST | Classify a support ticket |

The `/ask` and `/triage` endpoints require API-key authentication.

## Future Improvements

- Expand the support documentation knowledge base.
- Increase the size and diversity of the ticket dataset.
- Improve priority classification performance.
- Integrate trained language-model adapters into inference.
- Add persistent ticket storage and user authentication.
- Deploy the application to a production environment.

## Project Status

Core application features implemented:

- RAG-based AI Assistant
- Machine Learning Ticket Classification
- Analytics Dashboard
- FastAPI Backend
- React Frontend

---

**NexusAI — Intelligent Support Assistant**

Built with Python, React, Machine Learning and Retrieval-Augmented Generation.
