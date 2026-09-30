"""FactForge Review 2 LangGraph orchestration workflow definition.

Builds and compiles the claim-level orchestration graph using LangGraph StateGraph,
implementing state transitions, conditional routing, and retry bounds.
"""

from langgraph.graph import END, START, StateGraph

from orchestration.router import route_claim
from orchestration.state import ClaimState, OrchestratorState, transition_state


def research_step(state: OrchestratorState) -> OrchestratorState:
    """Research node handler in the orchestration graph."""
    return transition_state(state, ClaimState.RESEARCHING, reason="Executing claim research")


def verify_step(state: OrchestratorState) -> OrchestratorState:
    """Verification node handler in the orchestration graph."""
    transition_state(state, ClaimState.VERIFYING, reason="Verifying claim evidence")
    if state.verification_status is None and state.flag is None:
        state.verification_status = "supported"
    return state


def detect_step(state: OrchestratorState) -> OrchestratorState:
    """Detection node handler in the orchestration graph."""
    return transition_state(state, ClaimState.DETECTING, reason="Running anomaly/contradiction detection")


def retry_step(state: OrchestratorState) -> OrchestratorState:
    """Retry node handler in the orchestration graph."""
    if state.retry_count < 2:
        state.retry_count += 1
    reason = state.retry_reason or "Retrying claim pipeline"
    return transition_state(state, ClaimState.RETRY, reason=reason)


def resolve_step(state: OrchestratorState) -> OrchestratorState:
    """Resolution node handler in the orchestration graph."""
    return transition_state(state, ClaimState.RESOLVED, reason="Claim verified and resolved")


def unresolve_step(state: OrchestratorState) -> OrchestratorState:
    """Unresolved node handler in the orchestration graph."""
    return transition_state(state, ClaimState.UNRESOLVED, reason="Claim unresolved after maximum retries")


def create_orchestration_graph():
    """Build and compile the FactForge Review 2 orchestration graph.

    Returns:
        Compiled StateGraph instance.
    """
    workflow = StateGraph(OrchestratorState)

    # Add nodes
    workflow.add_node("research", research_step)
    workflow.add_node("verify", verify_step)
    workflow.add_node("detect", detect_step)
    workflow.add_node("retry", retry_step)
    workflow.add_node("resolve", resolve_step)
    workflow.add_node("unresolve", unresolve_step)

    # Add edges
    workflow.add_edge(START, "research")
    workflow.add_edge("research", "verify")
    workflow.add_edge("verify", "detect")

    # Add conditional routing after detection
    workflow.add_conditional_edges(
        "detect",
        route_claim,
        {
            "resolved": "resolve",
            "retry": "retry",
            "unresolved": "unresolve",
        },
    )

    # Add retry loop edge
    workflow.add_edge("retry", "research")

    # Terminal edges
    workflow.add_edge("resolve", END)
    workflow.add_edge("unresolve", END)

    return workflow.compile()
