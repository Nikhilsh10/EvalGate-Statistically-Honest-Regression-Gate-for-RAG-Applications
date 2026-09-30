# EvalGate — Statistically Honest Regression Gate for RAG Applications

> A CLI, GitHub Action, and small service that evaluates a RAG app against a versioned eval set, reports metrics **with confidence intervals**, **measures LLM judge reliability** against human labels, and **fails a PR only when a regression is statistically supported**.

## Status

🚧 **M0 — Skeleton and Decisions** (in progress)

## Problem

Teams change prompts, chunk sizes, embedding models, and retrievers, then ship based on eyeballed answers or a single LLM judge score. Two failures follow:

1. **Noise mistaken for signal.** A 2-point score change on 50 examples is often within run-to-run noise.
2. **Unvalidated judges.** LLM-as-judge scores are treated as ground truth without checking agreement with humans.

## What EvalGate Does

- Evaluates a RAG app against a **versioned eval set** with human-labelled items
- Reports retrieval metrics (hit@k, MRR) and generation metrics (correctness, faithfulness) **with bootstrap confidence intervals**
- Measures **LLM judge reliability** via Cohen's kappa against human labels
- Runs **paired permutation/bootstrap tests** to detect real regressions vs noise
- Provides a **CI gate** that fails PRs only on statistically supported regressions

## Architecture

```
eval set (versioned JSONL, human labels on subset)
        │
        ▼
 runner ── calls target RAG app (HTTP) ──► traces: question, retrieved contexts, answer, latency, tokens
        │
        ▼
 metrics
   retrieval:  hit@k, MRR (against labelled source chunks)
   generation: judge correctness, faithfulness (ragas where suitable)
        │
        ▼
 statistics
   bootstrap CIs · paired permutation/bootstrap test vs baseline · judge-vs-human agreement (kappa)
        │
        ├─► MLflow (experiment tracking)
        ├─► report (HTML/Markdown artifact)
        └─► gate: exit code + PR comment via GitHub Action
```

## Quick Start

```bash
# Install
pip install -e ".[dev]"

# Run tests
make test

# Run linting
make lint
```

## Stack

| Layer | Choice |
|-------|--------|
| Language / packaging | Python, `pyproject.toml`, Typer CLI |
| Target app | RAG-QA-System (FastAPI, FAISS, Ollama) |
| Metrics | ragas (where suitable), custom retrieval metrics |
| Stats | numpy/scipy, custom bootstrap and permutation code |
| Tracking | MLflow |
| CI | GitHub Actions |
| Packaging | Docker |

## Repository Layout

```
evalgate/
├── CLAUDE.md
├── README.md
├── pyproject.toml
├── Makefile
├── docs/
│   ├── PRD.md
│   ├── decisions/
│   └── evidence/
├── evalgate/
│   ├── cli.py
│   ├── runner.py
│   ├── metrics/
│   ├── stats/
│   ├── judge/
│   └── report/
├── data/
│   └── eval_v1/
├── tests/
│   ├── unit/
│   └── fixtures/
├── action/
└── .github/workflows/
```

## Commands

| Command | Description |
|---------|-------------|
| `make test` | Run unit tests |
| `make lint` | Run linting |
| `make eval` | Run full evaluation |
| `make noise` | Measure run-to-run noise |
| `make gate` | Run regression gate |
| `make report` | Generate report |

## Limitations

- **Status:** Early development — only the project skeleton exists at M0.
- **Eval set:** Not yet created. Human labelling required (M2).
- **No generality claims:** Will only be tested against one RAG application.
- **Local models only:** Uses Ollama (zero API cost), which may be noisier than larger commercial models. This is a feature — we measure the noise.

## License

MIT
