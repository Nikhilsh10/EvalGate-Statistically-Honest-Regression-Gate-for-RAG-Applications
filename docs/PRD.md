# PRD: EvalGate — Statistically Honest Regression Gate for RAG Applications

**Owner:** Nikhil · **Target roles:** ML/AI Engineer (primary), Backend Engineer · **Timebox:** 3–4 weeks part-time
**Status:** Draft v1 · **Audience:** Nikhil and Claude Code

---

## 0. How to use this with Claude Code

1. Save as `docs/PRD.md` in a new repo `evalgate`. Copy Section 11 into `CLAUDE.md`.
2. One milestone at a time. Plan mode first, restate acceptance criteria, then build.
3. A milestone is done only when its verification commands were run and raw output saved to `docs/evidence/Mx.txt`.
4. No number enters the README, blog post, or resume unless it exists in `docs/evidence/`.

---

## 1. Problem

Teams change prompts, chunk sizes, embedding models, and retrievers, then ship based on a handful of eyeballed answers or a single score from an LLM judge. Two failures follow:

1. **Noise mistaken for signal.** A 2-point score change on 50 examples is often within run-to-run noise.
2. **Unvalidated judges.** LLM-as-judge scores are treated as ground truth without checking agreement with humans.

EvalGate is a CLI, GitHub Action, and small service that evaluates a RAG app against a versioned eval set, reports metrics **with confidence intervals**, **measures how much the LLM judge can be trusted** against a human-labelled subset, and **fails a PR only when a regression is statistically supported**.

## 2. Why this project (differentiators)

- Eval and reliability engineering is a hiring priority for AI teams, and few freshers show it.
- It builds directly on existing strengths: an evaluation-library contribution, calibration and reliability work, MLOps, and FastAPI.
- The value is rigor (CIs, significance tests, judge validation), not another chatbot.

## 3. Non-goals

- Not a new RAG framework. Target app is your existing RAG-QA-System (fully local via Ollama, zero API cost).
- Not a reimplementation of ragas metrics. Use ragas where it fits; add what it doesn't do (significance testing, judge validation, CI gating).
- No claims of generality beyond what you tested.

## 4. Success criteria (all measured, none assumed)

| # | Criterion | Evidence |
|---|-----------|----------|
| S1 | Eval set v1 with at least 150 items, of which at least 100 are human-labelled by you | `data/eval_v1/` + labelling log |
| S2 | Judge agreement with human labels reported with Cohen's kappa and a bootstrap CI | `docs/evidence/M4.txt` |
| S3 | Gate catches an injected regression (e.g. top-k reduced, chunk size broken) and passes a no-op change | CI runs for both |
| S4 | Run-to-run noise measured (same config repeated at least 5 times) and used to set the gate threshold | `docs/evidence/noise.txt` |
| S5 | At least 4 real configuration experiments compared with paired tests | results table in README |
| S6 | Fresh clone to first eval report in under 20 minutes by README alone | timed run |
| S7 | CI passes: lint, unit tests, a small fixed-fixture eval | Actions run |

## 5. Architecture

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

## 6. Stack

| Layer | Choice | Note |
|-------|--------|------|
| Language / packaging | Python, `pyproject.toml`, Typer CLI | |
| Target app | Existing RAG-QA-System (FastAPI, FAISS, Ollama) | Pin its commit hash per experiment |
| Metrics | ragas (where suitable), custom retrieval metrics | Cite ragas; do not fork it |
| Stats | numpy/scipy, own bootstrap and permutation code with tests | |
| Tracking | MLflow | |
| Service (optional M7) | FastAPI + SQLite | Serves run history |
| CI | GitHub Actions | Use recorded model outputs (fixtures) for CI; full local-model runs are local/nightly |
| Packaging | Docker | |

Pin all versions at M0.

## 7. Data policy

- Pick a public corpus with a licence that permits redistribution; verify the licence at M0 and record it in `docs/decisions/ADR-001.md`. If unsure, commit only scripts that download it.
- Questions: draft with an LLM if you like, but **every item in the human-labelled subset is reviewed and labelled by you**, including whether the answer is correct and which chunk supports it. Synthetic-only eval sets are a known bias; state this limitation.
- Split the set: dev items for building, held-out items never touched until final experiments.

## 8. Milestones

### M0 — Skeleton and decisions (day 1–2)
Repo layout, pyproject, Makefile, CI with lint and a placeholder test, ADR for corpus, judge model, and metrics.
**Verify:** CI green; `make test` output.

### M1 — Traceable target app (day 3–5)
Add a tracing endpoint or wrapper to the RAG app that returns retrieved chunk IDs, scores, answer, latency, and token counts. Pin target app version.
**Acceptance:** one question returns a full trace with stable chunk IDs.
**Verify:** `curl` transcript.

### M2 — Eval set v1 (day 5–9)
JSONL schema, versioning, labelling tool (a small CLI or spreadsheet import), dev/held-out split.
**Acceptance:** S1.
**Verify:** counts per split and label distribution saved to evidence.

### M3 — Metric runners (day 10–13)
Retrieval metrics, judge-based correctness, faithfulness. Deterministic seeds; judge temperature fixed and recorded.
**Acceptance:** one full eval run produces per-item scores and an aggregate.
**Verify:** run output plus MLflow run.

### M4 — Judge reliability (day 13–16)
Compare judge verdicts to your human labels on the labelled subset: agreement, Cohen's kappa, bootstrap CI, confusion matrix. Test at least one known bias (e.g. answer length or position) with a controlled perturbation.
**Acceptance:** S2. Report plainly if the judge is unreliable. That is a valid and useful result.
**Verify:** `docs/evidence/M4.txt`.

### M5 — Noise and gate (day 16–20)
Repeat the baseline at least 5 times to measure noise (S4). Implement paired bootstrap/permutation test, threshold config, exit codes, Markdown PR comment, GitHub Action.
**Acceptance:** S3, S7.
**Verify:** two CI runs, one pass (no-op change) and one fail (injected regression).

### M6 — Experiments (day 20–25)
At least 4 changes (e.g. chunk size, embedding model, top-k, reranker), each evaluated on the held-out set against baseline with CIs and paired tests. Include at least one change where the result is **not significant** and say so.
**Acceptance:** S5.
**Verify:** results table generated by script, raw outputs saved.

### M7 — Report, docs, demo (day 25–28)
HTML report, README with architecture and honest limitations, demo GIF, short write-up (blog or README section) explaining the judge-reliability and noise findings. Optional FastAPI history service.
**Acceptance:** S6.
**Verify:** timed fresh-clone run.

## 9. Repository layout

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
│   └── fixtures/       # recorded traces for CI
├── action/             # GitHub Action definition
└── .github/workflows/
```

Never commit `.env`. Add a secret-scanning pre-commit hook.

## 10. Risks

| Risk | Mitigation |
|------|-----------|
| Small local judge is noisy | That is the finding. Measure it (M4) and report it |
| CI cannot run Ollama fast enough | CI uses recorded fixtures; full runs local |
| Labelling 100+ items is tedious | Budget the time now: about 2–3 days. Do not skip it, it is the credibility core |
| Tiny eval set gives wide CIs | Report the CIs anyway and state the minimum detectable effect |
| Scope creep into dashboards or new metrics | Nothing beyond M7 until all criteria are met |
| Building instead of applying | Keep applying and outreach running in parallel; do not pause the job search for this |

## 11. Content for `CLAUDE.md`

See `CLAUDE.md` in repo root.

## 12. Resume bullet templates (fill only from `docs/evidence/`)

- Built EvalGate, a CI regression gate for RAG applications that reports metrics with bootstrap confidence intervals and fails PRs only on statistically supported regressions (paired test, **[N]**-item held-out set).
- Validated an LLM judge against **[N]** human-labelled items (Cohen's kappa **[X]**, 95% CI **[a–b]**); identified **[bias finding]** and set gate thresholds from measured run-to-run noise (**[N]** repeats).
- Evaluated **[N]** RAG configuration changes; **[k]** produced significant improvements and **[m]** did not, avoiding **[describe]** unsupported changes.

Delete any bullet whose placeholders cannot be filled from real measurements.
