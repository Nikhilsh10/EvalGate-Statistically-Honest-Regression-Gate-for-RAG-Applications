"""Placeholder test — verifies the project skeleton is functional.

This test exists to satisfy M0 acceptance: `make test` passes.
Real tests will be added alongside each milestone's implementation.
"""

import numpy as np

from evalgate import __version__
from evalgate.metrics.retrieval import hit_at_k, mean_reciprocal_rank
from evalgate.metrics.generation import judge_correctness
from evalgate.stats.bootstrap import bootstrap_ci
from evalgate.stats.permutation import paired_permutation_test
from evalgate.stats.agreement import cohens_kappa, confusion_matrix_binary


class TestVersion:
    """Test that the package version is set."""

    def test_version_exists(self) -> None:
        assert __version__ is not None
        assert isinstance(__version__, str)
        assert __version__ == "0.1.0"


class TestRetrievalMetrics:
    """Test retrieval metrics against known cases."""

    def test_hit_at_k_hit(self) -> None:
        """Relevant chunk is in top-k."""
        retrieved = ["a", "b", "c", "d", "e"]
        relevant = ["c"]
        assert hit_at_k(retrieved, relevant, k=5) == 1.0

    def test_hit_at_k_miss(self) -> None:
        """Relevant chunk is NOT in top-k."""
        retrieved = ["a", "b", "c", "d", "e"]
        relevant = ["f"]
        assert hit_at_k(retrieved, relevant, k=5) == 0.0

    def test_hit_at_k_partial(self) -> None:
        """Relevant chunk is outside the k window."""
        retrieved = ["a", "b", "c", "d", "e"]
        relevant = ["e"]
        assert hit_at_k(retrieved, relevant, k=3) == 0.0  # e is at position 5

    def test_mrr_first_position(self) -> None:
        """Relevant chunk is at position 1."""
        retrieved = ["a", "b", "c"]
        relevant = ["a"]
        assert mean_reciprocal_rank(retrieved, relevant) == 1.0

    def test_mrr_third_position(self) -> None:
        """Relevant chunk is at position 3."""
        retrieved = ["a", "b", "c"]
        relevant = ["c"]
        assert mean_reciprocal_rank(retrieved, relevant) == 1 / 3

    def test_mrr_no_hit(self) -> None:
        """No relevant chunk found."""
        retrieved = ["a", "b", "c"]
        relevant = ["z"]
        assert mean_reciprocal_rank(retrieved, relevant) == 0.0


class TestGenerationMetrics:
    """Test generation metrics against known cases."""

    def test_judge_correctness_agree(self) -> None:
        assert judge_correctness(True, True) == 1.0
        assert judge_correctness(False, False) == 1.0

    def test_judge_correctness_disagree(self) -> None:
        assert judge_correctness(True, False) == 0.0
        assert judge_correctness(False, True) == 0.0


class TestBootstrap:
    """Test bootstrap CI against known cases."""

    def test_bootstrap_ci_known_mean(self) -> None:
        """Bootstrap CI of a constant array should be tight around the value."""
        data = np.array([5.0] * 100)
        result = bootstrap_ci(data, statistic=np.mean, n_resamples=1000, seed=42)
        assert result.estimate == 5.0
        assert result.ci_lower == 5.0
        assert result.ci_upper == 5.0
        assert result.standard_error == 0.0

    def test_bootstrap_ci_covers_true_mean(self) -> None:
        """95% CI from a normal distribution should cover the true mean (most of the time)."""
        rng = np.random.default_rng(42)
        data = rng.normal(loc=10.0, scale=2.0, size=200)
        result = bootstrap_ci(data, statistic=np.mean, n_resamples=5000, seed=42)
        assert result.ci_lower < 10.0 < result.ci_upper

    def test_bootstrap_ci_confidence_level(self) -> None:
        """Metadata should match what we requested."""
        data = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        result = bootstrap_ci(data, confidence_level=0.90, seed=42)
        assert result.confidence_level == 0.90


class TestPermutationTest:
    """Test permutation test against known cases."""

    def test_identical_distributions(self) -> None:
        """Same data should not be significant."""
        scores = np.array([0.5, 0.6, 0.7, 0.8, 0.9])
        result = paired_permutation_test(scores, scores, n_permutations=1000, seed=42)
        assert result.observed_diff == 0.0
        assert result.p_value >= 0.05
        assert result.significant is False

    def test_clearly_different(self) -> None:
        """Very different distributions should be significant."""
        baseline = np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
        candidate = np.array([0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9])
        result = paired_permutation_test(baseline, candidate, n_permutations=5000, seed=42)
        assert result.observed_diff > 0
        assert result.p_value < 0.05
        assert result.significant is True

    def test_mismatched_lengths_raises(self) -> None:
        """Different length arrays should raise ValueError."""
        import pytest
        with pytest.raises(ValueError, match="equal-length"):
            paired_permutation_test(np.array([1.0, 2.0]), np.array([1.0]))


class TestAgreement:
    """Test Cohen's kappa against known cases."""

    def test_perfect_agreement(self) -> None:
        """Perfect agreement should give kappa = 1.0."""
        rater_a = np.array([1, 1, 0, 0, 1, 0])
        rater_b = np.array([1, 1, 0, 0, 1, 0])
        assert cohens_kappa(rater_a, rater_b) == 1.0

    def test_no_agreement(self) -> None:
        """Complete disagreement should give negative kappa."""
        rater_a = np.array([1, 1, 1, 0, 0, 0])
        rater_b = np.array([0, 0, 0, 1, 1, 1])
        kappa = cohens_kappa(rater_a, rater_b)
        assert kappa < 0

    def test_confusion_matrix(self) -> None:
        """Verify confusion matrix computation."""
        rater_a = np.array([1, 1, 0, 0])
        rater_b = np.array([1, 0, 1, 0])
        cm = confusion_matrix_binary(rater_a, rater_b)
        # [[TN, FP], [FN, TP]]
        assert cm[0, 0] == 1  # TN
        assert cm[0, 1] == 1  # FP
        assert cm[1, 0] == 1  # FN
        assert cm[1, 1] == 1  # TP

    def test_mismatched_lengths_raises(self) -> None:
        """Different length arrays should raise ValueError."""
        import pytest
        with pytest.raises(ValueError, match="same length"):
            cohens_kappa(np.array([1, 0]), np.array([1]))
