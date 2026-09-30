"""Retrieval metrics: Hit@k and MRR.

These are computed deterministically against labelled source chunks.
No LLM judge needed.

Implementation planned for M3.
"""

from __future__ import annotations


def hit_at_k(
    retrieved_chunk_ids: list[str],
    relevant_chunk_ids: list[str],
    k: int = 5,
) -> float:
    """Compute Hit@k: 1 if any of top-k retrieved chunks is relevant, else 0.

    Args:
        retrieved_chunk_ids: Ordered list of retrieved chunk IDs (most relevant first).
        relevant_chunk_ids: List of ground-truth relevant chunk IDs.
        k: Number of top chunks to consider.

    Returns:
        1.0 if hit, 0.0 if miss.
    """
    top_k = set(retrieved_chunk_ids[:k])
    relevant = set(relevant_chunk_ids)
    return 1.0 if top_k & relevant else 0.0


def mean_reciprocal_rank(
    retrieved_chunk_ids: list[str],
    relevant_chunk_ids: list[str],
) -> float:
    """Compute Mean Reciprocal Rank (MRR) for a single query.

    Returns 1/rank of the first relevant chunk, or 0.0 if none found.

    Args:
        retrieved_chunk_ids: Ordered list of retrieved chunk IDs (most relevant first).
        relevant_chunk_ids: List of ground-truth relevant chunk IDs.

    Returns:
        Reciprocal rank (1/rank) or 0.0.
    """
    relevant = set(relevant_chunk_ids)
    for rank, chunk_id in enumerate(retrieved_chunk_ids, start=1):
        if chunk_id in relevant:
            return 1.0 / rank
    return 0.0
