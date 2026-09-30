# ADR-002: Judge Model Selection

**Status:** Accepted
**Date:** 2026-09-30
**Deciders:** Nikhil Sharma

## Context

EvalGate needs an LLM judge to score generation quality (correctness, faithfulness). The PRD mandates zero API cost (Ollama, fully local). We need to choose a model that:

1. Runs locally via Ollama on consumer hardware.
2. Has reasonable instruction-following for structured evaluation prompts.
3. Is fast enough for 150+ evaluations.

## Decision

**Primary judge: Llama 3.1 8B (via Ollama)**

- **Model ID:** `llama3.1:8b`
- **Why:**
  - Instruction-tuned, good at following structured prompts.
  - 8B parameters — runs comfortably on machines with 16GB+ RAM.
  - Widely used for LLM-as-judge tasks in the community.
  - Fast inference on consumer hardware (typically 20-40 tokens/sec).

**Fallback / comparison: Mistral 7B v0.3**
- **Model ID:** `mistral:7b`
- **Why:** Alternative architecture for cross-model judge validation (M4).

## Judge Configuration

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Temperature | 0.0 | Deterministic for reproducibility |
| Top-p | 1.0 | No nucleus sampling — full greedy |
| Seed | 42 (fixed per run) | Reproducibility across runs |
| Max tokens | 512 | Sufficient for structured verdicts |

## Consequences

- **Local models are noisier than GPT-4/Claude.** This is expected and a feature of the project: we measure the noise (M4) and report it honestly.
- **Judge reliability must be validated** against human labels (M4). If kappa is low, that is a valid result — report it.
- **Temperature 0.0 with fixed seed** reduces run-to-run variance but does not eliminate it (Ollama implementation details may vary). The noise measurement (M5) accounts for this.
- Hardware requirements: 16GB+ RAM for 8B model. Document this.

## Alternatives Considered

| Model | Rejected because |
|-------|-----------------|
| GPT-4 / Claude API | Non-zero cost, external dependency, can't redistribute |
| Llama 3.1 70B | Too large for consumer hardware |
| Phi-3 Mini 3.8B | Too small, weaker instruction following |
