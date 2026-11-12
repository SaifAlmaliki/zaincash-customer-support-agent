import pytest

from app.config import Settings
from app.intake.errors import ModelUnavailable
from app.intake.graph import IntakeGraph
from app.models_config.types import ModelChoice
from tests.intake.helpers import context, message


async def test_graph_budget_uses_the_pinned_choice_and_timeout(tax):
    seen = []
    choice = ModelChoice("ollama", "gemma3:4b")

    def choice_for(session_id):
        seen.append(session_id)
        return choice, 150.0

    graph = IntakeGraph(object(), tax, None, Settings(_env_file=None), choice_for=choice_for)
    turn = context([message("hello", language="en")])
    budget = await graph._budget(turn)
    assert budget.choice == choice and 149 < budget.remaining_s() <= 150
    assert seen == [turn.session_id]


async def test_pin_failure_is_reported_as_model_unavailable(tax):
    def broken(session_id):
        raise RuntimeError("database down")

    graph = IntakeGraph(object(), tax, None, Settings(_env_file=None), choice_for=broken)
    with pytest.raises(ModelUnavailable):
        await graph._budget(context([message("hello", language="en")]))


async def test_without_pinning_the_budget_uses_settings(tax):
    graph = IntakeGraph(object(), tax, None, Settings(_env_file=None, intake_timeout_s=42))
    budget = await graph._budget(context([message("hi", language="en")]))
    assert budget.choice is None and budget.remaining_s() <= 42
