"""Report generator — HTML and Markdown evaluation reports.

Generates evaluation reports with:
    - Metric summaries with confidence intervals
    - Comparison tables (baseline vs candidate)
    - Judge reliability summary
    - Statistical test results

Implementation planned for M7.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class ReportFormat(str, Enum):
    """Supported report output formats."""

    HTML = "html"
    MARKDOWN = "markdown"


@dataclass
class ReportConfig:
    """Configuration for report generation."""

    format: ReportFormat = ReportFormat.HTML
    output_dir: Path = Path("reports")
    template_dir: Path = Path("evalgate/report/templates")
    include_judge_reliability: bool = True
    include_noise_analysis: bool = True


class ReportGenerator:
    """Generates evaluation reports.

    Implementation planned for M7.
    """

    def __init__(self, config: ReportConfig | None = None) -> None:
        self.config = config or ReportConfig()

    def generate(self, run_dir: Path) -> Path:
        """Generate a report from a completed evaluation run.

        TODO: Implement in M7.
        """
        raise NotImplementedError("Report generator implementation planned for M7.")
