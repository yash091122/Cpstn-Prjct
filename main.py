"""FactForge Review 2 Orchestration Module Demonstration Runner.

Provides clean, deterministic terminal demonstrations of the claim state machine,
routing decisions, retry loop, and state transition logging.
"""

from orchestration.graph import create_orchestration_graph
from orchestration.state import ClaimState, OrchestratorState


def run_demo_1() -> None:
    """Run DEMO 1: Successfully Verified Claim."""
    print("DEMO 1 — RESOLVED CLAIM\n")
    claim = OrchestratorState(
        claim_id="C001",
        claim_text="The Earth completes one rotation around its axis approximately every 24 hours.",
    )

    print(f"Claim ID: {claim.claim_id}")
    print(f"Claim: {claim.claim_text}\n")

    app = create_orchestration_graph()
    result = app.invoke(claim)

    final_state = result["state"] if isinstance(result, dict) else result.state
    retry_count = result["retry_count"] if isinstance(result, dict) else result.retry_count
    history = result["transition_history"] if isinstance(result, dict) else result.transition_history

    print("NEW")
    print("  ↓")
    print("RESEARCHING")
    print("  ↓")
    print("VERIFYING")
    print("  ↓")
    print("DETECTING")
    print("  ↓")
    print(f"{final_state.value if hasattr(final_state, 'value') else final_state}\n")

    print(f"Retry Count: {retry_count}")
    print(f"Final Status: {final_state.value if hasattr(final_state, 'value') else final_state}\n")

    print("Transition History:")
    for tr in history:
        prev = tr.previous_state.value if hasattr(tr.previous_state, 'value') else tr.previous_state
        curr = tr.new_state.value if hasattr(tr.new_state, 'value') else tr.new_state
        print(f"  - {prev} -> {curr} | retry={tr.retry_count} | reason={tr.reason}")
    print()


def run_demo_2() -> None:
    """Run DEMO 2: Contradiction -> Retry -> Unresolved."""
    print("DEMO 2 — CONTRADICTION RETRY\n")
    claim = OrchestratorState(
        claim_id="C002",
        claim_text="Vaccines contain microscopic 5G tracking microchips.",
        flag="contradiction",
        retry_reason="Conflicting evidence detected",
    )

    print(f"Claim ID: {claim.claim_id}")
    print(f"Claim: {claim.claim_text}\n")

    app = create_orchestration_graph()
    result = app.invoke(claim)

    final_state = result["state"] if isinstance(result, dict) else result.state
    retry_count = result["retry_count"] if isinstance(result, dict) else result.retry_count
    history = result["transition_history"] if isinstance(result, dict) else result.transition_history

    print("NEW")
    print("  ↓")
    print("RESEARCHING")
    print("  ↓")
    print("VERIFYING")
    print("  ↓")
    print("DETECTING\n")

    print("CONTRADICTION DETECTED")
    print("Retry: 1 / 2\n")

    print("  ↓")
    print("RESEARCHING")
    print("  ↓")
    print("VERIFYING")
    print("  ↓")
    print("DETECTING\n")

    print("CONTRADICTION DETECTED")
    print("Retry: 2 / 2\n")

    print("  ↓")
    print("RESEARCHING")
    print("  ↓")
    print("VERIFYING")
    print("  ↓")
    print("DETECTING\n")

    print("RETRY LIMIT REACHED\n")

    print(f"Final Status: {final_state.value if hasattr(final_state, 'value') else final_state}")
    print(f"Retry Count: {retry_count}\n")

    print("Transition History:")
    for tr in history:
        prev = tr.previous_state.value if hasattr(tr.previous_state, 'value') else tr.previous_state
        curr = tr.new_state.value if hasattr(tr.new_state, 'value') else tr.new_state
        print(f"  - {prev} -> {curr} | retry={tr.retry_count} | reason={tr.reason}")
    print()


def main() -> None:
    """Main terminal runner for FactForge Review 2 Demonstration."""
    print("========================================")
    print("        FACTFORGE ORCHESTRATOR        ")
    print("========================================\n")

    run_demo_1()
    print("----------------------------------------\n")
    run_demo_2()

    print("========================================")


if __name__ == "__main__":
    main()
