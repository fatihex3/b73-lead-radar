from lead_radar.config import get_settings
from lead_radar.database import LeadDatabase
from lead_radar.models import Lead


settings = get_settings()

db = LeadDatabase(
    settings.database_path
)

lead = Lead(
    source="manual",
    external_id="demo-001",
    title="Need a website for my local business",
    body=(
        "Looking for a developer to build a "
        "5-page responsive website for my company. "
        "Budget is $600."
    ),
    url="https://example.com/demo",
    budget_text="$600",
)

created = db.insert_lead(lead)

print(
    "Lead inserted."
    if created
    else "Lead already exists."
)
