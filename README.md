# Agentic AI Pitch Evaluation System

A multi-agent AI system that classifies startup pitches, routes them to specialized coaching agents, evaluates them against dynamically retrieved rubrics, and iteratively improves them through an evaluator-optimizer loop.

The system supports three startup categories—Consumer, B2B SaaS, and Deep Tech—with category-specific coaching and evaluation criteria. An MCP server provides the appropriate rubric at runtime, while structured Pydantic outputs enforce consistent classification and evaluation results.

Rather than optimizing pitches by inventing missing information, the system identifies unsupported claims and surfaces missing evidence for the user to provide.

## Architecture

The pipeline combines routing, specialized agents, MCP-based tool use, and an evaluator-optimizer feedback loop.

```text
                        ┌─────────────────┐
                        │  Startup Pitch  │
                        └────────┬────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │   Classifier    │
                        └────────┬────────┘
                                 │
                  ┌──────────────┼──────────────┐
                  ▼              ▼              ▼
             Consumer        B2B SaaS       Deep Tech
               Coach           Coach           Coach
                  └──────────────┼──────────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │    Evaluator    │◄──── MCP Rubric Server
                        └────────┬────────┘
                                 │
                           Pass? │
                          ┌──────┴──────┐
                         Yes            No
                          │              │
                          ▼              ▼
                    Final Pitch     Optimizer
                                         │
                                         └──────► Evaluator
```

The classifier determines the pitch category and routes it to the appropriate domain-specific coach. The evaluator retrieves the corresponding rubric from an MCP server rather than relying on hard-coded evaluation criteria. If the draft fails any criterion, the optimizer revises it using the evaluator's feedback and returns it for another evaluation, up to a fixed iteration limit.

## How It Works

1. **Classify** — The classifier analyzes the startup pitch and assigns it to Consumer, B2B SaaS, or Deep Tech using a structured Pydantic output.
2. **Route** — The pitch is sent to a category-specific coaching agent that rewrites the draft around the priorities of that startup type.
3. **Retrieve Rubric** — The evaluator calls an MCP server to retrieve the appropriate three-criterion evaluation rubric at runtime.
4. **Evaluate** — The evaluator scores the revised pitch against each criterion and returns structured feedback.
5. **Optimize** — If the pitch does not pass, the optimizer uses the evaluator's feedback to revise the draft before another evaluation.
6. **Stop** — The process ends when the pitch passes or reaches the three-iteration limit.

## Technologies

- **Python 3.12** — Core application and pipeline logic
- **OpenAI Agents SDK** — Agent orchestration, routing, and model execution
- **Model Context Protocol (MCP)** — Runtime retrieval of pitch-specific evaluation rubrics
- **Pydantic** — Structured outputs for classification and evaluation
- **AsyncIO** — Asynchronous pipeline execution

## Project Structure

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
└── requirements.txt
```

## Example Results

The pipeline was evaluated using synthetic startup pitches representing each supported category.

| Pitch | Category | Iterations | Result |
| --- | --- | ---: | --- |
| SnackPocket | Consumer | 1 | Passed |
| ShiftRoster | B2B SaaS | 3 | Did not pass — missing traction evidence |
| KitchenSense | Deep Tech | 3 | Did not pass — missing first-customer evidence |

The unsuccessful cases demonstrate an intentional constraint of the system: the optimizer can improve a pitch using available information, but it does not fabricate unsupported business evidence simply to satisfy the rubric.

Detailed classification reasoning, final pitches, and criterion-level evaluator feedback are available in `examples/sample_results.md`.

## Setup

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

### 4. Configure the API key

Copy `.env.example` to `.env` and replace the placeholder with your OpenAI API key.

```text
OPENAI_API_KEY=your_api_key_here
```

Do not commit `.env` or expose API credentials in source code.

### 5. Run the demo

```bash
python examples/run_demo.py
```

The demo processes the three example pitches through the classification, coaching, evaluation, and optimization pipeline.

## Design Decisions

**Dynamic rubric retrieval:** Evaluation criteria are served through an MCP server instead of being embedded directly in the evaluator prompt. This separates evaluation policy from agent behavior and allows rubrics to be updated independently.

**Structured outputs:** Pydantic models constrain classification and evaluation responses to predictable schemas, making agent outputs easier to route and use programmatically.

**Specialized routing:** Rather than using one general-purpose coaching agent, the classifier routes pitches to category-specific coaches with different priorities for Consumer, B2B SaaS, and Deep Tech startups.

**Bounded optimization:** The evaluator-optimizer loop is capped at three iterations to prevent runaway execution. The optimizer is also instructed not to fabricate missing evidence, allowing the pipeline to surface information gaps when further rewriting cannot resolve them.

