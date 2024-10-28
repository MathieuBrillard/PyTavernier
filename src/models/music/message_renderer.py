from discord import Embed


class MessageRenderer:
    @staticmethod
    def add_song(
        title: str,
        title_url: str,
        uploader: str,
        uploader_url: str,
        thumbnail: str,
        duration: str,
    ):
        return Embed(
            color="cf00ff",
            description=f"***[{uploader}]({uploader_url})***\n**[{title}]({title_url})** `[{duration}]`",
            thumbnail=thumbnail,
        )

    @staticmethod
    def play_song(
        title: str,
        title_url: str,
        uploader: str,
        uploader_url: str,
        thumbnail: str,
        duration: str,
    ):
        return Embed(color="cf00ff", description="")
