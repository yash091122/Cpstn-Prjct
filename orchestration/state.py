"""Claim state model for FactForge Review 2.

Defines the state enumeration, transition recording model, main orchestrator
state structure, and state transition handling with logging.
"""

from datetime import datetime
from enum import Enum
import logging
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

logger = logging.getLogger(__name__)


class ClaimState(str, Enum):
    """Enumeration of valid states in the claim state machine."""
    NEW = "NEW"
    RESEARCHING = "RESEARCHING"
    VERIFYING = "VERIFYING"
    DETECTING = "DETECTING"
    RETRY = "RETRY"
    RESOLVED = "RESOLVED"
    UNRESOLVED = "UNRESOLVED"
    SYNTHESIZED = "SYNTHESIZED"


class TransitionRecord(BaseModel):
    """Record of a state transition event."""
    previous_state: ClaimState
    new_state: ClaimState
    timestamp: datetime = Field(default_factory=datetime.now)
    reason: Optional[str] = None
    retry_count: int = 0


class OrchestratorState(BaseModel):
    """Claim-level orchestration state model for FactForge."""
    claim_id: str
    claim_text: str
    state: ClaimState = ClaimState.NEW
    verification_status: Optional[str] = None
    flag: Optional[str] = None
    retry_count: int = Field(default=0, ge=0, le=2)
    retry_reason: Optional[str] = None
    transition_history: List[TransitionRecord] = Field(default_factory=list)

    @field_validator("retry_count")
    @classmethod
    def validate_retry_count(cls, v: int) -> int:
        """Validate that retry_count is within [0, 2]."""
        if v < 0:
            raise ValueError("retry_count cannot be negative.")
        if v > 2:
            raise ValueError("retry_count cannot exceed 2.")
        return v


def transition_state(
    state: OrchestratorState,
    new_state: ClaimState,
    reason: str = ""
) -> OrchestratorState:
    """Transition an OrchestratorState to a new ClaimState and log the transition.

    Args:
        state: Current claim state object.
        new_state: Target ClaimState to transition into.
        reason: Description or justification for the transition.

    Returns:
        The updated OrchestratorState object.
    """
    previous_state = state.state
    record = TransitionRecord(
        previous_state=previous_state,
        new_state=new_state,
        timestamp=datetime.now(),
        reason=reason,
        retry_count=state.retry_count,
    )
    state.state = new_state
    state.transition_history.append(record)

    logger.info(
        "[%s] %s -> %s | retry=%d | reason=%s",
        state.claim_id,
        previous_state.value if isinstance(previous_state, Enum) else previous_state,
        new_state.value if isinstance(new_state, Enum) else new_state,
        state.retry_count,
        reason,
    )
    return state
