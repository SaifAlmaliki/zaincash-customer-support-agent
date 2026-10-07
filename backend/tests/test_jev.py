import pytest

from app.pipeline.candidates import find_candidates
from app.pipeline.classify.jev import NONE, JevClassifier
from app.pipeline.contracts import FLAG_NAMES
from app.pipeline.normalize import normalize
from tests.fakes import FakeJevRunnable
from tests.helpers import make_ticket

TEXT = "حولت ٥٠ الف لاخوي امس وما وصلت"


def _criteria(q):
    return getattr(q, "criteria", None) if hasattr(q, "criteria") else q["criteria"]


def _run(tax, runnable, text=TEXT, max_chars=6000):
    nt = normalize(make_ticket(text))
    clf = JevClassifier(runnable, tax, model_id="jev-1.13.0", t_jev=0.6, min_top_prob=0.6,
                        price_in_per_m=0.042, max_state_chars=max_chars)
    return clf, nt, find_candidates(nt.match_text)


async def test_one_main_call_with_all_questions(tax):
    r = FakeJevRunnable(picks={"amount": ("50 الف", 0.9)})
    clf, nt, cands = _run(tax, r)
    out = await clf.classify(nt, cands)
    assert len(r.calls) == 2  # main call + option-order check
    main_q = r.calls[0]["questions"]
    assert {"category", "priority", *FLAG_NAMES, "pick_amount", "pick_date"} <= set(main_q)
    assert "pick_phone" not in main_q  # no phone candidates in the text
    assert set(_criteria(main_q["pick_amount"])) == {"50 الف", NONE}
    assert out.classification.category == "failed_transfer"
    assert out.classification.priority == "P2"
    assert not out.classification.uncertain and out.reasons == ()
    assert out.picks["amount"].value == "50 الف" and out.picks["amount"].method == "jev_pick"
    assert out.picks["phone"].method == "none"
    assert out.cost_usd == pytest.approx(2000 * 0.042 / 1e6)


async def test_order_check_uses_reversed_options(tax):
    r = FakeJevRunnable()
    clf, nt, cands = _run(tax, r)
    await clf.classify(nt, cands)
    main_keys = list(_criteria(r.calls[0]["questions"]["category"]))
    order_keys = list(_criteria(r.calls[1]["questions"]["category"]))
    assert order_keys == list(reversed(main_keys))


async def test_order_disagreement_is_uncertain(tax):
    clf, nt, cands = _run(tax, FakeJevRunnable(reversed_choice="wrong_recipient"))
    out = await clf.classify(nt, cands)
    assert out.classification.uncertain and out.reasons == ("low_confidence",)


async def test_low_top_probability_is_uncertain(tax):
    clf, nt, cands = _run(tax, FakeJevRunnable(top_prob=0.5))
    assert (await clf.classify(nt, cands)).classification.uncertain


async def test_unknown_category_is_other_and_uncertain(tax):
    clf, nt, cands = _run(tax, FakeJevRunnable(category="transfer_failed"))
    out = await clf.classify(nt, cands)
    assert out.classification.category == "other" and out.classification.uncertain


async def test_state_is_truncated(tax):
    r = FakeJevRunnable()
    clf, nt, cands = _run(tax, r, text="ا" * 50, max_chars=10)
    await clf.classify(nt, cands)
    assert len(r.calls[0]["state"]["ticket_text"]) == 10


async def test_priority_level_maps_to_p_label(tax):
    clf, nt, cands = _run(tax, FakeJevRunnable(priority_level=3))
    assert (await clf.classify(nt, cands)).classification.priority == "P1"
