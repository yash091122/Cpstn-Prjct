"""Unit tests for the claim state model in FactForge Review 2."""

import pytest
from pydantic import ValidationError
from orchestration.state import ClaimState, OrchestratorState, TransitionRecord


def test_default_state_is_new():
    """Verify that default state is ClaimState.NEW."""
    state = OrchestratorState(claim_id="claim-101", claim_text="The earth revolves around the sun.")
    assert state.state == ClaimState.NEW


def test_retry_count_starts_at_zero():
    """Verify that retry_count starts at 0 by default."""
    state = OrchestratorState(claim_id="claim-101", claim_text="The earth revolves around the sun.")
    assert state.retry_count == 0


def test_retry_count_cannot_be_negative():
    """Verify that setting retry_count < 0 raises a ValidationError."""
    with pytest.raises(ValidationError):
        OrchestratorState(
            claim_id="claim-101",
            claim_text="The earth revolves around the sun.",
            retry_count=-1,
        )


def test_retry_count_cannot_exceed_two():
    """Verify that setting retry_count > 2 raises a ValidationError."""
    with pytest.raises(ValidationError):
        OrchestratorState(
            claim_id="claim-101",
            claim_text="The earth revolves around the sun.",
            retry_count=3,
        )


def test_transition_record_can_be_created():
    """Verify that TransitionRecord can be instantiated correctly."""
    record = TransitionRecord(
        previous_state=ClaimState.NEW,
        new_state=ClaimState.RESEARCHING,
        reason="Beginning research phase",
        retry_count=0,
    )
    assert record.previous_state == ClaimState.NEW
    assert record.new_state == ClaimState.RESEARCHING
    assert record.reason == "Beginning research phase"
    assert record.retry_count == 0
    assert record.timestamp is not None


def test_transition_history_stores_multiple_transitions():
    """Verify that transition_history can store multiple transitions."""
    rec1 = TransitionRecord(
        previous_state=ClaimState.NEW,
        new_state=ClaimState.RESEARCHING,
        reason="Start research",
    )
    rec2 = TransitionRecord(
        previous_state=ClaimState.RESEARCHING,
        new_state=ClaimState.VERIFYING,
        reason="Research finished, starting verification",
    )
    rec3 = TransitionRecord(
        previous_state=ClaimState.VERIFYING,
        new_state=ClaimState.RESOLVED,
        reason="Claim verified successfully",
    )

    state = OrchestratorState(
        claim_id="claim-101",
        claim_text="The earth revolves around the sun.",
        transition_history=[rec1, rec2, rec3],
    )

    assert len(state.transition_history) == 3
    assert state.transition_history[0].previous_state == ClaimState.NEW
    assert state.transition_history[1].new_state == ClaimState.VERIFYING
    assert state.transition_history[2].new_state == ClaimState.RESOLVED
