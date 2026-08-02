# AI Support Agent

## Overview

This project implements a **Local-First AI Support Agent** using **LangGraph**, **Sentence Transformers**, **FAISS**, and **Hugging Face Transformers**.

The system answers support questions using a fictional OrbitDesk knowledge base. It classifies user queries, retrieves relevant documents, generates responses using a local Hugging Face language model, verifies the generated response, and returns both a human-readable answer and structured JSON output.

The application runs completely **locally** after the required models are downloaded.

---

## Features

- LangGraph-based workflow
- Typed shared state
- Question triage
- Local document retrieval using FAISS
- Local Hugging Face language model
- Response verification
- Retry / Safe failure path
- Structured JSON output
- Source references
- Execution logs

---

## Workflow

```
                User Question
                      │
                      ▼
                 Triage Node
                      │
      ┌───────────────┼───────────────┐
      │               │               │
      ▼               ▼               ▼
Clarification   Out of Scope     Answerable
      │               │               │
      ▼               ▼               ▼
 Ask User      Safe Response     Retriever
                                      │
                                      ▼
                                FAISS Search
                                      │
                                      ▼
                             TinyLlama Generator
                                      │
                                      ▼
                                Verification
                                      │
                            ┌─────────┴─────────┐
                            │                   │
                            ▼                   ▼
                      Final Answer         Retry Once
```

---

## Project Structure

```
AI-Support-Agent/
│
├── app.py
├── graph.py
├── retriever.py
├── verifier.py
├── prompts.py
├── knowledge_base/
├── sample_questions.json
├── resolved_cases.json
├── output_schema.json
├── requirements.txt
└── README.md
```

---

## Models Used

### Embedding Model

- sentence-transformers/all-MiniLM-L6-v2

### Language Model

- TinyLlama/TinyLlama-1.1B-Chat-v1.0

---

## Hardware Used

- **Operating System:** Windows 11
- **CPU:** 11th Gen Intel(R) Core(TM) i5-1135G7 @ 2.40GHz
- **RAM:** 8 GB
- **GPU:** CPU Only
- **Python Version:** 3.11
- **Approximate Model Load Time:** 1 minute 19 seconds
- **Approximate Response Time:** 1 minute 09 seconds

---

## Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_LINK
```

Move to the project folder:

```bash
cd AI-Support-Agent
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment (Windows):

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Run the Project

```bash
python app.py
```

---

## Sample Test Cases

### 1. Answerable Question

```
Can a read-only user create API credentials?
```

### 2. Multi-document Retrieval

```
My scheduled exports stopped after I changed my workspace timezone. What should I check?
```

### 3. Clarification

```
Help
```

### 4. Out of Scope

```
Refund my subscription.
```

### 5. Escalation

```
My account has been hacked.
```

---

## Sample JSON Output

```json
{
    "classification": "answerable",
    "answer": "No. Read-only users (Viewers) cannot create API credentials. Only Owners and Admins can create or revoke API credentials.",
    "sources": [
        {
            "document": "05_api_credentials.md"
        }
    ],
    "confidence": 0.95,
    "requires_human": false,
    "reason": "Answer found in knowledge base."
}
```

---

## Hardware Requirements

- Python 3.11 or later
- Minimum 8 GB RAM
- CPU execution supported
- Internet required only for the initial model download
- Around 3–4 GB free disk space for Hugging Face models

---

## Known Limitations

- Small local language models may occasionally generate inaccurate responses.
- Verification performs basic validation and is not a full fact-checking system.
- Retrieval quality depends on the supplied knowledge base.
- Designed as an internship assignment and demonstration project rather than a production-ready system.

---

## AI Assistance

AI coding assistance (ChatGPT) was used during development to:

- Explain LangGraph concepts
- Generate initial boilerplate code
- Assist with debugging Python errors
- Suggest improvements for retrieval and verification logic
- Review project structure and documentation

The final project integration, testing, debugging, and validation were completed by the author.

---

## Author

**Sanket Digambar Kolhe**

B.Tech Computer Engineering

MIT Academy of Engineering (MITAOE)

Graduation Year: 2026