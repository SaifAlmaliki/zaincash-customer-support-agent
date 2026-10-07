import pytest

from app.config import REPO_ROOT
from app.taxonomy import TaxonomyError, load_taxonomy, most_urgent, priority_rank

EXPECTED = {
    "failed_transfer", "wrong_recipient", "login_access", "agent_dispute", "card_issue",
    "bill_payment", "account_kyc", "refund_request", "fraud_report", "app_bug",
    "general_inquiry", "other",
}


@pytest.fixture(scope="module")
def taxonomy():
    return load_taxonomy(REPO_ROOT / "data" / "taxonomy.yaml")


def test_loads_all_categories(taxonomy):
    assert set(taxonomy.ids) == EXPECTED
    assert taxonomy.get("failed_transfer").team == "Payments Ops"
    assert taxonomy.get("fraud_report").min_priority == "P1"
    assert taxonomy.get("failed_transfer").required_fields == ("amount", "date")


def test_unknown_id_falls_back_to_other(taxonomy):
    assert taxonomy.get("nope").id == "other"


def test_every_category_is_complete(taxonomy):
    for c in taxonomy.categories.values():
        assert c.examples, c.id
        assert c.team in taxonomy.teams


def test_describe_and_render(taxonomy):
    d = taxonomy.get("failed_transfer").describe()
    assert "Not for:" in d and "Examples:" in d
    assert "- failed_transfer: " in taxonomy.render()


def test_priority_helpers():
    assert priority_rank("P1") < priority_rank("P4")
    assert most_urgent("P3", "P1", "P2") == "P1"


def test_rejects_unknown_team(tmp_path):
    p = tmp_path / "t.yaml"
    p.write_text(
        "teams: [A]\ncategories:\n  - {id: other, team: B, what_en: x, what_ar: y,"
        " examples: [z], min_priority: P4}\n",
        encoding="utf-8",
    )
    with pytest.raises(TaxonomyError):
        load_taxonomy(p)
