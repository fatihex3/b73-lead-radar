from dataclasses import dataclass
from datetime import datetime


@dataclass
class Lead:
    source: str
    external_id: str
    title: str
    body: str
    url: str

    posted_at: datetime | None = None
    budget_text: str | None = None

    status: str = "NEW"
    ai_score: float | None = None
    ai_reason: str | None = None
