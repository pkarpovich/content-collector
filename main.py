import asyncio

from pyatv.const import Protocol
from os import environ as env
from dotenv import load_dotenv

from repositories.ContentRepository import ContentRepository
from devices.AppleTv import AppleTv
from services.CollectorService import CollectorService
from services.LoggerService import LoggerService

load_dotenv()

Database_Path = env.get('DATABASE_PATH', './data/content_history.db')
Sleep_Timeout = int(env.get('SLEEP_TIMEOUT', 60))

logger_service = LoggerService()

def init_devices():
    living_room = AppleTv(
        name=env.get('ATV_NAME'),
        identifiers={env.get('ATV_ID')},
        credentials={
            Protocol.AirPlay: env.get('ATV_AIR_PLAY_CREDENTIALS'),
            Protocol.Companion: env.get('ATV_COMPANION_CREDENTIALS'),
            Protocol.RAOP: env.get('ATV_RAOP_CREDENTIALS'),
        },
        logger_service=logger_service
    )

    return [living_room]


def init_content_repo():
    return ContentRepository(Database_Path)


async def collect_playback_data(loop, devices: list[AppleTv], content_repo: ContentRepository):
    collector = CollectorService(devices, content_repo, logger_service)
    while True:
        await collector.collect(loop)
        logger_service.log(f"Sleeping for {Sleep_Timeout} seconds...")
        logger_service.log("========================================")
        await asyncio.sleep(Sleep_Timeout)

if __name__ == "__main__":
    LOOP = asyncio.new_event_loop()
    asyncio.set_event_loop(LOOP)

    content_repo = init_content_repo()
    devices = init_devices()

    LOOP.run_until_complete(collect_playback_data(LOOP, devices, content_repo))