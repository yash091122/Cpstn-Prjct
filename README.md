# FactForge - Review 2 Orchestration Module

This repository contains the Review 2 contribution for the B.Tech capstone project **FactForge**.

## Scope for Phase 2
- Claim-level orchestration
- Claim state machine
- Conditional routing
- Retry mechanism (max 2 retries)
- State-transition logging
- Unit tests

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

## Setup & Running
1. Activate virtual environment or create one:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run tests:
   ```bash
   pytest
   ```
4. Run main entry point:
   ```bash
   python main.py
   ```
