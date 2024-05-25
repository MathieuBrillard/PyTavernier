from sys import stdout
import logging
from colorlog import ColoredFormatter, escape_codes
import re

logger = logging.getLogger('TavernierLogger')
logging.addLevelName(1,'TRACE')
logger.setLevel(logging.DEBUG)


### Formatters ###
class TavernierColorFormatter(ColoredFormatter):
    ESC = escape_codes.escape_codes

    SPECIAL_CHARS = r'([\\/:|\[\]\(\),])' # \/:|[](),
    SPECIAL_COLOR = ESC["yellow"]

    LEVEL_COLORS = {
        'TRACE'   : (ESC['light_purple']),
        'DEBUG'   : (ESC['light_purple']),
        'INFO'    : (ESC['cyan']),
        'WARNING' : (ESC['light_yellow']),
        'ERROR'   : (ESC['red']),
        'CRITICAL': (ESC['fg_black'],ESC['bg_light_red']),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def color_str(self, input_str: str, regex: str, color: str) -> str:
        # Expression régulière pour trouver les séquences ANSI
        ansi_escape = re.compile(r'(\x1b\[\d*m|\x1b\[\d\;\d*m)')
        # Split l'input_str en parties, séparant les séquences ANSI des autres caractères
        parts = ansi_escape.split(input_str)
        current_color = ""
        result = []
        for part in parts:
            if ansi_escape.match(part):
                # Si la partie est une séquence ANSI, on l'ajoute telle quelle
                current_color = part
                result.append(part)
            else:
                # Sinon, on colorie les caractères spécifiques en jaune
                colored_part = re.sub(regex, f'{color}\\1{self.ESC["reset"]}{current_color}', part)
                result.append(colored_part)
        return ''.join(result)

    def format(self, record):
        message = super().format(record)
        # color special chars
        message = self.color_str(message, self.SPECIAL_CHARS, self.SPECIAL_COLOR)
        # color log levels
        for level, color in self.LEVEL_COLORS.items():
            if level in message:
                message = self.color_str(message, f'({level})', ''.join(color))
                message = message.replace(level, f'[{level}]') # add [] around levelname
        return message


console_format = TavernierColorFormatter(
    fmt='[%(blue)s%(asctime)s,%(msecs)03d%(reset)s] [%(blue)s%(module)s%(reset)s:%(light_yellow)s%(lineno)d%(reset)s] (%(blue)s%(funcName)s%(reset)s) %(levelname)-8s : %(message_log_color)s%(message)s',
    datefmt='%d/%m/%Y|%H:%M:%S',
    style='%',
    secondary_log_colors={
        'message': {
            'TRACE': 'light_blue',
            'DEBUG': 'light_purple',
            'INFO': 'cyan',
            'WARNING': 'light_yellow',
            'ERROR': 'red',
            'CRITICAL': 'red',
        },
    }
)
file_format = logging.Formatter(
    fmt='[%(asctime)s,%(msecs)03d] [%(module)s:%(lineno)d] (%(funcName)s) %(levelname)-10s : %(message)s',
    datefmt='%d/%m/%Y|%H:%M:%S',
    style='%',
)

### Handlers ###
console_handler = logging.StreamHandler(
    stream=stdout
)
all_handler = logging.FileHandler(
    filename='./logs/all.log',
    mode="a",
    encoding="utf-8",
    delay=False
)

LEVEL_HANDLERS_FILENAMES = [
    ('trace', 1),
    ('debug',logging.DEBUG),
    ('info', logging.INFO),
    ('warning', logging.WARNING),
    ('error', logging.ERROR),
    ('critical', logging.CRITICAL),
]
for filename,level in LEVEL_HANDLERS_FILENAMES:
    hd = logging.FileHandler(
        filename=f'./logs/{filename}.log',
        mode="a",
        encoding="utf-8",
        delay=False
    )
    hd.setLevel(level)
    hd.setFormatter(file_format)
    logger.addHandler(hd)

console_handler.setFormatter(console_format)
all_handler.setFormatter(file_format)
logger.addHandler(console_handler)
logger.addHandler(all_handler)
################

def log():
    logger.fatal("coucouuu")
    logger.error("coucouuu")
    logger.warning("coucouuu")
    logger.info("coucouuu")
    logger.debug("coucouuu")

if __name__ == "__main__":
    log()
