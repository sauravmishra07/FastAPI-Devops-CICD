# FastAPI Todo App

Simple in-memory TODO web app using FastAPI and Jinja2 templates.

## Project layout

- `app/main.py` — FastAPI application
- `app/templates/index.html` — Jinja2 template
- `requirements.txt` — Python dependencies
- `terraform/` — Infrastructure as Code for AWS deployment

### Folder Structure

```
Todo-app/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── app/
│   ├── main.py              # FastAPI application
│   ├── __pycache__/         # Python cache files
│   └── templates/
│       └── index.html       # Jinja2 template
└── terraform/
    ├── main.tf              # Terraform main configuration
    ├── provider.tf          # AWS provider settings
    ├── ec2.tf               # EC2 instance configuration
    ├── security_group.tf    # Security group configuration
    └── output.tf            # Terraform outputs
```

## Requirements

- Python 3.8+
- Terraform 1.0+ (for infrastructure deployment)
- See `requirements.txt` for exact Python packages

## Setup

1. Create a virtual environment and activate it:

```bash
python -m venv .venv
# Windows (cmd):
.venv\Scripts\activate
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. (Optional) Create a `.env` file in the project root to override app settings:

```
APP_NAME=My Todo App
APP_VERSION=0.1.0
```

## Run

Start the app with Uvicorn from the repository root:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open http://127.0.0.1:8000 in your browser.

## API Docs

FastAPI exposes interactive API documentation when the app is running locally.

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- OpenAPI JSON: http://127.0.0.1:8000/openapi.json

You can fetch the raw OpenAPI spec with curl:

```bash
curl http://127.0.0.1:8000/openapi.json
```

## Notes

- Todos are stored in `app/todos.json` and will persist between server restarts.
- The template files live in `app/templates` and use Jinja2.
