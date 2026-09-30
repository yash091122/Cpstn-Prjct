"""Unit tests for demo nodes and retry mechanism in FactForge Review 2."""

from orchestration.nodes import (
    contradiction_demo_node,
    research_node,
    retry_node,
    verify_node,
)
from orchestration.state import ClaimState, OrchestratorState


def test_research_node_behavior():
    """Verify research_node transitions to RESEARCHING and then VERIFYING."""
    state = OrchestratorState(claim_id="C001", claim_text="Water boils at 100C.")
    updated_state = research_node(state)

    assert updated_state.state == ClaimState.VERIFYING
    assert len(updated_state.transition_history) == 2
    assert updated_state.transition_history[0].new_state == ClaimState.RESEARCHING
    assert updated_state.transition_history[1].new_state == ClaimState.VERIFYING


def test_verify_node_behavior():
    """Verify verify_node sets supported status, clears flag, and transitions to DETECTING."""
    state = OrchestratorState(claim_id="C002", claim_text="Water boils at 100C.")
    updated_state = verify_node(state)

    assert updated_state.state == ClaimState.DETECTING
    assert updated_state.verification_status == "supported"
    assert updated_state.flag is None


def test_contradiction_demo_node_behavior():
    """Verify contradiction_demo_node sets unsupported status, contradiction flag, and retry reason."""
    state = OrchestratorState(claim_id="C003", claim_text="The moon is made of cheese.")
    updated_state = contradiction_demo_node(state)

    assert updated_state.state == ClaimState.DETECTING
    assert updated_state.verification_status == "unsupported"
    assert updated_state.flag == "contradiction"
    assert updated_state.retry_reason == "Conflicting evidence detected"


def test_retry_node_increments_count_and_transitions_to_researching():
    """Verify retry_node increments retry_count by 1, transitions to RESEARCHING, and preserves retry_reason."""
    state = OrchestratorState(
        claim_id="C004",
        claim_text="The moon is made of cheese.",
        retry_count=0,
        retry_reason="Conflicting evidence detected",
    )
    updated_state = retry_node(state)

    assert updated_state.retry_count == 1
    assert updated_state.state == ClaimState.RESEARCHING
    assert updated_state.retry_reason == "Conflicting evidence detected"


def test_retry_node_retry_count_limit_does_not_exceed_two():
    """Verify retry_node increments up to 2 and does not exceed 2."""
    state = OrchestratorState(
        claim_id="C005",
        claim_text="The moon is made of cheese.",
        retry_count=1,
        retry_reason="Conflicting evidence detected",
    )
    # First retry (count 1 -> 2)
    state = retry_node(state)
    assert state.retry_count == 2
    assert state.state == ClaimState.RESEARCHING

    # Second retry attempt when already at max 2
    state = retry_node(state)
    assert state.retry_count == 2
    assert state.state == ClaimState.RESEARCHING
