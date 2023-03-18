from src.devices.AppleTv import AppleTv
from src.repositories.ContentRepository import ContentRepository
from src.services import LoggerService


class CollectorService:
    def __init__(self, devices: list[AppleTv], content_repository: ContentRepository, logger_service: LoggerService):
        self.devices = devices
        self.content_repository = content_repository
        self.logger_service = logger_service

    async def collect(self, loop):
        for device in self.devices:
            self.logger_service.log(f"Trying to collect data from {device.name}")

            if not await device.get_is_connected():
                self.logger_service.log(f"Device {device.name} is not connected, trying to connect...")
                await device.connect(loop)
                self.logger_service.log(f"Device {device.name} connected")

            if not await device.is_playing():
                self.logger_service.log(f"Device {device.name} is not playing, skipping...")
                continue

            playback_info = await device.get_playback_info()
            self.logger_service.log(f"Playback info from device {device.name}: {playback_info}")
            self.content_repository.insert_record([
                playback_info["title"],
                playback_info["artist"],
                playback_info["album"],
                playback_info["position"],
                playback_info["app_identifier"],
                playback_info["device"],
                playback_info["media_type"],
            ])
            self.logger_service.log(f"Saved to database content from {device.name}")