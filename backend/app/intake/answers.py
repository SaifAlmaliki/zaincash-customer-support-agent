"""Record a tapped quick reply without asking the model to interpret it."""
from __future__ import annotations

from app.intake.contracts import Analysis, EvidenceRef, Fact, TurnContext
from app.intake.errors import InvalidEvidence


def quick_answer(context: TurnContext, key: str, choice: str) -> Analysis:
    source = next(
        (item for item in context.messages if item.id == context.current_message_id and item.role == "user"), None
    )
    if source is None or not source.text.strip():
        raise InvalidEvidence("Send the answer as a message.")
    evidence = [EvidenceRef(kind="message", source_id=source.id, quote=source.text)]
    if choice == "unknown":
        update = Fact(key=key, status="unknown", evidence=evidence)
    elif choice in {"yes", "no"}:
        update = Fact(key=key, status="known", value=source.text, normalized=choice, evidence=evidence)
    else:
        raise InvalidEvidence("Choose one of the offered answers.")
    return Analysis(language=source.language, category=context.state.category, updates=[update])
