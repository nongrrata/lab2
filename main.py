from tests import set_units_info
import logging
import logging.handlers
from game_controller import GameController

def setup_logging():
    root = logging.getLogger()

    if root.handlers:
        return

    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(message)s",
        datefmt="%H:%M:%S",
    )

    file = logging.handlers.RotatingFileHandler(
        "game.log", maxBytes=1_000_000, backupCount=3, encoding="utf-8"
    )
    file.setFormatter(formatter)
    file.setLevel(logging.DEBUG)

    root.setLevel(logging.DEBUG)
    root.addHandler(file)


if __name__ == "__main__":
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.debug("Запуск...")

    set_units_info()
    game_controller = GameController()
    game_controller.run()