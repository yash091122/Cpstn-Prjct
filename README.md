# FactForge - Orchestration Module (Review 2)

Claim-level orchestration module for B.Tech Capstone Project "FactForge".

## Core Scope (Review 2)
- Claim-level orchestration
- Claim state machine
- Conditional routing
- Retry mechanism (max 2 retries)
- State-transition logging
- Unit tests

## Tech Stack
- Python 3.11+
- LangGraph
- Pydantic
- pytest
- Python standard logging

## Project Structure
```
factforge/
├── orchestration/
│   ├── __init__.py
│   ├── state.py
│   ├── router.py
│   ├── nodes.py
│   └── graph.py
│
├── tests/
│   ├── __init__.py
│   ├── test_router.py
│   ├── test_state_machine.py
│   └── test_retry.py
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Environment Setup & Installation
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running Tests
```bash
pytest
```

## Running Main
```bash
python main.py
```
