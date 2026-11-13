from app.intake.answers import quick_answer
from tests.intake.helpers import context, message


def test_quick_reply_keeps_the_requested_details():
    turn = context([message("اي")], category="failed_transfer")
    turn.state.additional_needed = ["recipient_name", "exact_error"]
    analysis = quick_answer(turn, "debited", "yes")
    assert analysis.additional_needed == ["recipient_name", "exact_error"]
    assert analysis.updates[0].key == "debited"
