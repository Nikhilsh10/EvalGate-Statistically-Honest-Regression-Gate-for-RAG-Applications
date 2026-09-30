"""EvalGate Runner — Calls target RAG app and collects traces.

Responsibilities:
    - Send questions from the eval set to the target RAG app via HTTP.
    - Collect traces: question, retrieved contexts (with chunk IDs), answer, latency, token counts.
    - Store traces as structured JSONL for downstream metric computation.

Implementation planned for M1.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Trace:
    """A single evaluation trace from the target RAG app."""

    question_id: str
    question: str
    retrieved_chunks: list[dict[str, Any]] = field(default_factory=list)
    answer: str = ""
    latency_ms: float = 0.0
    token_count: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class RunConfig:
    """Configuration for an evaluation run."""

    target_url: str = "http://localhost:8000"
    target_endpoint: str = "/query"
    timeout_seconds: float = 30.0
    max_retries: int = 3
    seed: int = 42


class EvalRunner:
    """Runs evaluation queries against the target RAG app.

    Implementation planned for M1.
    """

    def __init__(self, config: RunConfig) -> None:
        self.config = config
        self.traces: list[Trace] = []

    async def run_single(self, question_id: str, question: str) -> Trace:
        """Run a single question against the target app and return a trace.

        TODO: Implement in M1.
        """
        raise NotImplementedError("Runner implementation planned for M1.")

    async def run_eval_set(self, eval_set_path: str) -> list[Trace]:
        """Run the full eval set and return all traces.

        TODO: Implement in M1.
        """
        raise NotImplementedError("Runner implementation planned for M1.")
