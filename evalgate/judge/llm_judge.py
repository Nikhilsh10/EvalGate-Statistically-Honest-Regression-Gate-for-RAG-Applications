"""LLM Judge — Calls Ollama to score generation quality.

Uses a local LLM (Llama 3.1 8B via Ollama) for:
    - Answer correctness scoring
    - Faithfulness assessment

Configuration per ADR-002:
    - Temperature: 0.0 (deterministic)
    - Seed: 42 (fixed per run)
    - Max tokens: 512

Implementation planned for M3.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class JudgeVerdict(str, Enum):
    """Possible judge verdicts."""

    CORRECT = "correct"
    INCORRECT = "incorrect"
    PARTIALLY_CORRECT = "partially_correct"
    ABSTAIN = "abstain"


@dataclass
class JudgeConfig:
    """Configuration for the LLM judge."""

    model: str = "llama3.1:8b"
    base_url: str = "http://localhost:11434"
    temperature: float = 0.0
    top_p: float = 1.0
    seed: int = 42
    max_tokens: int = 512


@dataclass
class JudgeResult:
    """Result from a single judge evaluation."""

    verdict: JudgeVerdict
    score: float  # 0.0 to 1.0
    reasoning: str = ""
    raw_response: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


class LLMJudge:
    """LLM-as-judge for evaluating RAG generation quality.

    Implementation planned for M3.
    """

    def __init__(self, config: JudgeConfig | None = None) -> None:
        self.config = config or JudgeConfig()

    async def judge_correctness(
        self,
        question: str,
        generated_answer: str,
        reference_answer: str,
    ) -> JudgeResult:
        """Judge whether the generated answer is correct.

        TODO: Implement in M3.
        """
        raise NotImplementedError("Judge implementation planned for M3.")

    async def judge_faithfulness(
        self,
        question: str,
        generated_answer: str,
        retrieved_contexts: list[str],
    ) -> JudgeResult:
        """Judge whether the generated answer is faithful to retrieved contexts.

        TODO: Implement in M3.
        """
        raise NotImplementedError("Judge implementation planned for M3.")
