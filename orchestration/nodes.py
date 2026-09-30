"""Deterministic demo nodes for FactForge Review 2 orchestration module.

Provides mock/demo nodes to simulate Research and Verification module outputs
for testing state transitions and routing independently.
"""

from orchestration.state import ClaimState, OrchestratorState, transition_state


def research_node(state: OrchestratorState) -> OrchestratorState:
    """Simulate research node execution.

    Transitions claim state to RESEARCHING and then to VERIFYING upon completion.

    Args:
        state: Current OrchestratorState.

    Returns:
        Updated OrchestratorState.
    """
    transition_state(state, ClaimState.RESEARCHING, reason="Initial research started")
    transition_state(state, ClaimState.VERIFYING, reason="Research completed")
    return state


def verify_node(state: OrchestratorState) -> OrchestratorState:
    """Simulate successful verification node execution.

    Transitions state to VERIFYING, sets status to supported, clears flags,
    and transitions to DETECTING.

    Args:
        state: Current OrchestratorState.

    Returns:
        Updated OrchestratorState.
    """
    transition_state(state, ClaimState.VERIFYING, reason="Verification started")
    state.verification_status = "supported"
    state.flag = None
    transition_state(state, ClaimState.DETECTING, reason="Claim verified as supported")
    return state


def contradiction_demo_node(state: OrchestratorState) -> OrchestratorState:
    """Simulate verification output with a contradiction flag for retry demo.

    Transitions state to DETECTING, sets status to unsupported, sets flag to contradiction,
    and records retry reason.

    Args:
        state: Current OrchestratorState.

    Returns:
        Updated OrchestratorState.
    """
    transition_state(state, ClaimState.DETECTING, reason="Contradiction detection started")
    state.verification_status = "unsupported"
    state.flag = "contradiction"
    state.retry_reason = "Conflicting evidence detected"
    return state


def retry_node(state: OrchestratorState) -> OrchestratorState:
    """Handle retry node logic.

    Increments retry_count by 1 (max 2), transitions to RESEARCHING, and preserves
    the existing retry_reason.

    Args:
        state: Current OrchestratorState.

    Returns:
        Updated OrchestratorState.
    """
    if state.retry_count < 2:
        state.retry_count += 1

    reason = state.retry_reason or "Retrying claim research"
    transition_state(state, ClaimState.RESEARCHING, reason=reason)
    return state
