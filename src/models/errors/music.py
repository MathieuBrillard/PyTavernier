class NotConnectedToVoice(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class NoSongFound(Exception):
    def __init__(self, *args):
        super().__init__(*args)
