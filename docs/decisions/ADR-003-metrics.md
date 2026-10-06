# ADR-003: Metrics Selection

**Status:** Proposed
**Date:** 2026-09-30
**Deciders:** Nikhil Sharma

## Context

EvalGate evaluates a RAG application at two levels: retrieval quality and generation quality. The PRD says to "use ragas where it fits; add what it doesn't do (significance testing, judge validation, CI gating)."

## Decision

### Retrieval Metrics (Custom Implementation)

These are computed deterministically against labelled source chunks — no LLM judge needed.

| Metric | Definition | Why |
|--------|-----------|-----|
| **Hit@k** | 1 if any of the top-k retrieved chunks contains the labelled source chunk, else 0 | Binary relevance — simple, interpretable |
| **MRR** (Mean Reciprocal Rank) | 1/rank of the first relevant chunk in retrieved list, averaged over queries | Rewards systems that rank relevant chunks higher |

### Generation Metrics (ragas + Custom)

| Metric | Source | Definition | Why |
|--------|--------|-----------|-----|
| **Answer Correctness** | ragas (`answer_correctness`) | LLM judge comparison of generated answer vs reference answer | Standard generation quality metric |
| **Faithfulness** | ragas (`faithfulness`) | Proportion of claims in the answer that are supported by retrieved contexts | Detects hallucination |
| **Judge Correctness** | Custom | Binary: judge agrees with human label (correct/incorrect) | Needed for judge validation (M4) |

### Statistical Methods (Custom Implementation — PRD requirement)

| Method | Purpose |
|--------|---------|
| **Bootstrap CI** (BCa, 10,000 resamples) | Confidence intervals on all metrics |
| **Paired Bootstrap Test** | Compare candidate vs baseline metric distributions |
| **Paired Permutation Test** | Non-parametric significance test for A/B comparison |
| **Cohen's Kappa** | Judge-vs-human agreement (M4) |
| **Bootstrap CI on Kappa** | Uncertainty on judge reliability estimate |

## Consequences

- **ragas dependency:** We use ragas for answer_correctness and faithfulness, but do not fork it. We cite it properly. ragas requires an LLM for these metrics — uses the judge model from ADR-002. (Source: https://docs.ragas.io/en/stable/)
- **Custom stats code:** Bootstrap, permutation, and kappa code must be tested against known cases (e.g., bootstrap CI of a known normal distribution). This is the core differentiator.
- **Deterministic seeds:** All stochastic methods use fixed seeds, recorded per run.
- **10,000 resamples** is standard but may be slow for full eval sets. Profile at M3 and reduce if necessary (document the trade-off).

## Alternatives Considered

| Alternative | Rejected because |
|-------------|-----------------|
| NDCG | Requires graded relevance labels; binary is sufficient for this eval set |
| BERTScore | Adds model dependency for generation eval; ragas covers this |
| ROUGE/BLEU | Poor correlation with human judgments for open-ended QA |
| Wilcoxon signed-rank | Valid alternative to permutation test, but permutation test is distribution-free and more intuitive to explain |
