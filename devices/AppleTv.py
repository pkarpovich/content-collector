from typing import TypedDict

from pyatv import connect, scan
from pyatv.const import Protocol, DeviceState
from pyatv.exceptions import AuthenticationError

from services import LoggerService


class PlaybackInfo(TypedDict):
    title: str
    artist: str
    album: str
    position: str
    app_identifier: str
    device: str
    media_type: str


class AppleTv:
    def __init__(self, name: str, identifiers: set[str | None], credentials: dict[Protocol, str], logger_service: LoggerService):
        self.name = name
        self.identifiers = identifiers
        self.credentials = credentials

        self.logger_service = logger_service
        self.atv = None

    async def connect(self, loop):
        confs = await scan(loop, identifier=self.identifiers)

        if not confs:
            self.logger_service.log(f"Device {self.name} not found")
            return None

        conf = confs[0]
        for protocol, credentials in self.credentials.items():
            conf.set_credentials(protocol, credentials)

        try:
            self.atv = await connect(conf, loop)
        except AuthenticationError as ex:
            self.logger_service.log(f"Authentication error: {ex}")

    async def get_is_connected(self):
        return self.atv is not None

    async def get_playing(self):
        return await self.atv.metadata.playing()

    async def get_device_state(self):
        playing = await self.get_playing()
        return playing.device_state

    async def is_playing(self):

        return await self.get_device_state() == DeviceState.Playing

    async def get_playback_info(self) -> PlaybackInfo:
        playing = await self.get_playing()
        percentage = (playing.position / playing.total_time) * 100
        formatted_percentage = "{:.2f}%".format(percentage)

        return {
            "title": playing.title,
            "artist": playing.artist,
            "album": playing.album,
            "position": formatted_percentage,
            "app_identifier": self.atv.metadata.app.identifier,
            "device": self.atv.device_info.raw_model,
            "media_type": playing.media_type.name,
        }