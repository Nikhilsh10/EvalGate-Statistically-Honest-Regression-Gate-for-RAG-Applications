# ADR-001: Corpus Selection

**Status:** Proposed
**Date:** 2026-09-30
**Deciders:** Nikhil Sharma

## Context

The PRD requires a public corpus with a licence that permits redistribution for the eval set. We need a question-answering dataset that is representative of RAG use cases: questions that require retrieving relevant passages from a knowledge base.

## Decision

**Primary corpus: Stanford Question Answering Dataset (SQuAD) 2.0**

- **Licence:** CC BY-SA 4.0 — permits redistribution with attribution and share-alike. (Source: https://rajpurkar.github.io/SQuAD-explorer/)
- **Source:** https://rajpurkar.github.io/SQuAD-explorer/
- **Why SQuAD:**
  - Well-established QA benchmark with passage-grounded answers.
  - Contains ~150k question-answer pairs with source paragraphs — sufficient for our 150-item eval set.
  - Answers are span-based (extractable from passages), which aligns with RAG retrieval evaluation.
  - Includes unanswerable questions (SQuAD 2.0), useful for testing faithfulness and abstention.

**Supplementary corpus (if needed): Natural Questions (NQ) Open**
- **Licence:** CC BY-SA 3.0
- **Source:** https://ai.google.com/research/NaturalQuestions
- **Why:** Real Google search questions; more representative of production RAG usage.

## Eval Set Construction Plan

1. Sample ~200 question-passage-answer triples from SQuAD 2.0.
2. Index the source passages into the target RAG app's FAISS index.
3. Human-label at least 100 items (Nikhil): correctness of answer, which chunk supports it.
4. Split: ~50 dev items (for building/debugging) + ~150 held-out (for final experiments at M6).
5. Store as versioned JSONL in `data/eval_v1/`.

## Consequences

- SQuAD passages are Wikipedia-based, which is different from domain-specific RAG apps. State this limitation.
- We commit the eval set directly (CC BY-SA allows redistribution), but must include attribution.
- If the RAG app is tuned for a different domain, SQuAD may not reflect real performance. This is a known limitation — we are testing the eval *framework*, not optimising the RAG app.

## Attribution

SQuAD 2.0: Pranav Rajpurkar, Robin Jia, and Percy Liang. "Know What You Don't Know: Unanswerable Questions for SQuAD." ACL 2018.
Licensed under CC BY-SA 4.0.
