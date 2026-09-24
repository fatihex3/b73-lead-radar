import sqlite3

from lead_radar.models import Lead


class LeadDatabase:
    def __init__(self, path: str):
        self.path = path
        self._initialize()

    def connect(self):
        return sqlite3.connect(self.path)

    def _initialize(self):
        with self.connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS leads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    source TEXT NOT NULL,
                    external_id TEXT NOT NULL,

                    title TEXT NOT NULL,
                    body TEXT NOT NULL,
                    url TEXT NOT NULL,

                    posted_at TEXT,
                    budget_text TEXT,

                    status TEXT NOT NULL DEFAULT 'NEW',

                    ai_score REAL,
                    ai_reason TEXT,

                    created_at TEXT NOT NULL
                        DEFAULT CURRENT_TIMESTAMP,

                    UNIQUE(source, external_id)
                )
                """
            )

    def insert_lead(self, lead: Lead) -> bool:
        try:
            with self.connect() as conn:
                conn.execute(
                    """
                    INSERT INTO leads (
                        source,
                        external_id,
                        title,
                        body,
                        url,
                        posted_at,
                        budget_text,
                        status
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        lead.source,
                        lead.external_id,
                        lead.title,
                        lead.body,
                        lead.url,
                        lead.posted_at.isoformat()
                        if lead.posted_at else None,
                        lead.budget_text,
                        lead.status,
                    ),
                )

            return True

        except sqlite3.IntegrityError:
            return False

    def get_new_leads(self):
        with self.connect() as conn:
            conn.row_factory = sqlite3.Row

            return conn.execute(
                """
                SELECT *
                FROM leads
                WHERE status = 'NEW'
                ORDER BY id ASC
                """
            ).fetchall()

    def update_analysis(
        self,
        lead_id: int,
        score: float,
        reason: str,
        status: str,
    ):
        with self.connect() as conn:
            conn.execute(
                """
                UPDATE leads
                SET
                    ai_score = ?,
                    ai_reason = ?,
                    status = ?
                WHERE id = ?
                """,
                (
                    score,
                    reason,
                    status,
                    lead_id,
                ),
            )

    def stats(self):
        with self.connect() as conn:
            conn.row_factory = sqlite3.Row

            total = conn.execute(
                "SELECT COUNT(*) AS count FROM leads"
            ).fetchone()["count"]

            rows = conn.execute(
                """
                SELECT status, COUNT(*) AS count
                FROM leads
                GROUP BY status
                """
            ).fetchall()

        return {
            "total": total,
            "statuses": {
                row["status"]: row["count"]
                for row in rows
            },
        }
