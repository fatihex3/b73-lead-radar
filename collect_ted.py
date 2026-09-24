from lead_radar.collectors.ted import (
    TedCollector,
    TedCollectorConfig,
)
from lead_radar.config import get_settings
from lead_radar.database import LeadDatabase


def main():
    settings = get_settings()

    database = LeadDatabase(
        settings.database_path
    )

    collector = TedCollector(
        TedCollectorConfig(
            cpv_code="72413000",
            lookback_days=3,
            page_size=20,
        )
    )

    leads = collector.collect()

    inserted = 0
    duplicates = 0

    for lead in leads:
        created = database.insert_lead(
            lead
        )

        if created:
            inserted += 1
        else:
            duplicates += 1

    print(
        f"Fetched: {len(leads)}"
    )

    print(
        f"Inserted: {inserted}"
    )

    print(
        f"Duplicates: {duplicates}"
    )


if __name__ == "__main__":
    main()
