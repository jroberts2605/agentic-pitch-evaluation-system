# Agentic AI Pitch Evaluation System

A Python project that uses multiple AI agents to classify startup pitches, route them through category-specific coaching prompts, evaluate them against rubric-based criteria, and refine weak drafts until they meet the required bar or clearly surface missing evidence.

This repository demonstrates an LLM-powered workflow for a practical product challenge: helping founders improve rough pitch narratives without making unsupported claims. The system is intentionally evidence-first. If a pitch lacks traction, customer specificity, or technical proof points, it flags the gap instead of fabricating a stronger story.

## Project at a glance

- Problem: early-stage pitches are often strong in concept but weak in structure, evidence, and category-specific fit.
- Solution: route each pitch through a classifier, specialized coach, evaluator, and optimizer loop.
- Outcome: produce a more credible draft and make missing evidence explicit.
- Core idea: evaluate quality with structure, not optimism.

## Why this project exists

Founders often have a promising idea but an incomplete pitch. The challenge is not only clarity; it is alignment with the expectations of the startup category and the standards of evidence.

This repository explores that problem by combining:

- classification into Consumer, B2B SaaS, or Deep Tech,
- category-specific coaching guidance,
- runtime rubric retrieval through an MCP server,
- structured outputs for consistent evaluation,
- bounded optimization loops that revise weak drafts without inventing facts.

The result is a workflow that identifies gaps in a pitch and makes them visible to the founder rather than silently filling them with unsupported details.

## Core workflow

The system follows a simple sequence:

1. A raw pitch is classified as Consumer, B2B SaaS, or Deep Tech.
2. The pitch is routed to a coaching agent specialized for that startup type.
3. An evaluator requests the matching rubric from the MCP server.
4. The evaluator scores the draft against each criterion.
5. If the pitch fails, an optimizer revises it using the evaluator's feedback.
6. The loop continues until the pitch passes or reaches the three-iteration cap.

This makes the project a useful demonstration of agentic workflow design: a structured pipeline where each step has a clear role, a clear set of inputs, and a clear output.

## Quick start

If you want the fastest way to run the project locally:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m examples.run_demo
```

This command runs the demo pipeline for the included example pitches and prints the final classification, revision loop, and evaluation results.

## Architecture

```text
                           ┌────────────────────┐
                           │  Startup pitch     │
                           └─────────┬──────────┘
                                     │
                                     ▼
                           ┌────────────────────┐
                           │  Pitch classifier  │
                           └─────────┬──────────┘
                                     │
                     ┌───────────────┼───────────────┐
                     ▼               ▼               ▼
        ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
        │ Consumer coach   │ │ B2B SaaS coach   │ │ Deep tech coach  │
        └─────────┬────────┘ └─────────┬────────┘ └─────────┬────────┘
                  │                   │                   │
                  └───────────────┬───────────────────┘
                                      ▼
                              ┌──────────────────┐
                              │  Evaluator agent │
                              │  + MCP rubric    │
                              └────────┬─────────┘
                                       │
                            ┌──────────┴──────────┐
                            │                     │
                            ▼                     ▼
                     Passes                     Fails
                        │                        │
                        ▼                        ▼
                 Final pitch             Optimizer
                                            │
                                            └────► Evaluator
```

The architecture is intentionally modular. The classifier is separate from the coaches, the evaluator retrieves rubrics at runtime instead of hard-coding them, and the optimizer is explicitly constrained to avoid inventing missing evidence.

## Technologies

- Python 3.12 for the application logic and orchestration
- OpenAI Agents SDK for agent execution and routing
- Model Context Protocol (MCP) for runtime rubric retrieval
- Pydantic for structured, typed outputs
- AsyncIO for asynchronous execution in the pipeline

## Repository structure

```text
agentic-pitch-evaluation-system/
├── examples/
│   ├── pitches.py
│   ├── run_demo.py
│   └── sample_results.md
├── mcp/
│   └── rubric_server.py
├── src/
│   ├── pipeline.py
│   ├── pitch_agents.py
│   └── schemas.py
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── .venv/   # local environment, not committed
```

## Example workflow

The repository includes three synthetic startup pitches that exercise each supported category:

- SnackPocket — Consumer product
- ShiftRoster — B2B SaaS
- KitchenSense — Deep tech

These examples are defined in [examples/pitches.py](examples/pitches.py) and processed by the demo script in [examples/run_demo.py](examples/run_demo.py).

The expected behavior is demonstrated in [examples/sample_results.md](examples/sample_results.md):

- SnackPocket passes in one iteration.
- ShiftRoster does not pass until the missing traction signal is explicitly called out.
- KitchenSense does not pass until the first-customer requirement is specified.

This behavior is intentional. The system is designed to favor evidence and clarity over artificially inflating a pitch to satisfy the rubric.

## Setup and installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd agentic-pitch-evaluation-system
```

### 2. Create a virtual environment

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

The current dependency set is intentionally small and is defined in [requirements.txt](requirements.txt):

```text
openai-agents==0.20.0
pydantic==2.13.4
ipython==9.16.1
```

### 4. Configure the API key

Copy [.env.example](.env.example) to `.env` and add your OpenAI API key.

```text
OPENAI_API_KEY=your_api_key_here
```

Important:
- do not commit `.env`
- do not add real credentials to source code
- keep environment variables local to your machine

### 5. Run the demo

```bash
python examples/run_demo.py
```

This script walks through each example pitch and prints the final draft, pass/fail result, and evaluator feedback.

## Key technical decisions

### Dynamic rubric retrieval

The rubric logic is not embedded directly in the evaluator prompt. Instead, the evaluator requests the relevant rubric from the MCP server in [mcp/rubric_server.py](mcp/rubric_server.py). This keeps evaluation criteria separate from agent behavior and makes the system easier to evolve without rewriting the orchestration layer.

### Structured outputs

The system uses Pydantic models in [src/schemas.py](src/schemas.py) to enforce predictable outputs from the LLM. This helps convert free-form agent responses into structured data that can be used downstream in the pipeline.

### Specialized coaching by startup type

Rather than using one generic pitch-writer, the project routes each pitch to a coach tailored for Consumer, B2B SaaS, or Deep Tech scenarios. This makes the rewrite step more aligned with the investor expectations and common pitch patterns for each category.

### Bounded optimization

The optimization loop in [src/pipeline.py](src/pipeline.py) is capped at three iterations. That prevents a runaway loop while still allowing the pitch to improve when there are meaningful weaknesses.

### Evidence-first behavior

One of the strongest choices in this project is that the optimizer is instructed not to fabricate missing facts. Instead of guessing customer numbers or traction, it surfaces placeholders such as `[TRACTION SIGNAL NEEDED: founder must cite a specific pilot, paying customer, or letter of intent]` when information is missing. This makes the system more realistic than a naive "always make it pass" solution and demonstrates a product-minded approach to AI evaluation.

## Implementation notes

### Pipeline logic

The orchestration logic lives in [src/pipeline.py](src/pipeline.py). It handles:

- classification,
- coach selection,
- rubric-aware evaluation,
- feedback-driven revision,
- early exit when the pitch passes.

### Agent definitions

The AI agents are defined in [src/pitch_agents.py](src/pitch_agents.py). This file contains the specialized startup coaches, the classifier, and the optimizer agent.

### MCP rubric server

The MCP server in [mcp/rubric_server.py](mcp/rubric_server.py) exposes a `get_rubric` tool that returns a rubric based on the requested pitch category.

## Example results

A few sample outputs are included in [examples/sample_results.md](examples/sample_results.md). They demonstrate both successful and unsuccessful cases and explain the reasoning behind the evaluator's final judgment.

This is useful for understanding not just whether a pitch passed, but why and which criteria were missing.

## Security and secrets

This repository does not contain hard-coded secrets or API keys. The project uses the standard `.env` pattern, and the top-level [.gitignore](.gitignore) excludes environment files and local caches.

Best practice:

- keep secrets in a local `.env` file,
- do not commit `.env` files,
- avoid hard-coding credentials in code or documentation,
- review any generated outputs before publishing them externally.

## Project scope and limitations

This repository is a focused prototype rather than a full production application. It demonstrates an agentic evaluation workflow and shows how MCP, schema enforcement, and category-specific coaching can be combined in a single pipeline.

The project currently highlights the workflow through sample pitches and example output rather than through a formal test suite or production deployment setup.

## What this project demonstrates

This repository is a compact example of:

- multi-agent orchestration,
- rubric-driven evaluation,
- structured LLM outputs,
- domain-specific agent behavior,
- evidence-aware iteration rather than fabricated optimization.

That combination makes it a strong demonstration of product-minded AI system design, especially for work that blends technical execution with clear business judgment.

- category-specific agent behavior,
- evidence-aware iteration rather than fabricated optimization.

It is a practical example of system design that blends AI workflows with product-oriented evaluation logic.

