from yt_dlp import YoutubeDL
from ytsearch import YTSearch

from lib.logger import _LOGGER
from models.errors.music import NoSongFound

# Download audio info and create a stream
YTDLP_OPTS = {"format": "bestaudio/best", "noplaylist": False, "quiet": True}


class SongExtractor:
    @staticmethod
    def _search_title(title: str) -> dict:
        _LOGGER.info(f"title is: '{title}'")
        songs = YTSearch().search_by_term(term=title, max_results=1)
        if songs is None:
            raise NoSongFound(f"No song were found for the query '{title}'.")
        else:
            url = "https://www.youtube.com/watch?v=" + songs[0]["id"]
            return SongExtractor._search_url(url)

    @staticmethod
    def _search_url(url: str) -> dict:
        with YoutubeDL(YTDLP_OPTS) as ydl:
            info = ydl.extract_info(url, download=False)
            if "entries" in info.keys():
                _LOGGER.debug("Play list detected, handling ...")
            return info

    @staticmethod
    def search(url_or_title: str) -> dict:
        if "http://" in url_or_title or "https://" in url_or_title:
            return SongExtractor._search_url(url_or_title)
        else:
            return SongExtractor._search_title(url_or_title)
