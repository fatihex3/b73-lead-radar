from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any

import httpx

from lead_radar.models import Lead


TED_SEARCH_URL = "https://api.ted.europa.eu/v3/notices/search"


@dataclass
class TedCollectorConfig:
    cpv_code: str = "72413000"
    lookback_days: int = 30
    page_size: int = 20
    timeout_seconds: float = 20.0


class TedCollector:
    def __init__(
        self,
        config: TedCollectorConfig | None = None,
    ):
        self.config = config or TedCollectorConfig()

    def _build_query(self) -> str:
        now = datetime.now(timezone.utc)

        start = now - timedelta(
            days=self.config.lookback_days
        )

        start_str = start.strftime("%Y%m%d")
        end_str = now.strftime("%Y%m%d")

        return (
            f"publication-date = ({start_str} <> {end_str})"
        )

    def _payload(self) -> dict[str, Any]:
        return {
            "query": self._build_query(),
            "fields": [
                "publication-number",
                "notice-title",
                "publication-date",
                "classification-cpv",
                "buyer-name",
                "buyer-country",
                "deadline",
            ],
            "page": 1,
            "limit": self.config.page_size,
            "scope": "ACTIVE",
            "checkQuerySyntax": True,
            "paginationMode": "PAGE_NUMBER",
        }

    def fetch(self) -> list[dict[str, Any]]:
        payload = self._payload()

        with httpx.Client(
            timeout=self.config.timeout_seconds
        ) as client:
            response = client.post(
                TED_SEARCH_URL,
                json=payload,
                headers={
                    "Accept": "application/json",
                    "User-Agent": "B73-Lead-Radar/1.0",
                },
            )

            print("TED STATUS:", response.status_code)

            if response.status_code >= 400:
                print("TED RESPONSE:", response.text)

            response.raise_for_status()

            data = response.json()

        print("TED KEYS:", list(data.keys()))

        notices = (
            data.get("notices")
            or data.get("results")
            or []
        )

        print("RAW RESULT COUNT:", len(notices))

        if not isinstance(notices, list):
            raise RuntimeError(
                "Unexpected TED API response format."
            )

        return notices

    @staticmethod
    def _first(value: Any) -> str | None:
        if value is None:
            return None

        if isinstance(value, list):
            if not value:
                return None
            return str(value[0])

        return str(value)

    def normalize(
        self,
        notice: dict[str, Any],
    ) -> Lead | None:
        publication_number = self._first(
            notice.get("publication-number")
        )

        if not publication_number:
            return None

        title = (
            self._first(
                notice.get("notice-title")
            )
            or "TED procurement notice"
        )

        buyer = self._first(
            notice.get("buyer-name")
        )

        country = self._first(
            notice.get("buyer-country")
        )

        deadline = self._first(
            notice.get("deadline")
        )

        publication_date = self._first(
            notice.get("publication-date")
        )

        body_parts: list[str] = []

        if buyer:
            body_parts.append(
                f"Buyer: {buyer}"
            )

        if country:
            body_parts.append(
                f"Country: {country}"
            )

        if deadline:
            body_parts.append(
                f"Deadline: {deadline}"
            )

        body_parts.append(
            f"CPV: {self.config.cpv_code}"
        )

        url = (
            "https://ted.europa.eu/en/notice/"
            f"{publication_number}/html"
        )

        posted_at = None

        if publication_date:
            try:
                posted_at = datetime.fromisoformat(
                    publication_date.replace(
                        "Z",
                        "+00:00",
                    )
                )
            except ValueError:
                try:
                    posted_at = datetime.strptime(
                        publication_date,
                        "%Y-%m-%d",
                    ).replace(
                        tzinfo=timezone.utc
                    )
                except ValueError:
                    posted_at = None

        return Lead(
            source="EU_TED",
            external_id=publication_number,
            title=title,
            body="\n".join(body_parts),
            url=url,
            posted_at=posted_at,
            budget_text=None,
        )

    def collect(self) -> list[Lead]:
        raw_notices = self.fetch()

        leads: list[Lead] = []

        for notice in raw_notices:
            lead = self.normalize(notice)

            if lead is not None:
                leads.append(lead)

        return leads
