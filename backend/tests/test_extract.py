from app.llm import LLMUnavailable
from app.pipeline.contracts import FieldPick
from app.pipeline.stage1_normalize.candidates import find_candidates
from app.pipeline.stage1_normalize.normalize import normalize
from app.pipeline.stage3_extract.extract import fill_gaps, finalize
from tests.fakes import FakeExtractor
from tests.helpers import make_ticket

TEXT = "حولت ٥٠ الف لرقم 0770 123 4567 امس رقم العملية ZC-2410000123"


def _setup(text=TEXT):
    nt = normalize(make_ticket(text))
    return nt, find_candidates(nt.match_text)


def test_jev_picks_map_to_candidates_and_normalize():
    nt, cands = _setup()
    picks = {
        "txn_ref": FieldPick("ZC-2410000123", 0.95, "jev_pick"),
        "amount": FieldPick("50 الف", 0.9, "jev_pick"),
        "phone": FieldPick("0770 123 4567", 0.8, "jev_pick"),
        "date": FieldPick("امس", 0.9, "jev_pick"),
    }
    ex = finalize(picks, cands, nt)
    assert ex["txn_ref"].value == "ZC2410000123"
    assert ex["amount"].value == 50000 and ex["amount"].currency == "IQD"
    assert ex["phone"].value == "07701234567"
    assert ex["date"].value == "2026-10-06"
    a = ex["amount"]
    assert nt.ticket.text[a.start : a.end] == "٥٠ الف"  # span indexes the original text


def test_missing_picks_are_null():
    nt, cands = _setup()
    ex = finalize({}, cands, nt)
    assert all(f.value is None for f in ex.values())


def test_gemini_word_amount_uses_normalized_hint():
    nt, cands = _setup("حولت خمسين الف")
    ex = finalize({"amount": FieldPick("خمسين الف", 0.6, "gemini", "50000")}, cands, nt)
    assert ex["amount"].value == 50000 and ex["amount"].span == "خمسين الف"


def test_gemini_span_not_in_text_is_null():
    nt, cands = _setup("حولت فلوس")
    ex = finalize({"amount": FieldPick("100 الف", 0.6, "gemini", "100000")}, cands, nt)
    assert ex["amount"].value is None


async def test_fill_gaps_only_asks_for_weak_required_fields():
    nt, cands = _setup("حولت خمسين الف امس")
    ex = finalize({"date": FieldPick("امس", 0.9, "jev_pick")}, cands, nt)
    fake = FakeExtractor(picks={"amount": FieldPick("خمسين الف", 0.6, "gemini", "50000")})
    filled, cost = await fill_gaps(ex, nt, ("amount", "date"), fake)
    assert fake.requested == [["amount"]]
    assert filled["amount"].value == 50000 and cost > 0


async def test_fill_gaps_noop_and_failure_tolerant():
    nt, cands = _setup("سؤال عام")
    ex = finalize({}, cands, nt)
    assert await fill_gaps(ex, nt, (), FakeExtractor()) == (ex, 0.0)
    failing = FakeExtractor(raises=LLMUnavailable("down"))
    assert await fill_gaps(ex, nt, ("amount",), failing) == (ex, 0.0)
