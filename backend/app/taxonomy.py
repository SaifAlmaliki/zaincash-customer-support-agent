from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

PRIORITIES = ("P1", "P2", "P3", "P4")
FIELD_NAMES = ("txn_ref", "amount", "phone", "date")


class TaxonomyError(ValueError):
    """Raised when taxonomy.yaml is inconsistent."""


@dataclass(frozen=True)
class Category:
    id: str
    team: str
    what_en: str
    what_ar: str
    not_for: str
    examples: tuple[str, ...]
    required_fields: tuple[str, ...]
    min_priority: str
    needs_transaction: bool

    def describe(self) -> str:
        """One-line description used by both Jev criteria and Gemini prompts."""
        parts = [f"{self.what_en} ({self.what_ar})"]
        if self.not_for:
            parts.append(f"Not for: {self.not_for}")
        if self.examples:
            parts.append("Examples: " + " | ".join(self.examples))
        return ". ".join(parts)


@dataclass(frozen=True)
class Taxonomy:
    teams: tuple[str, ...]
    categories: dict[str, Category]

    @property
    def ids(self) -> tuple[str, ...]:
        return tuple(self.categories)

    def get(self, category_id: str) -> Category:
        return self.categories.get(category_id, self.categories["other"])

    def render(self) -> str:
        return "\n".join(f"- {c.id}: {c.describe()}" for c in self.categories.values())


def priority_rank(priority: str) -> int:
    if priority not in PRIORITIES:
        raise ValueError(f"unknown priority {priority!r}")
    return PRIORITIES.index(priority)


def most_urgent(*priorities: str) -> str:
    return min(priorities, key=priority_rank)


def load_taxonomy(path: str | Path) -> Taxonomy:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    teams = tuple(data["teams"])
    categories: dict[str, Category] = {}
    for raw in data["categories"]:
        cid = raw["id"]
        if cid in categories:
            raise TaxonomyError(f"duplicate category {cid}")
        if raw["team"] not in teams:
            raise TaxonomyError(f"category {cid} uses unknown team {raw['team']!r}")
        if raw["min_priority"] not in PRIORITIES:
            raise TaxonomyError(f"category {cid} has invalid min_priority")
        required = tuple(raw.get("required_fields") or ())
        unknown = set(required) - set(FIELD_NAMES)
        if unknown:
            raise TaxonomyError(f"category {cid} requires unknown fields {sorted(unknown)}")
        categories[cid] = Category(
            id=cid,
            team=raw["team"],
            what_en=str(raw["what_en"]).strip(),
            what_ar=str(raw["what_ar"]).strip(),
            not_for=str(raw.get("not_for") or "").strip(),
            examples=tuple(raw.get("examples") or ()),
            required_fields=required,
            min_priority=raw["min_priority"],
            needs_transaction=bool(raw.get("needs_transaction", False)),
        )
    if "other" not in categories:
        raise TaxonomyError("taxonomy must define an 'other' category")
    return Taxonomy(teams=teams, categories=categories)
