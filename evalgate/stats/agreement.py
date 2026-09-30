"""Agreement metrics: Cohen's kappa with bootstrap CI.

Used to measure LLM judge reliability against human labels (M4).

This is custom code (PRD requirement) — must be tested against known cases.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


@dataclass
class AgreementResult:
    """Result of an agreement analysis."""

    kappa: float
    observed_agreement: float
    expected_agreement: float
    ci_lower: float
    ci_upper: float
    confidence_level: float
    n_items: int
    confusion_matrix: NDArray[np.int_]


def cohens_kappa(
    rater_a: NDArray[np.int_],
    rater_b: NDArray[np.int_],
) -> float:
    """Compute Cohen's kappa for two binary raters.

    Args:
        rater_a: Binary array of rater A judgments (0 or 1).
        rater_b: Binary array of rater B judgments (0 or 1).

    Returns:
        Cohen's kappa coefficient.

    Raises:
        ValueError: If arrays have different lengths.
    """
    if len(rater_a) != len(rater_b):
        msg = f"Raters must have same length. Got {len(rater_a)} and {len(rater_b)}."
        raise ValueError(msg)

    n = len(rater_a)

    # Observed agreement
    p_o = np.mean(rater_a == rater_b)

    # Expected agreement by chance
    p_a1 = np.mean(rater_a)
    p_b1 = np.mean(rater_b)
    p_e = p_a1 * p_b1 + (1 - p_a1) * (1 - p_b1)

    if p_e == 1.0:
        return 1.0  # Perfect agreement by chance — kappa undefined, return 1.0

    kappa = (p_o - p_e) / (1 - p_e)
    return float(kappa)


def confusion_matrix_binary(
    rater_a: NDArray[np.int_],
    rater_b: NDArray[np.int_],
) -> NDArray[np.int_]:
    """Compute 2x2 confusion matrix for two binary raters.

    Returns:
        2x2 array: [[TN, FP], [FN, TP]] where rater_a is ground truth.
    """
    tn = int(np.sum((rater_a == 0) & (rater_b == 0)))
    fp = int(np.sum((rater_a == 0) & (rater_b == 1)))
    fn = int(np.sum((rater_a == 1) & (rater_b == 0)))
    tp = int(np.sum((rater_a == 1) & (rater_b == 1)))
    return np.array([[tn, fp], [fn, tp]])


def agreement_with_ci(
    rater_a: NDArray[np.int_],
    rater_b: NDArray[np.int_],
    n_resamples: int = 10_000,
    confidence_level: float = 0.95,
    seed: int = 42,
) -> AgreementResult:
    """Compute Cohen's kappa with bootstrap confidence interval.

    Args:
        rater_a: Binary array — human labels (ground truth).
        rater_b: Binary array — judge labels.
        n_resamples: Number of bootstrap resamples.
        confidence_level: Confidence level for the CI.
        seed: Random seed.

    Returns:
        AgreementResult with kappa, CI, and confusion matrix.
    """
    rng = np.random.default_rng(seed)
    n = len(rater_a)

    # Point estimates
    kappa = cohens_kappa(rater_a, rater_b)
    p_o = float(np.mean(rater_a == rater_b))
    p_a1 = float(np.mean(rater_a))
    p_b1 = float(np.mean(rater_b))
    p_e = p_a1 * p_b1 + (1 - p_a1) * (1 - p_b1)
    cm = confusion_matrix_binary(rater_a, rater_b)

    # Bootstrap CI on kappa
    boot_kappas = np.empty(n_resamples)
    for i in range(n_resamples):
        idx = rng.integers(0, n, size=n)
        boot_kappas[i] = cohens_kappa(rater_a[idx], rater_b[idx])

    alpha = 1 - confidence_level
    ci_lower = float(np.percentile(boot_kappas, 100 * alpha / 2))
    ci_upper = float(np.percentile(boot_kappas, 100 * (1 - alpha / 2)))

    return AgreementResult(
        kappa=kappa,
        observed_agreement=p_o,
        expected_agreement=p_e,
        ci_lower=ci_lower,
        ci_upper=ci_upper,
        confidence_level=confidence_level,
        n_items=n,
        confusion_matrix=cm,
    )
