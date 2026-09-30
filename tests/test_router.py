"""Unit tests for the claim routing logic in FactForge Review 2."""

from orchestration.router import route_claim
from orchestration.state import ClaimState, OrchestratorState


def test_supported_claim_routes_to_resolved():
    """Verify that verification_status == 'supported' routes to 'resolved'."""
    state = OrchestratorState(
        claim_id="claim-1",
        claim_text="The earth orbits the sun.",
        verification_status="supported",
    )
    assert route_claim(state) == "resolved"


def test_contradiction_retry_0_routes_to_retry():
    """Verify contradiction flag with retry_count=0 routes to 'retry'."""
    state = OrchestratorState(
        claim_id="claim-2",
        claim_text="The sun orbits the earth.",
        flag="contradiction",
        retry_count=0,
    )
    assert route_claim(state) == "retry"


def test_contradiction_retry_1_routes_to_retry():
    """Verify contradiction flag with retry_count=1 routes to 'retry'."""
    state = OrchestratorState(
        claim_id="claim-3",
        claim_text="The sun orbits the earth.",
        flag="contradiction",
        retry_count=1,
    )
    assert route_claim(state) == "retry"


def test_contradiction_retry_2_routes_to_unresolved():
    """Verify contradiction flag with retry_count=2 routes to 'unresolved'."""
    state = OrchestratorState(
        claim_id="claim-4",
        claim_text="The sun orbits the earth.",
        flag="contradiction",
        retry_count=2,
    )
    assert route_claim(state) == "unresolved"


def test_hallucination_retry_0_routes_to_retry():
    """Verify hallucination flag with retry_count=0 routes to 'retry'."""
    state = OrchestratorState(
        claim_id="claim-5",
        claim_text="Unsubstantiated quantum statement.",
        flag="hallucination",
        retry_count=0,
    )
    assert route_claim(state) == "retry"


def test_hallucination_retry_1_routes_to_retry():
    """Verify hallucination flag with retry_count=1 routes to 'retry'."""
    state = OrchestratorState(
        claim_id="claim-6",
        claim_text="Unsubstantiated quantum statement.",
        flag="hallucination",
        retry_count=1,
    )
    assert route_claim(state) == "retry"


def test_hallucination_retry_2_routes_to_unresolved():
    """Verify hallucination flag with retry_count=2 routes to 'unresolved'."""
    state = OrchestratorState(
        claim_id="claim-7",
        claim_text="Unsubstantiated quantum statement.",
        flag="hallucination",
        retry_count=2,
    )
    assert route_claim(state) == "unresolved"


def test_no_flag_acceptable_status_routes_to_resolved():
    """Verify claim with no problem flag routes to 'resolved'."""
    state = OrchestratorState(
        claim_id="claim-8",
        claim_text="Water freezes at 0 degrees Celsius.",
        flag=None,
    )
    assert route_claim(state) == "resolved"
