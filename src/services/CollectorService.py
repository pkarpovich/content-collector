from src.devices.AppleTv import AppleTv
from src.repositories.ContentRepository import ContentRepository


class CollectorService:
    def __init__(self, devices: list[AppleTv], content_repository: ContentRepository):
        self.devices = devices
        self.content_repository = content_repository

    async def collect(self, loop):
        for device in self.devices:
            print(f"Trying to collect data from {device.name}")

            if not await device.get_is_connected():
                print(f"Device {device.name} is not connected, trying to connect...")
                await device.connect(loop)
                print(f"Device {device.name} connected")

            if not await device.is_playing():
                print(f"Device {device.name} is not playing, skipping...")
                continue

            playback_info = await device.get_playback_info()
            print(f"Playback info from device {device.name}: {playback_info}")
            self.content_repository.insert_record([
                playback_info["title"],
                playback_info["artist"],
                playback_info["album"],
                playback_info["position"],
                playback_info["app_identifier"],
                playback_info["device"],
                playback_info["media_type"],
            ])
            print(f"Saved to database content from {device.name}")