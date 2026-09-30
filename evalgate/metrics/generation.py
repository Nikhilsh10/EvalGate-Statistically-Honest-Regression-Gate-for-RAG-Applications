"""Generation metrics: Answer correctness and faithfulness.

Uses ragas where suitable (answer_correctness, faithfulness).
Custom judge correctness metric for judge validation (M4).

Implementation planned for M3.
"""

from __future__ import annotations


def judge_correctness(
    judge_verdict: bool,
    human_label: bool,
) -> float:
    """Binary agreement: does the judge verdict match the human label?

    Used for judge validation (M4) — not a generation quality metric itself.

    Args:
        judge_verdict: Whether the judge says the answer is correct.
        human_label: Whether the human labeller says the answer is correct.

    Returns:
        1.0 if they agree, 0.0 if they disagree.
    """
    return 1.0 if judge_verdict == human_label else 0.0
