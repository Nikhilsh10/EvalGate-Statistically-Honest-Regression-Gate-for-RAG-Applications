"""Bootstrap confidence intervals.

Implements BCa (bias-corrected and accelerated) bootstrap for confidence intervals
on arbitrary scalar statistics.

This is custom code (PRD requirement) — must be tested against known cases.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


@dataclass
class BootstrapResult:
    """Result of a bootstrap confidence interval computation."""

    estimate: float
    ci_lower: float
    ci_upper: float
    confidence_level: float
    n_resamples: int
    standard_error: float


def bootstrap_ci(
    data: NDArray[np.floating],
    statistic: callable = np.mean,
    n_resamples: int = 10_000,
    confidence_level: float = 0.95,
    seed: int = 42,
    method: str = "percentile",
) -> BootstrapResult:
    """Compute a bootstrap confidence interval for a scalar statistic.

    Args:
        data: 1-D array of observations.
        statistic: Function that computes a scalar from a 1-D array.
        n_resamples: Number of bootstrap resamples.
        confidence_level: Confidence level (e.g. 0.95 for 95% CI).
        seed: Random seed for reproducibility.
        method: 'percentile' or 'bca'. BCa is more accurate but slower.

    Returns:
        BootstrapResult with point estimate, CI bounds, and metadata.
    """
    rng = np.random.default_rng(seed)
    n = len(data)
    point_estimate = float(statistic(data))

    # Generate bootstrap resamples
    boot_indices = rng.integers(0, n, size=(n_resamples, n))
    boot_statistics = np.array([statistic(data[idx]) for idx in boot_indices])

    standard_error = float(np.std(boot_statistics, ddof=1))

    if method == "percentile":
        alpha = 1 - confidence_level
        ci_lower = float(np.percentile(boot_statistics, 100 * alpha / 2))
        ci_upper = float(np.percentile(boot_statistics, 100 * (1 - alpha / 2)))
    elif method == "bca":
        ci_lower, ci_upper = _bca_interval(
            data, boot_statistics, statistic, confidence_level, point_estimate
        )
    else:
        msg = f"Unknown method: {method}. Use 'percentile' or 'bca'."
        raise ValueError(msg)

    return BootstrapResult(
        estimate=point_estimate,
        ci_lower=ci_lower,
        ci_upper=ci_upper,
        confidence_level=confidence_level,
        n_resamples=n_resamples,
        standard_error=standard_error,
    )


def _bca_interval(
    data: NDArray[np.floating],
    boot_statistics: NDArray[np.floating],
    statistic: callable,
    confidence_level: float,
    point_estimate: float,
) -> tuple[float, float]:
    """Compute BCa (bias-corrected and accelerated) confidence interval.

    Args:
        data: Original data array.
        boot_statistics: Array of bootstrap statistic values.
        statistic: The statistic function.
        confidence_level: Desired confidence level.
        point_estimate: Point estimate of the statistic.

    Returns:
        Tuple of (lower, upper) CI bounds.
    """
    from scipy import stats as sp_stats

    n = len(data)
    alpha = 1 - confidence_level

    # Bias correction factor
    z0 = sp_stats.norm.ppf(np.mean(boot_statistics < point_estimate))

    # Acceleration factor (jackknife)
    jackknife_estimates = np.array([statistic(np.delete(data, i)) for i in range(n)])
    jack_mean = np.mean(jackknife_estimates)
    numerator = np.sum((jack_mean - jackknife_estimates) ** 3)
    denominator = 6.0 * (np.sum((jack_mean - jackknife_estimates) ** 2) ** 1.5)
    acc = numerator / denominator if denominator != 0 else 0.0

    # Adjusted percentiles
    z_alpha_lower = sp_stats.norm.ppf(alpha / 2)
    z_alpha_upper = sp_stats.norm.ppf(1 - alpha / 2)

    alpha1 = sp_stats.norm.cdf(z0 + (z0 + z_alpha_lower) / (1 - acc * (z0 + z_alpha_lower)))
    alpha2 = sp_stats.norm.cdf(z0 + (z0 + z_alpha_upper) / (1 - acc * (z0 + z_alpha_upper)))

    ci_lower = float(np.percentile(boot_statistics, 100 * alpha1))
    ci_upper = float(np.percentile(boot_statistics, 100 * alpha2))

    return ci_lower, ci_upper
