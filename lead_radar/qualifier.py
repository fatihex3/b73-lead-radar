import json
import re
from dataclasses import dataclass

from lead_radar.config import Settings
from lead_radar.nvidia import NvidiaClient


@dataclass
class Qualification:
    score: float
    qualified: bool
    reason: str


SYSTEM_PROMPT = """
You are a sales lead qualification system.

Evaluate whether the supplied opportunity represents
a realistic paid software or web-development opportunity.

Prioritize:

- explicit buyer intent
- clear development need
- realistic paid work
- project-based / fixed-price suitability
- clear scope
- commercial urgency

Avoid treating these as strong leads:

- developers advertising themselves
- unpaid collaboration
- revenue-share-only arrangements
- vague networking posts
- recruitment with no project
- social-media-only work
- clearly irrelevant requests

Return JSON only:

{
  "score": 0-100,
  "qualified": true,
  "reason": "short explanation"
}
"""


def extract_json(text: str) -> dict:
    text = text.strip()

    fenced = re.search(
        r"```(?:json)?\s*(\{.*?\})\s*```",
        text,
        re.DOTALL,
    )

    if fenced:
        text = fenced.group(1)

    else:
        match = re.search(
            r"\{.*\}",
            text,
            re.DOTALL,
        )

        if match:
            text = match.group(0)

    return json.loads(text)


class LeadQualifier:
    def __init__(
        self,
        settings: Settings,
        client: NvidiaClient,
    ):
        self.settings = settings
        self.client = client

    def analyze(
        self,
        title: str,
        body: str,
        budget_text: str | None = None,
    ) -> Qualification:

        prompt = f"""
TITLE:
{title}

BODY:
{body}

BUDGET:
{budget_text or "Not specified"}
"""

        raw = self.client.chat(
            model=self.settings.fast_model,
            system_prompt=SYSTEM_PROMPT,
            user_prompt=prompt,
        )

        data = extract_json(raw)

        score = float(data["score"])
        qualified = bool(data["qualified"])
        reason = str(data["reason"])

        return Qualification(
            score=score,
            qualified=qualified,
            reason=reason,
        )
