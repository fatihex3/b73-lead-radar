from lead_radar.database import LeadDatabase
from lead_radar.qualifier import LeadQualifier


class LeadPipeline:
    def __init__(
        self,
        database: LeadDatabase,
        qualifier: LeadQualifier,
    ):
        self.database = database
        self.qualifier = qualifier

    def analyze_new(self):
        leads = self.database.get_new_leads()

        results = []

        for lead in leads:

            result = self.qualifier.analyze(
                title=lead["title"],
                body=lead["body"],
                budget_text=lead["budget_text"],
            )

            status = (
                "QUALIFIED"
                if result.qualified
                else "SKIPPED"
            )

            self.database.update_analysis(
                lead_id=lead["id"],
                score=result.score,
                reason=result.reason,
                status=status,
            )

            results.append(
                {
                    "id": lead["id"],
                    "title": lead["title"],
                    "score": result.score,
                    "status": status,
                    "reason": result.reason,
                }
            )

        return results
