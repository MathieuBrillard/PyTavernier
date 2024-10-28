from asyncio import run
from typing import TYPE_CHECKING

from discord import FFmpegPCMAudio, VoiceClient

if TYPE_CHECKING:
    from discord.abc import MessageableChannel
    from models.music.queue_manager import QueueManager

from lib.logger import _LOGGER
from models.errors.music import NotConnectedToVoice
from models.music.song_extractor import SongExtractor

FFMPEG_OPTIONS = {"options": "-vn"}  # Audio-only options for ffmpeg

# Download audio info and create a stream
YTDLP_OPTS = {"format": "bestaudio/best", "noplaylist": True, "quiet": True}


class Queue:
    def __init__(
        self,
        manager: "QueueManager",
        connection: VoiceClient,
        interaction_chat: "MessageableChannel",
    ):
        self._manager = manager
        self._vc = connection
        self.interaction_chat = interaction_chat
        self._songs = []
        self._current_song = None
        self._previous_song = None
        self._next_event = False

    # TODO: ensure that connection is in the same channel that the song requester

    async def handle_next(self):
        self._next_event = True
        await self.playSong()

    def after(self, e: Exception = None):
        if e:
            _LOGGER.exception(
                "Client encountered an exception while playing the song:", e
            )
            try:
                run(self._manager.cleanup(self._vc, self._vc.guild.id))
            except Exception as err:
                _LOGGER.exception("Could not cleanup properly:", err)
        elif self._next_event is True:
            self._next_event = False
        else:
            run(self.playSong())

    async def check_connection(self) -> None:
        vc = self._vc
        guild = vc.guild
        _LOGGER.info(
            f"Client checking voice connection is up for guild: '{guild.name}'..."
        )
        if vc.is_connected() is False:
            _LOGGER.error("Client is not connected to voice channel.")
            await self._manager.cleanup(vc, guild.id)
            raise NotConnectedToVoice("Client must be connected to voice channel.")

    async def addSong(self, song) -> None:
        self._songs.append(song)
        await self.interaction_chat.send(f"Song {song['title']} was added to queue.")
        if self._vc.is_playing() is False:
            await self.playSong()

    async def playSong(self):
        await self.check_connection()
        if len(self._songs) < 1:  # Handle the end of the queue
            _LOGGER.info(
                f"Queue for guild: '{self._vc.guild.name}' is empty: cleaning up voice connection...'"
            )
            await self._manager.cleanup(self._vc, self._vc.guild.id)
        else:
            if self._vc.is_playing() is True:  # handle next command
                self._vc.stop()
            next_song = self._songs.pop()
            audio_url = next_song["url"]
            try:
                await self.interaction_chat.send(f"Now playing: {next_song['title']}")
                self._vc.play(
                    FFmpegPCMAudio(audio_url, **FFMPEG_OPTIONS),
                    after=self.after,
                    signal_type="music",
                )
            except Exception as e:
                _LOGGER.exception("Client could not play song correctly:", e)
            else:
                _LOGGER.success("Client started playing song successfully.")

    async def play(self, url_or_title: str) -> None:
        try:
            info = SongExtractor.search(url_or_title)
            await self.addSong(info)
        except Exception as e:
            _LOGGER.exception("Cannot retrieve song info from yt_dlp:", e)
        else:
            _LOGGER.success("Successfully retrieved song info.")
