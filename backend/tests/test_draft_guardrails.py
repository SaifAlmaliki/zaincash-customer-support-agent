"""Draft checks exercise evidence boundaries, not arbitrary numeric substrings."""
from copy import deepcopy
from dataclasses import replace
from datetime import timedelta

import pytest

from app.kb.contracts import Passage
from app.pipeline.contracts import ExtractedField, LookupResult, TxnRecord
from app.pipeline.stage6_draft.guardrails import check_draft, requests_credentials
from tests.helpers import RECEIVED, make_ticket

REF = "ZC2410000123"
TEXT = "حولت ٥٠ الف دينار يوم ٦/١٠/٢٠٢٦ للرقم ٠٧٧٠١٢٣٤٥٦٧ المرجع ZC٢٤١٠٠٠٠١٢٣"
REPLY = "نراجع حوالتك ونرجعلك بالتفاصيل. لا تشارك الرقم السري ويا أي شخص."
PASSAGE = Passage("policy:current:0", 1, 0, "سياسة الحوالات", "policy.txt", 0.9)


@pytest.fixture
def state():
    return {"ticket": make_ticket(TEXT), "lookup": LookupResult("not_found")}


def check(reply, state, *, citations=None, used_txn_ref=None, retrieved=None):
    return check_draft(
        reply, [PASSAGE.id] if citations is None else citations, used_txn_ref, state,
        {PASSAGE.id: PASSAGE} if retrieved is None else retrieved,
    )


@pytest.mark.parametrize(("reply", "unsafe"), [
    ("لا تشارك الرقم السري ويا أي شخص.", False),
    ("دزلي الرقم السري حتى أساعدك.", True),
    ("لا تشارك الرمز ويا غيرنا. أرسل لنا رمز OTP.", True),
    ("Never share your PIN.", False),
    ("Please send your password.", True),
    ("Don't send us your OTP.", False),
    ("Do not disclose your one-time password.", False),
    ("لا تْدز الرمز السري لأي شخص.", False),
    ("إيّاك ومشاركة كلمة المرور.", False),
    ("ممنوع إرسال رمز التحقق.", False),
    ("لازم ما تشارك كلمة السر ويه أحد.", False),
    ("لا تدز الرمز بس دزلنا كلمة المرور.", True),
    ("لا تشارك الرمز، وارسل لنا الرقم السري.", True),
    ("لا تشارك الرقم السري وارسل لنا رمز التحقق", True),
    ("Never share your PIN but send us your OTP.", True),
    ("Don't share your PIN and provide your password here.", True),
    ("لا تقلق، دزلي رمز التحقق.", True),
    ("Don't worry, send the OTP to support.", True),
    ("دزلي كلمه السر على الخاص.", True),
    ("زودنا بالرمز السري.", True),
    ("Please give us your passcode.", True),
    ("Reply with your one-time code.", True),
    ("الرقم السري ارسله لنا.", True),
    ("دزلي رقم الحوالة حتى نتابع طلبك.", False),
    ("غيّر كلمة المرور من التطبيق.", False),
    ("Enter your PIN in the official app.", False),
    ("لا تشارك الرمز ولا ترسل كلمة المرور.", False),
    ("Please do not ever share your PIN.", False),
    ("نحتاج منك رمز التحقق حتى نكمل الطلب.", True),
    ("شاركنا رمز الدخول.", True),
    ("أرسل لنا كلمة مرورك.", True),
    ("We need your PIN to proceed.", True),
    ("We will never ask you to share your PIN.", False),
    ("We will never ask you to share your PIN but send your OTP here.", True),
    ("Never share your PIN and send us the transaction reference.", False),
    ("لا تشارك الرمز وارسل لنا رقم الحوالة.", False),
])
def test_credential_requests_respect_local_negation(reply, unsafe):
    assert requests_credentials(reply) is unsafe


def test_live_draft_avoid_sharing_warning_is_not_a_credential_request(state):
    # Actual OpenRouter draft from synthetic browser run 39: Jev scored 0.04,
    # but the deterministic checker treated "تجنب مشاركة" as a request.
    reply = (
        "أهلاً بك. لشرح مشكلتك بأمان، تكدر تذكر وصف مختصر للمشكلة، "
        "نص رسالة الخطأ إذا ظهرت عندك، ومرجع العملية إن وجد. "
        "يرجى تجنب مشاركة أي معلومات سرية مثل رمز التحقق (OTP)، "
        "الرمز السري (PIN)، أو كلمة المرور، وعدم إرسال صور المستمسكات. "
        "فريقنا بخدمتك دائماً."
    )
    assert check(reply, state) == []


@pytest.mark.parametrize(("reply", "unsafe"), [
    ("تجنب إرسال أو مشاركة رمز التحقق.", False),
    ("وتجنب تماماً مشاركة أي بيانات سرية مثل رمز التحقق (OTP).", False),
    ("تجنب مشاركة الرقم السري وارسل لنا رقم الحوالة.", False),
    ("تجنب مشاركة الرقم السري وارسل لنا رمز التحقق.", True),
    ("تجنب تماماً مشاركة الرقم السري وارسل لنا رمز التحقق.", True),
    ("يرجى تجنب مشاركة كلمة المرور. أرسل لنا رمز التحقق.", True),
    ("لا تتجنب مشاركة رمز التحقق معنا.", True),
])
def test_avoid_sharing_warning_does_not_excuse_a_later_request(reply, unsafe):
    assert requests_credentials(reply) is unsafe


@pytest.mark.parametrize(("reply", "findings"), [
    (REPLY, []),
    (" \n\t", ["empty_reply"]),
    ("123 !!!", ["non_arabic_reply"]),
    ("Please wait while we investigate.", ["non_arabic_reply"]),
    ("اب ab", []),  # Alphabetic ratio exactly 0.5 passes.
    ("اب abc", ["non_arabic_reply"]),
    ("مرحبا " * 120, []),
    ("مرحبا\n" * 121, ["reply_too_long"]),
    ("١. افتح التطبيق\n٢. اختار المساعدة\n٣. تواصل ويانا", []),
    ("دزلي الرقم السري حتى أساعدك.", ["requests_credentials"]),
])
def test_reply_findings_are_explicit(reply, findings, state):
    assert check(reply, state) == findings


def test_citations_must_have_been_retrieved_for_this_ticket(state):
    assert check(REPLY, state, citations=[]) == ["missing_citations"]
    assert check(REPLY, state, citations=[PASSAGE.id, "policy:older-run:0"]) == ["invalid_citations"]
    assert check(REPLY, state, retrieved={}) == ["invalid_citations"]


@pytest.mark.parametrize(("reply", "finding"), [
    ("مبلغ الحوالة ٥١ ألف دينار.", "ungrounded_amount"),
    ("مبلغ الحوالة ٥٠٠٠ دينار.", "ungrounded_amount"),
    ("مبلغ الحوالة ٥٠٠٠٠ دولار.", "ungrounded_amount"),
    ("مبلغ الحوالة USD 50000.", "ungrounded_amount"),
    ("رسوم الحوالة ٥ دينار.", "ungrounded_amount"),
    ("المبلغ 50.", "ungrounded_amount"),
    ("الحوالة بتاريخ 2026-10-05.", "ungrounded_date"),
    ("الحوالة بتاريخ 31/02/2026.", "ungrounded_date"),
    ("رقم الهاتف ٠٧٨٠١٢٣٤٥٦٧.", "ungrounded_phone"),
    ("مرجع الحوالة ZC2410000124.", "ungrounded_txn_ref"),
    ("مرجع الحوالة ZC24100001230.", "ungrounded_txn_ref"),
    ("مرجع الحوالة ZC241000012.", "ungrounded_txn_ref"),
    ("مبلغ الحوالة ٥٠٠٠٠٫٤ دينار.", "ungrounded_amount"),
    ("مبلغ الحوالة 50,000.40 دينار.", "ungrounded_amount"),
    ("مبلغ الحوالة -50000 دينار.", "ungrounded_amount"),
    ("الحوالة بتاريخ 05.10.2026.", "ungrounded_date"),
])
def test_invented_values_have_typed_findings(reply, finding, state):
    assert check(reply, state) == [finding]


@pytest.mark.parametrize("reply", [
    "حوالتك بمبلغ ٥٠٬٠٠٠ دينار بتاريخ ٢٠٢٦-١٠-٠٦ نتابعها ويه الفريق.",
    "حوالتك بمبلغ ۵۰ الف دينار بتاريخ ٦/١٠/٢٦ نتابعها ويه الفريق.",
    "حوالتك بمبلغ 50,000 IQD بتاريخ 2026-10-6 نتابعها ويه الفريق.",
    "حوالتك بمبلغ IQD 50000 نتابعها ويه الفريق.",
    "نراجع حوالتك للرقم +964 770 123 4567 ونرجعلك بالتفاصيل.",
    "نراجع حوالتك للرقم ۰۷۷۰۱۲۳۴۵۶۷ ونرجعلك بالتفاصيل.",
    "نراجع حوالتك المرجع zc-٢٤١٠٠٠٠١٢٣ ونرجعلك بالتفاصيل.",
    "حوالتك بتاريخ 06.10.2026 نتابعها ويه الفريق.",
    "حوالتك بتاريخ 2026/10/06 نتابعها ويه الفريق.",
    "حوالتك بمبلغ 50,000.00 دينار نتابعها ويه الفريق.",
])
def test_semantic_equivalents_are_grounded(reply, state):
    assert check(reply, state) == []


def txn():
    return TxnRecord(REF, "07701234567", "07809876543", None, 50000, "p2p", "pending",
                     RECEIVED - timedelta(days=1))


def test_confirmed_match_is_evidence_and_used_reference_must_identify_it():
    state = {"ticket": make_ticket("حوالتي معلقة"), "lookup": LookupResult("matched", txn())}
    reply = "حوالتك بمبلغ ٥٠ الف دينار بتاريخ ٦/١٠/٢٠٢٦ للرقم ٠٧٨٠٩٨٧٦٥٤٣ المرجع ZC2410000123"
    assert check(reply, state, used_txn_ref="zc-٢٤١٠٠٠٠١٢٣") == []
    assert check(REPLY, state, used_txn_ref="ZC2410000124") == ["invalid_used_txn_ref"]
    assert check(REPLY, state, used_txn_ref="") == ["invalid_used_txn_ref"]
    assert check(REPLY, state, used_txn_ref=REF + "0") == ["invalid_used_txn_ref"]


@pytest.mark.parametrize("status", ["not_found", "ambiguous", "amount_mismatch", "date_mismatch"])
def test_candidate_transactions_cannot_authorize_reply_evidence(status):
    state = {"ticket": make_ticket("حوالتي معلقة"), "lookup": LookupResult(status, txn(), 1)}
    reply = "حوالتك بمبلغ ٥٠ الف دينار بتاريخ ٦/١٠/٢٠٢٦ للرقم ٠٧٨٠٩٨٧٦٥٤٣ المرجع ZC2410000123"
    assert check(reply, state, used_txn_ref=REF) == [
        "invalid_used_txn_ref", "ungrounded_amount", "ungrounded_date",
        "ungrounded_phone", "ungrounded_txn_ref",
    ]


def test_ticket_reference_alone_does_not_confirm_used_reference(state):
    assert check(REPLY, state, used_txn_ref=REF) == ["invalid_used_txn_ref"]


def test_policy_passages_are_not_financial_evidence():
    state = {"ticket": make_ticket("حوالتي معلقة")}
    passage = replace(PASSAGE, text="رسوم الحوالة ٥٠٠ دينار")
    assert check("رسوم الحوالة ٥٠٠ دينار", state, retrieved={PASSAGE.id: passage}) == [
        "ungrounded_amount"
    ]


def test_ticket_customer_phone_and_relative_date_are_evidence():
    state = {"ticket": make_ticket("الحوالة امس", customer_phone="+9647701234567")}
    assert check("حوالتك بتاريخ ٦/١٠/٢٠٢٦ للرقم ٠٧٧٠١٢٣٤٥٦٧ نراجعها ويه الفريق", state) == []


def test_span_anchored_extracted_word_amount_is_evidence():
    state = {"ticket": make_ticket("خمسين الف"), "extracted": {
        "amount": ExtractedField(50000, "خمسين الف", 0, 9, "gemini", 0.9, "IQD"),
    }}
    assert check("حوالتك بمبلغ ٥٠٠٠٠ دينار نراجعها", state) == []
    state["extracted"]["amount"] = replace(state["extracted"]["amount"], span="غير موجود")
    assert check("حوالتك بمبلغ ٥٠٠٠٠ دينار نراجعها", state) == ["ungrounded_amount"]


def test_aggregation_is_deduplicated_and_has_no_state_side_effects(state):
    before = deepcopy(state)
    assert check("دزلي الرقم السري والمبلغ ٥١ الف و٥٢ الف دينار", state, citations=[]) == [
        "missing_citations", "ungrounded_amount", "requests_credentials",
    ]
    assert state == before


def test_fractional_usd_is_compared_without_rounding_or_currency_loss():
    state = {"ticket": make_ticket("دفعت $50.25")}
    assert check("المبلغ ٥٠٫٢٥ دولار نراجعه ويه الفريق", state) == []
    assert check("المبلغ ٥٠ دولار نراجعه ويه الفريق", state) == ["ungrounded_amount"]


def test_currency_after_multiplier_cannot_be_changed():
    state = {"ticket": make_ticket("دفعت 50 الف دولار")}
    assert check("المبلغ ٥٠٠٠٠ دولار نراجعه ويه الفريق", state) == []
    assert check("المبلغ ٥٠٠٠٠ دينار نراجعه ويه الفريق", state) == ["ungrounded_amount"]


def test_candidate_prompt_limit_does_not_hide_later_ungrounded_references():
    refs = " ".join(f"ZC241000{i:04}" for i in range(51))
    state = {"ticket": make_ticket(refs)}
    # Plenty of Arabic letters keep this focused on reference validation.
    reply = "اهلاوسهلا " * 30 + refs
    assert check(reply, state) == []
    assert check(reply + " ZC9999999999", state) == ["ungrounded_txn_ref"]


@pytest.mark.parametrize(("ticket", "reply", "findings"), [
    ("حولت 50000 دينار", "المبلغ 50 الف دينار والرسوم 50 الف دولار", ["ungrounded_amount"]),
    ("حولت 50000 دينار", "المبلغ 50000 دينار والتصحيح -50000 دينار", ["ungrounded_amount"]),
    ("حولت 50000 دينار", "المبلغ ٥٠ الف دينار والرسوم ۵۰ الف دولار", ["ungrounded_amount"]),
    ("حولت 50000 دينار", "المبلغ 50 الف دينار والتأكيد 50 الف دينار", []),
    ("المبلغ 50 الف دينار والرسوم 50 الف دولار", "الرسوم 50000 دولار حسب رسالتك", []),
    ("المبلغ -50000 دينار والتصحيح 50000 دينار", "التصحيح 50000 دينار حسب رسالتك", []),
])
def test_amount_occurrences_keep_their_own_currency_and_sign(ticket, reply, findings):
    assert check(reply, {"ticket": make_ticket(ticket)}) == findings


@pytest.mark.parametrize("reply", [
    "يرجى إرسال كلمة المرور حتى نراجع طلبك.",
    "يرجى إرسال أو مشاركة الرقم السري حتى نراجع طلبك.",
    "نرجو منك مشاركة رمز التحقق حتى نراجع طلبك.",
    "يرجى تزويدنا بكلمة المرور حتى نراجع طلبك.",
    "من فضلك تقديم كلمة المرور حتى نراجع طلبك.",
])
def test_polite_arabic_disclosure_requests_are_unsafe(reply, state):
    assert requests_credentials(reply) is True
    assert check(reply, state) == ["requests_credentials"]


@pytest.mark.parametrize("reply", [
    "لا ترسل أو تشارك الرقم السري مع أي شخص.",
    "لا ترسل وتشارك الرقم السري مع أي شخص.",
    "Never share or send your OTP.",
    "Do not share and send your password.",
    "لا تحتاج ترسل كلمة المرور.",
    "لا تحتاج أن ترسل أو تشارك كلمة المرور.",
    "You do not need to send or share your PIN.",
    "يرجى عدم إرسال أو مشاركة كلمة المرور.",
    "لا ترسل أو تشارك الرقم السري وارسل لنا رقم الحوالة.",
])
def test_coordinated_and_indirect_credential_warnings_are_safe(reply):
    assert requests_credentials(reply) is False


@pytest.mark.parametrize("reply", [
    "لا ترسل أو تشارك الرقم السري مع أي شخص. يرجى إرسال كلمة المرور لنا.",
    "لا ترسل أو تشارك الرقم السري مع أي شخص، أرسل لنا رمز التحقق.",
    "لا ترسل أو تشارك الرقم السري لكن يرجى تزويدنا بكلمة المرور.",
    "لا ترسل أو تشارك الرقم السري وارسل لنا رمز التحقق.",
    "Never share or send your OTP. Please send your password.",
    "Never share or send your OTP but provide your password here.",
    "Never share or send your OTP and send us your password.",
    "لا تحتاج ترسل كلمة المرور. يرجى إرسال رمز التحقق.",
    "لا تحتاج ترسل كلمة المرور وارسل لنا رمز التحقق.",
    "لا تحتاج الرمز، أرسل لنا كلمة المرور.",
    "لا تحتاج الرمز ارسل لنا كلمة المرور.",
    "You do not need to send your PIN but please send your OTP.",
    "You do not need to send your PIN and provide your password here.",
])
def test_warning_negation_cannot_authorize_a_following_disclosure_request(reply):
    assert requests_credentials(reply) is True


@pytest.mark.parametrize("warning", [
    "لا تحتاج إلى إرسال كلمة المرور.",
    "لا نحتاج إلى مشاركة كلمة المرور.",
    "لا نطلب منك إرسال كلمة المرور.",
    "نحذرك من مشاركة كلمة المرور.",
    "مشاركة كلمة المرور ممنوعة.",
])
def test_contextual_denials_and_prohibitions_stay_local(warning, state):
    assert requests_credentials(warning) is False
    assert check(warning, state) == []
    for reply in (
        warning + " يرجى إرسال رمز التحقق لنا.",
        warning.removesuffix(".") + " وارسل لنا رمز التحقق.",
    ):
        assert requests_credentials(reply) is True
        assert check(reply, state) == ["requests_credentials"]
