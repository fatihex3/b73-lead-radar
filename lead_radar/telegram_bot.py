from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from lead_radar.config import Settings
from lead_radar.database import LeadDatabase
from lead_radar.pipeline import LeadPipeline


class TelegramLeadBot:
    def __init__(
        self,
        settings: Settings,
        database: LeadDatabase,
        pipeline: LeadPipeline,
    ):
        self.settings = settings
        self.database = database
        self.pipeline = pipeline

    def authorized(self, update: Update) -> bool:
        if self.settings.telegram_allowed_user_id is None:
            return True

        if not update.effective_user:
            return False

        return (
            update.effective_user.id
            == self.settings.telegram_allowed_user_id
        )

    async def start(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ):
        if not self.authorized(update):
            return

        await update.message.reply_text(
            "🛰️ B73 Lead Radar connected."
        )

    async def status(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ):
        if not self.authorized(update):
            return

        stats = self.database.stats()

        lines = [
            "🛰️ B73 Lead Radar",
            "",
            f"Total: {stats['total']}",
        ]

        for status, count in stats["statuses"].items():
            lines.append(
                f"{status}: {count}"
            )

        await update.message.reply_text(
            "\n".join(lines)
        )

    async def analyze_new(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ):
        if not self.authorized(update):
            return

        await update.message.reply_text(
            "Analyzing new leads..."
        )

        results = self.pipeline.analyze_new()

        if not results:
            await update.message.reply_text(
                "No new leads."
            )
            return

        for item in results:

            message = (
                f"#{item['id']}\n"
                f"{item['title']}\n\n"
                f"Score: {item['score']:.0f}/100\n"
                f"Status: {item['status']}\n\n"
                f"{item['reason']}"
            )

            await update.message.reply_text(
                message
            )

    def run(self):
        if not self.settings.telegram_bot_token:
            raise RuntimeError(
                "TELEGRAM_BOT_TOKEN is missing."
            )

        app = (
            Application.builder()
            .token(
                self.settings.telegram_bot_token
            )
            .build()
        )

        app.add_handler(
            CommandHandler(
                "start",
                self.start,
            )
        )

        app.add_handler(
            CommandHandler(
                "status",
                self.status,
            )
        )

        app.add_handler(
            CommandHandler(
                "analyze_new",
                self.analyze_new,
            )
        )

        app.run_polling()
