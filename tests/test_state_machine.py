"""Unit tests for the claim state model in FactForge Review 2."""

import logging
import pytest
from pydantic import ValidationError
from orchestration.state import (
    ClaimState,
    OrchestratorState,
    TransitionRecord,
    transition_state,
)


def test_default_state_is_new():
    """Verify that default state is ClaimState.NEW."""
    state = OrchestratorState(claim_id="C001", claim_text="The earth revolves around the sun.")
    assert state.state == ClaimState.NEW


def test_retry_count_starts_at_zero():
    """Verify that retry_count starts at 0 by default."""
    state = OrchestratorState(claim_id="C001", claim_text="The earth revolves around the sun.")
    assert state.retry_count == 0


def test_retry_count_cannot_be_negative():
    """Verify that setting retry_count < 0 raises a ValidationError."""
    with pytest.raises(ValidationError):
        OrchestratorState(
            claim_id="C001",
            claim_text="The earth revolves around the sun.",
            retry_count=-1,
        )


def test_retry_count_cannot_exceed_two():
    """Verify that setting retry_count > 2 raises a ValidationError."""
    with pytest.raises(ValidationError):
        OrchestratorState(
            claim_id="C001",
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
        claim_id="C001",
        claim_text="The earth revolves around the sun.",
        transition_history=[rec1, rec2, rec3],
    )

    assert len(state.transition_history) == 3
    assert state.transition_history[0].previous_state == ClaimState.NEW
    assert state.transition_history[1].new_state == ClaimState.VERIFYING
    assert state.transition_history[2].new_state == ClaimState.RESOLVED


def test_transition_state_changes_state_correctly():
    """Verify that transition_state correctly changes the current state."""
    state = OrchestratorState(claim_id="C001", claim_text="Sample claim text")
    assert state.state == ClaimState.NEW

    updated_state = transition_state(state, ClaimState.RESEARCHING, reason="initial research")
    assert updated_state.state == ClaimState.RESEARCHING


def test_transition_state_records_previous_new_and_increases_history():
    """Verify that transition_state appends record with previous and new states."""
    state = OrchestratorState(claim_id="C001", claim_text="Sample claim text")
    initial_len = len(state.transition_history)

    transition_state(state, ClaimState.RESEARCHING, reason="initial research")

    assert len(state.transition_history) == initial_len + 1
    last_record = state.transition_history[-1]
    assert last_record.previous_state == ClaimState.NEW
    assert last_record.new_state == ClaimState.RESEARCHING


def test_transition_state_preserves_retry_count():
    """Verify that transition_state preserves the existing retry_count."""
    state = OrchestratorState(claim_id="C002", claim_text="Sample claim", retry_count=1)
    transition_state(state, ClaimState.RETRY, reason="contradiction detected")

    assert state.retry_count == 1
    assert state.transition_history[-1].retry_count == 1


def test_transition_state_stores_reason():
    """Verify that transition_state stores the transition reason."""
    state = OrchestratorState(claim_id="C001", claim_text="Sample claim text")
    transition_state(state, ClaimState.VERIFYING, reason="starting verification")

    assert state.transition_history[-1].reason == "starting verification"


def test_transition_state_logging_without_crashing(caplog):
    """Verify that transition_state logs the transition formatted correctly without crashing."""
    state = OrchestratorState(claim_id="C001", claim_text="Sample claim text", retry_count=0)
    with caplog.at_level(logging.INFO):
        transition_state(state, ClaimState.RESEARCHING, reason="initial research")

    assert "C001" in caplog.text
    assert "NEW -> RESEARCHING" in caplog.text
    assert "retry=0" in caplog.text
    assert "reason=initial research" in caplog.text
