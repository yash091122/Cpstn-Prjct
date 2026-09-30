"""Conditional claim router for FactForge Review 2 orchestration module.

Provides routing decision logic for claims based on verification status,
problem flags (contradiction, hallucination), and retry limits.
"""

from orchestration.state import OrchestratorState

MAX_RETRIES = 2


def route_claim(state: OrchestratorState) -> str:
    """Determine the next routing decision for a claim state.

    Args:
        state: The current OrchestratorState.

    Returns:
        Routing decision string: 'resolved', 'retry', or 'unresolved'.
    """
    # Rule 1: Verification status is "supported"
    if state.verification_status == "supported":
        return "resolved"

    # Rule 2: Problem flag is "contradiction"
    if state.flag == "contradiction":
        if state.retry_count < MAX_RETRIES:
            return "retry"
        return "unresolved"

    # Rule 3: Problem flag is "hallucination"
    if state.flag == "hallucination":
        if state.retry_count < MAX_RETRIES:
            return "retry"
        return "unresolved"

    # Rule 4: Claim has no problem flag and acceptable verification status
    return "resolved"
