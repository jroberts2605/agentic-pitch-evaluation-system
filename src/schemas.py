from typing import Literal

from pydantic import BaseModel


class PitchClassification(BaseModel):
    """Structured output returned by the pitch classification agent."""

    pitch_type: Literal["consumer", "b2b_saas", "deep_tech"]
    reasoning: str


class PitchEvaluation(BaseModel):
    """Structured output returned by the pitch evaluation agent."""

    passes: bool
    per_criterion_feedback: list[str]
    summary: str