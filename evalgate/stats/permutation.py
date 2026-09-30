"""Paired permutation test for comparing two conditions.

Used to determine if the difference between baseline and candidate
metric scores is statistically significant or within noise.

This is custom code (PRD requirement) — must be tested against known cases.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


@dataclass
class PermutationTestResult:
    """Result of a paired permutation test."""

    observed_diff: float
    p_value: float
    n_permutations: int
    significant: bool
    threshold: float


def paired_permutation_test(
    baseline_scores: NDArray[np.floating],
    candidate_scores: NDArray[np.floating],
    n_permutations: int = 10_000,
    threshold: float = 0.05,
    seed: int = 42,
    alternative: str = "two-sided",
) -> PermutationTestResult:
    """Paired permutation test for the difference in means.

    Tests H0: the mean of baseline_scores equals the mean of candidate_scores.
    Pairs are maintained (same eval item, different condition).

    Args:
        baseline_scores: Per-item scores under baseline condition.
        candidate_scores: Per-item scores under candidate condition.
        n_permutations: Number of random permutations.
        threshold: Significance threshold (alpha).
        seed: Random seed for reproducibility.
        alternative: 'two-sided', 'greater', or 'less'.

    Returns:
        PermutationTestResult with observed diff, p-value, and significance.

    Raises:
        ValueError: If arrays have different lengths.
    """
    if len(baseline_scores) != len(candidate_scores):
        msg = (
            f"Paired test requires equal-length arrays. "
            f"Got {len(baseline_scores)} and {len(candidate_scores)}."
        )
        raise ValueError(msg)

    rng = np.random.default_rng(seed)
    n = len(baseline_scores)

    # Observed difference in means (candidate - baseline)
    differences = candidate_scores - baseline_scores
    observed_diff = float(np.mean(differences))

    # Permutation: randomly flip signs of differences
    perm_diffs = np.empty(n_permutations)
    for i in range(n_permutations):
        signs = rng.choice([-1, 1], size=n)
        perm_diffs[i] = np.mean(differences * signs)

    # Compute p-value based on alternative hypothesis
    if alternative == "two-sided":
        p_value = float(np.mean(np.abs(perm_diffs) >= np.abs(observed_diff)))
    elif alternative == "greater":
        p_value = float(np.mean(perm_diffs >= observed_diff))
    elif alternative == "less":
        p_value = float(np.mean(perm_diffs <= observed_diff))
    else:
        msg = f"Unknown alternative: {alternative}. Use 'two-sided', 'greater', or 'less'."
        raise ValueError(msg)

    return PermutationTestResult(
        observed_diff=observed_diff,
        p_value=p_value,
        n_permutations=n_permutations,
        significant=p_value < threshold,
        threshold=threshold,
    )
