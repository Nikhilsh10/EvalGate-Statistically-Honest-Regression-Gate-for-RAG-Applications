# EvalGate — Statistically Honest Regression Gate for RAG Applications

> A CLI and GitHub Action that evaluates a RAG app against a versioned eval set, reports metrics **with confidence intervals**, **measures LLM judge reliability** against human labels, and **fails a PR only when a regression is statistically supported**.

## Status

🚧 **M0 — Skeleton and Decisions** (in progress)

CI: [![CI](https://github.com/Nikhilsh10/EvalGate-Statistically-Honest-Regression-Gate-for-RAG-Applications/actions/workflows/ci.yml/badge.svg)](https://github.com/Nikhilsh10/EvalGate-Statistically-Honest-Regression-Gate-for-RAG-Applications/actions/workflows/ci.yml)

## Problem

Teams change prompts, chunk sizes, embedding models, and retrievers, then ship based on eyeballed answers or a single LLM judge score. Two failures follow:

1. **Noise mistaken for signal.** A 2-point score change on 50 examples is often within run-to-run noise.
2. **Unvalidated judges.** LLM-as-judge scores are treated as ground truth without checking agreement with humans.

## What EvalGate Will Do

- Evaluate a RAG app against a **versioned eval set** with human-labelled items
- Report retrieval metrics (hit@k, MRR) and generation metrics **with bootstrap confidence intervals**
- Measure **LLM judge reliability** via Cohen's kappa against human labels
- Run **paired permutation/bootstrap tests** to detect real regressions vs noise
- Provide a **CI gate** that fails PRs only on statistically supported regressions

None of the above is implemented yet. See the milestone plan in `docs/PRD.md`.

## Quick Start

```bash
# Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
make test

# Run linting
make lint
```

## What Exists at M0

```
evalgate/
├── CLAUDE.md               # Agent rules
├── README.md               # This file
├── pyproject.toml          # Package metadata and dev deps
├── requirements.lock       # Tool-generated lockfile (pip freeze in clean venv)
├── .python-version         # Python 3.12
├── LICENSE                 # MIT
├── Makefile                # make test | make lint
├── docs/
│   ├── PRD.md              # Product Requirements Document
│   ├── decisions/          # ADRs: corpus, judge model, metrics
│   └── evidence/           # Empty until M0 CI is green
├── evalgate/
│   ├── __init__.py         # version = "0.1.0"
│   ├── cli.py              # Typer CLI skeleton (version + --help work)
│   ├── metrics/
│   │   ├── retrieval.py    # hit_at_k, mean_reciprocal_rank (implemented)
│   │   └── generation.py   # judge_correctness helper (implemented)
│   └── stats/
│       ├── bootstrap.py    # bootstrap_ci (implemented, tested)
│       ├── permutation.py  # paired_permutation_test (implemented, tested)
│       └── agreement.py    # cohens_kappa, confusion_matrix (implemented, tested)
├── tests/
│   └── unit/               # 19 tests, all passing
└── .github/workflows/
    └── ci.yml              # lint + smoke test + pytest on ubuntu-24.04 / Python 3.12
```

Future milestone files (runner, judge, report, data, action) are **not present** — they will be added at the milestone that implements them.

## Stack

| Layer | Choice | Note |
|-------|--------|------|
| Language / packaging | Python 3.12, `pyproject.toml`, Typer CLI | |
| Target app | RAG-QA-System (FastAPI, FAISS, Ollama) | Pinned at M1 |
| Metrics | ragas (where suitable), custom retrieval metrics | Added at M3 |
| Stats | numpy/scipy, custom bootstrap and permutation code | M0 skeleton present |
| Tracking | MLflow | Added at M3 |
| CI | GitHub Actions | `ubuntu-24.04`, Python 3.12 |

## Available Commands

| Command | Available | Description |
|---------|-----------|-------------|
| `make test` | ✅ M0 | Run unit tests |
| `make lint` | ✅ M0 | Run ruff check + format check |
| `make eval` | M3 | Run full evaluation |
| `make noise` | M5 | Measure run-to-run noise |
| `make gate` | M5 | Run regression gate |
| `make report` | M7 | Generate report |

## Limitations

- **Status:** M0 skeleton only. No evaluation runs have been performed.
- **Eval set:** Not created yet. Human labelling required (M2).
- **Statistics:** Bootstrap CI and permutation test code is implemented and unit-tested against known cases, but has not yet been run on real RAG data.
- **No generality claims:** Will only be tested against one RAG application.
- **Local models only:** Uses Ollama (zero API cost), which may be noisier than commercial models. Measuring this noise is the point of M4–M5.
- **Gate sensitivity:** The minimum detectable effect depends on eval set size and measured noise. This will be computed from real noise data at M5 before the gate threshold is set.

All numbers in this README come from `docs/evidence/`. Until that directory contains files, no performance claims are made.

## License

MIT — see [LICENSE](LICENSE).
