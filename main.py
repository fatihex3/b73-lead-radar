from lead_radar.config import get_settings
from lead_radar.database import LeadDatabase
from lead_radar.nvidia import NvidiaClient
from lead_radar.qualifier import LeadQualifier
from lead_radar.pipeline import LeadPipeline
from lead_radar.telegram_bot import TelegramLeadBot


def main():
    settings = get_settings()

    database = LeadDatabase(
        settings.database_path
    )

    nvidia = NvidiaClient(
        settings
    )

    qualifier = LeadQualifier(
        settings,
        nvidia,
    )

    pipeline = LeadPipeline(
        database,
        qualifier,
    )

    bot = TelegramLeadBot(
        settings,
        database,
        pipeline,
    )

    bot.run()


if __name__ == "__main__":
    main()
