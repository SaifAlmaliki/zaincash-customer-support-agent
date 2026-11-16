from uuid import uuid4

import pytest

from app.config import Settings
from app.intake.contracts import EvidenceRef, Fact, Question, QuestionRecord
from app.intake.policy import (
    answer_choices,
    answer_kind,
    ask_for,
    ask_once_keys,
    assess_readiness,
    choose_question,
    customer_received_money,
    material_keys,
    progress,
)
from app.taxonomy import load_taxonomy
from tests.intake.helpers import context, fact, message


@pytest.fixture
def taxonomy():
    return load_taxonomy(Settings(_env_file=None).taxonomy_path)


def asked(key, times=1):
    return [QuestionRecord(key=key, basis_revision=1, message_id=uuid4(), outcome="asked") for _ in range(times)]


def unknown(key, source):
    return Fact(key=key, status="unknown", evidence=[EvidenceRef(kind="message", source_id=source.id, quote=source.text)])


def complete_transfer(source, *extra):
    return [
        fact("issue", source.text, source),
        fact("amount", "50000", source, normalized="50000"),
        fact("date", "2026-10-06", source, normalized="2026-10-06"),
        fact("debited", "yes", source, normalized="yes"),
        fact("recipient_outcome", "no", source, normalized="no"),
        fact("recipient_phone", "07701234567", source, normalized="07701234567"),
        *extra,
    ]


@pytest.mark.parametrize(("category", "required", "optional"), [
    ("failed_transfer", ["issue", "amount", "date", "debited", "recipient_outcome", "recipient_phone"], ["recipient_name", "txn_ref"]),
    ("wrong_recipient", ["issue", "amount", "date", "recipient_phone"], ["recipient_name", "txn_ref"]),
    ("bill_payment", ["issue", "biller", "amount", "date"], ["txn_ref", "debited"]),
    ("agent_dispute", ["issue", "amount", "agent_location", "date"], ["txn_ref"]),
    ("refund_request", ["issue", "merchant", "amount", "date"], ["txn_ref"]),
    ("app_bug", ["issue", "failed_step", "expected"], ["exact_error", "device", "app_version"]),
    ("login_access", ["issue", "failed_step", "expected"], ["exact_error", "device", "app_version"]),
    ("card_issue", ["issue", "card_symptom", "expected"], ["exact_error"]),
    ("account_kyc", ["issue", "kyc_step", "expected"], ["exact_error"]),
    ("fraud_report", ["issue", "date"], ["amount", "recipient_phone", "txn_ref"]),
    ("general_inquiry", ["issue"], []),
    ("other", ["issue", "desired_outcome"], []),
    ("login", ["issue", "failed_step", "expected"], ["exact_error", "device", "app_version"]),
    ("something_new", ["issue", "desired_outcome"], []),
])
def test_field_plan(taxonomy, category, required, optional):
    assert material_keys(category, taxonomy) == required
    assert ask_once_keys(category) == optional


def test_money_problems_do_not_ask_what_was_expected(taxonomy):
    source = message("حولت فلوس وما وصلت")
    state = context([source], [fact("issue", source.text, source)], category="failed_transfer").state
    question = choose_question(state, None, 1, taxonomy)
    assert question is not None and question.key == "amount"
    readiness = assess_readiness(state, taxonomy)
    assert "expected" not in readiness.missing and "actual" not in readiness.missing


def test_question_carries_reason_kind_choices_and_attempt(taxonomy):
    source = message("حولت 50000 بتاريخ 2026-10-06 وما وصلت")
    known = [
        fact("issue", source.text, source),
        fact("amount", "50000", source, normalized="50000"),
        fact("date", "2026-10-06", source, normalized="2026-10-06"),
    ]
    question = choose_question(context([source], known, category="failed_transfer").state, None, 3, taxonomy)
    assert question.key == "debited"
    assert question.text == "انخصم المبلغ من محفظتك؟"
    assert question.reason == "حتى نعرف إذا الفلوس طلعت من محفظتك."
    assert question.answer_kind == "yes_no"
    assert question.choices == ["yes", "no", "unknown"]
    assert question.attempt == 1
    assert question.basis_revision == 3


@pytest.mark.parametrize(("key", "kind", "choices"), [
    ("debited", "yes_no", ["yes", "no", "unknown"]),
    ("recipient_outcome", "yes_no", ["yes", "no", "unknown"]),
    ("repeats", "yes_no", ["yes", "no", "unknown"]),
    ("amount", "amount", ["unknown"]),
    ("recipient_phone", "phone", ["unknown"]),
    ("txn_ref", "reference", ["unknown", "attach"]),
    ("date", "date", ["unknown"]),
    ("recipient_name", "text", ["unknown"]),
])
def test_answer_kind_comes_from_the_key(key, kind, choices):
    assert answer_kind(key) == kind
    assert answer_choices(key) == choices


def test_required_detail_is_asked_again_once_after_the_first_round(taxonomy):
    source = message("حولت فلوس وما وصلت")
    known = [fact("issue", source.text, source), fact("amount", "50000", source, normalized="50000")]
    state = context([source], known, category="failed_transfer").state
    state = state.model_copy(update={"questions": [*asked("amount"), *asked("date")]})
    first = choose_question(state, None, 4, taxonomy)
    assert first.key == "debited" and first.attempt == 1
    rest = ["debited", "recipient_outcome", "recipient_phone", "recipient_name", "txn_ref"]
    state = state.model_copy(update={"questions": [*state.questions, *[item for key in rest for item in asked(key)]]})
    again = choose_question(state, None, 5, taxonomy)
    assert again.key == "date" and again.attempt == 2
    assert again.text == "بس حتى نكمل التقرير: متى صارت هالمشكلة؟"
    state = state.model_copy(update={"questions": [*state.questions, *asked("date")]})
    after = choose_question(state, None, 6, taxonomy)
    assert after is not None and after.key == "debited" and after.attempt == 2


def test_ask_once_detail_is_never_asked_twice(taxonomy):
    source = message("x")
    state = context([source], complete_transfer(source), category="failed_transfer").state
    state = state.model_copy(update={"questions": [*asked("recipient_name"), *asked("txn_ref")]})
    assert choose_question(state, None, 9, taxonomy) is None
    assert assess_readiness(state, taxonomy).quality == "sufficient_context"


def test_unasked_ask_once_detail_keeps_collecting(taxonomy):
    source = message("x")
    readiness = assess_readiness(context([source], complete_transfer(source), category="failed_transfer").state, taxonomy)
    assert readiness.quality == "collecting"
    assert readiness.missing == []
    assert readiness.next_key == "recipient_name"


def test_unknown_reference_still_gives_a_complete_report(taxonomy):
    source = message("ما عندي رقم")
    facts = complete_transfer(source, fact("recipient_name", "علي حسين", source), unknown("txn_ref", source))
    assert assess_readiness(context([source], facts, category="failed_transfer").state, taxonomy).quality == "sufficient_context"


def test_unknown_required_detail_is_partial(taxonomy):
    source = message("ما أعرف")
    facts = [
        *complete_transfer(source)[:-1], unknown("recipient_phone", source),
        fact("recipient_name", "علي", source), fact("txn_ref", "ZC1", source, normalized="ZC1"),
    ]
    readiness = assess_readiness(context([source], facts, category="failed_transfer").state, taxonomy)
    assert readiness.quality == "partial_context"


def test_customer_chosen_question_ignores_the_ask_limit():
    source = message("x")
    state = context([source], [fact("issue", source.text, source), unknown("txn_ref", source)], category="failed_transfer").state
    state = state.model_copy(update={"questions": asked("txn_ref")})
    question = ask_for(state, "txn_ref", 7)
    assert question.key == "txn_ref" and question.attempt == 2
    assert question.text == "عدك رقم عملية أو مرجع؟"
    assert question.choices == ["unknown", "attach"]


def test_model_suggestion_is_used_within_the_current_round(taxonomy):
    source = message("حولت فلوس وما وصلت")
    state = context([source], [fact("issue", source.text, source)], category="failed_transfer").state
    suggested = Question(key="recipient_phone", text="على أي رقم حولت؟", reason="حتى نلگه التحويل.", basis_revision=0)
    question = choose_question(state, suggested, 2, taxonomy)
    assert question.key == "recipient_phone"
    assert question.text == "على أي رقم حولت؟"
    assert question.reason == "حتى نلگه التحويل."
    assert question.answer_kind == "phone"


def _transfer_state():
    source = message("حولت فلوس وما وصلت")
    return context([source], [fact("issue", source.text, source)], category="failed_transfer").state


def test_secret_asking_suggestion_falls_back_to_the_template(taxonomy):
    state = _transfer_state()
    suggested = Question(key="recipient_phone", text="شنو رمز السر مالك؟", reason="حتى نلگه التحويل.", basis_revision=0)
    question = choose_question(state, suggested, 2, taxonomy)
    assert question.key == "recipient_phone"
    assert question.text != suggested.text
    assert "رمز" not in question.text


@pytest.mark.parametrize("reason", ["We need your PIN to find it.", "نحتاج رمز السر حتى نلگه التحويل."])
def test_secret_asking_reason_falls_back_to_the_template_reason(taxonomy, reason):
    state = _transfer_state()
    suggested = Question(key="recipient_phone", text="على أي رقم حولت؟", reason=reason, basis_revision=0)
    question = choose_question(state, suggested, 2, taxonomy)
    assert question.text == "على أي رقم حولت؟"
    assert question.reason == ask_for(state, "recipient_phone", 2).reason
    assert question.reason != reason


def _received_unknown_sender(source, *, phone="07501112233"):
    return [
        fact("issue", f"وصلني تحويل من رقم {phone} وما أعرف المرسل", source),
        fact("amount", "200000", source, normalized="200000"),
        fact("date", "07-10-2026", source, normalized="2026-10-07"),
        fact("txn_ref", "ZC2410000789", source, normalized="ZC2410000789"),
    ]


def test_received_money_from_an_unknown_sender_asks_what_to_do(taxonomy):
    source = message("وصلني تحويل 200,000 دينار يوم 07-10-2026 من رقم 07501112233 وانا ما اعرف المرسل. رقم العملية ZC2410000789")
    state = context([source], _received_unknown_sender(source), category="wrong_recipient").state
    suggested = Question(key="recipient_phone", text="على أي رقم حولت الفلوس؟", reason="بساعدنا نلكه التحويل.", basis_revision=0)
    question = choose_question(state, suggested, 2, taxonomy)
    assert question is not None
    assert question.key == "desired_outcome"
    assert question.answer_kind == "text"
    assert "حولت" not in question.text
    assert "المرسل" in question.text
    readiness = assess_readiness(state, taxonomy)
    assert readiness.next_key == "desired_outcome"
    assert "recipient_phone" not in readiness.missing
    assert "recipient_name" not in readiness.missing
    answered = state.model_copy(update={"facts": {
        **state.facts, "desired_outcome": fact("desired_outcome", "اعرف منو المرسل", source),
    }})
    assert choose_question(answered, None, 3, taxonomy) is None
    assert assess_readiness(answered, taxonomy).quality == "sufficient_context"


def test_received_money_without_a_sender_number_asks_where_it_came_from(taxonomy):
    source = message("وصلني تحويل وما اعرف المرسل")
    facts = [
        fact("issue", source.text, source),
        fact("amount", "200000", source, normalized="200000"),
        fact("date", "07-10-2026", source, normalized="2026-10-07"),
    ]
    state = context([source], facts, category="failed_transfer").state
    suggested = Question(key="recipient_phone", text="على أي رقم حولت الفلوس؟", reason="يساعدنا نلگه التحويل.", basis_revision=0)
    question = choose_question(state, suggested, 2, taxonomy)
    assert question is not None
    assert question.key == "sender_phone"
    assert question.answer_kind == "phone"
    assert question.text == "من أي رقم وصلتك الفلوس؟"
    assert "حولت" not in question.text


def test_received_details_stay_visible_while_asking_what_to_do(taxonomy):
    source = message("وصلني تحويل 200,000 دينار يوم 07-10-2026 من رقم 07501112233 وانا ما اعرف المرسل. رقم العملية ZC2410000789")
    state = context([source], [
        fact("issue", "وصلني تحويل من مرسل ما أعرفه", source),
        fact("amount", "200,000", source, normalized="200000"),
        fact("date", "07-10-2026", source),
        fact("txn_ref", "ZC2410000789", source, normalized="ZC2410000789"),
        fact("sender_phone", "07501112233", source, normalized="07501112233"),
    ], category="general_inquiry").state
    question = choose_question(state, None, 2, taxonomy)
    assert question is not None and question.key == "desired_outcome"
    shown = {item.key: item.display for item in progress(state, taxonomy)}
    assert shown["amount"] == "200000"
    assert shown["date"] == "07-10-2026"
    assert shown["sender_phone"] == "07501112233"
    assert shown["txn_ref"] == "ZC2410000789"


def test_paid_bill_then_unpaid_notice_is_not_money_the_customer_received(taxonomy):
    """دفعت فاتورة … جاني اشعار means a bill looked paid, then a notice said it was not."""
    source = message(
        "دفعت فاتورة الكهرباء 35,000 دينار يوم الخميس وطلعت ناجحة بس بعدها جاني اشعار انها ما مدفوعة"
    )
    state = context([source], [
        fact("issue", "دفعت فاتورة الكهرباء وطلعت ناجحة بس بعدها جاني اشعار انها ما مدفوعة", source),
        fact("biller", "الكهرباء", source),
        fact("amount", "35,000", source, normalized="35000"),
        fact("date", "يوم الخميس", source, normalized="2026-11-12"),
    ], category="bill_payment").state
    assert customer_received_money(state) is False
    suggested = Question(
        key="sender_phone", text="من أي رقم وصلتك الفلوس؟",
        reason="حتى نعرف منو اللي دز التحويل.", basis_revision=0,
    )
    question = choose_question(state, suggested, 1, taxonomy)
    assert question is not None
    assert question.key == "txn_ref"
    assert "وصلتك" not in question.text
    assert "المرسل" not in question.text


@pytest.mark.parametrize("text", [
    "جاني تحويل 50000 دينار",
    "وصلني مبلغ ٥٠ الف",
    "استلمت الفلوس",
])
def test_money_that_arrived_is_still_an_incoming_transfer(text):
    source = message(text)
    state = context([source], [fact("issue", text, source)]).state
    assert customer_received_money(state) is True


@pytest.mark.parametrize("text", [
    "جاني اشعار ان الفاتورة 35,000 دينار ما مدفوعة",
    "استلمت رسالة انو المبلغ 35,000 دينار ما انخصم",
])
def test_a_notice_about_money_is_not_money_received(text):
    source = message(text)
    state = context([source], [fact("issue", text, source)]).state
    assert customer_received_money(state) is False
