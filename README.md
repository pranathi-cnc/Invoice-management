# DocuVault Enterprise

A full-stack document and invoice management application combining a Python/FastAPI backend, PocketBase database, OCR-based document processing, and AI-assisted invoice extraction.

## Overview

DocuVault Enterprise is designed to simplify document management and invoice processing.

The application provides a web interface for authentication and document handling while using a backend service to process uploaded documents and extract structured invoice information.

## Key Features

* User authentication
* Document upload and management
* Invoice document processing
* OCR-based text extraction
* Image preprocessing
* AI-assisted invoice information extraction
* Structured invoice data generation
* Excel export
* PocketBase database integration
* FastAPI backend
* Web-based frontend

## Architecture

```text
                    User
                     │
                     ▼
              Web Frontend
             HTML / CSS / JS
                     │
                     ▼
              FastAPI Backend
                     │
          ┌──────────┼──────────┐
          │          │          │
          ▼          ▼          ▼
      Security    Document    PocketBase
                   Service      DB
                     │
                     ▼
               Invoice Pipeline
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
        OCR      Preprocessing  AI Parser
          │          │          │
          └──────────┼──────────┘
                     ▼
             Structured Invoice
                     │
                     ▼
                Excel Output
```

## Invoice Processing Pipeline

```text
Invoice Image / PDF
        ↓
Preprocessing
        ↓
OCR
        ↓
Extracted Text
        ↓
AI-based Parsing
        ↓
Structured Invoice Data
        ↓
Excel Export
```

## Tech Stack

### Backend

* Python
* FastAPI
* PocketBase
* Python security/authentication components

### AI / Document Processing

* OCR
* Image preprocessing
* LLM-assisted parsing
* Structured data extraction

### Frontend

* HTML
* CSS
* JavaScript

### Data Processing

* Excel
* PDF processing
* Image processing

## Project Structure

```text
docuvault-enterprise/
│
├── backend/
│   ├── auth.py
│   ├── main.py
│   ├── pocketbase_service.py
│   ├── security.py
│   │
│   └── invoice_ai/
│       ├── ai_parser.py
│       ├── excel_writer.py
│       ├── ocr.py
│       ├── preprocess.py
│       ├── processor.py
│       └── prompt.py
│
├── frontend/
│   ├── index.html
│   ├── login.html
│   ├── login.css
│   ├── login.js
│   ├── script.js
│   └── style.css
│
├── OCR_BILL_POC/
│   ├── ai_parser.py
│   ├── excel_writer.py
│   ├── extract.py
│   ├── ocr.py
│   ├── preprocess.py
│   ├── prompt.py
│   └── requirements.txt
│
├── pb_migrations/
│
├── .gitignore
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/pranathi-cnc/docuvault-enterprise.git
cd docuvault-enterprise
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

## Running the Backend

From the project directory:

```bash
uvicorn backend.main:app --reload
```

The API can then be accessed through the local FastAPI server.

## Data and Security

Runtime PocketBase data, uploaded documents, generated outputs, and executable binaries are intentionally excluded from this repository.

Sensitive configuration such as API keys and credentials should be stored in environment variables and never committed to GitHub.

## What I Worked On

The project involved implementing and integrating:

* OCR processing
* Invoice preprocessing
* AI-assisted invoice parsing
* Excel generation
* FastAPI backend functionality
* PocketBase integration
* Authentication and security components
* Frontend document-management workflows

## Future Improvements

* Add automated backend tests
* Add API documentation examples
* Improve OCR accuracy
* Add asynchronous document processing
* Add background job processing


## Author

**Pranathi Reddy Gangavarapu**

Machine Learning Engineer

GitHub: https://github.com/pranathi-cnc
