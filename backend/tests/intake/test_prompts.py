from pathlib import Path

PROMPTS = Path(__file__).resolve().parents[2] / "app" / "intake" / "prompts"


def test_intake_prompt_knows_the_recipient_name_and_implied_answers():
    text = (PROMPTS / "intake_v1.md").read_text(encoding="utf-8")
    vocabulary = next(line for line in text.splitlines() if line.startswith("- Fact keys in updates:"))
    assert "recipient_name" in vocabulary
    assert "ما وصلت" in text and "انقطعت" in text
    assert "reason" in text and "why" in text.lower()


def test_review_prompt_asks_for_a_narrative_not_a_field_list():
    text = (PROMPTS / "review_v1.md").read_text(encoding="utf-8")
    assert "narrative" in text
    assert "label: value" in text
