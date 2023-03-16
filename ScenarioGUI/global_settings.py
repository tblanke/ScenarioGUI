from __future__ import annotations

import logging
from configparser import ConfigParser
from pathlib import Path
from platform import system
from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from functools import partial
    from typing import Callable

    from .gui_classes.gui_data_storage import DataStorage

WHITE: str = "rgb(255, 255, 255)"
LIGHT: str = "rgb(84, 188, 235)"
LIGHT_SELECT: str = "rgb(42, 126, 179)"
DARK: str = "rgb(0, 64, 122)"
GREY: str = "rgb(100, 100, 100)"
WARNING: str = "rgb(255, 200, 87)"
BLACK: str = "rgb(0, 0, 0)"

FONT = "Arial" if system() == "Windows" else "Helvetica"  # Arial
FONT_SIZE = 11 if system() == "Windows" else 14

FOLDER: Path = Path(__file__).parent

# get current version
path = Path(FOLDER).parent
config = ConfigParser()
with open(path.joinpath("setup.cfg")) as file:
    config.read_file(file)
VERSION = config.get("metadata", "version")

FILE_EXTENSION: str = "scenario"
GUI_NAME: str = "Scenario GUI"
ICON_NAME: str = "icon.svg"

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


class ResultsClass(Protocol):
    """Testing"""

    def _to_dict(self) -> dict:
        """creates a dict from class data"""

    def _from_dict(self, dictionary: dict) -> None:
        """creates a class from dict data"""


def func(d_s: DataStorage) -> tuple[ResultsClass, Callable[[], None]]:
    """Example function"""


DATA_2_RESULTS_FUNCTION: Callable[
    [DataStorage],
    tuple[ResultsClass, partial[[], None]] | tuple[ResultsClass, Callable[[], None]],
] = func


def set_graph_layout() -> None:
    """
    This function sets the graph layout to the correct format when the GUI is used.

    Returns
    -------
    None
    """
    import matplotlib.pyplot as plt
    from matplotlib.colors import to_rgb
    from numpy import array, float64

    background_color: str = to_rgb(array(DARK.replace("rgb(", "").replace(")", "").split(","), dtype=float64) / 255)
    white_color: str = to_rgb(array(WHITE.replace("rgb(", "").replace(")", "").split(","), dtype=float64) / 255)
    # light_color: str = to_rgb(array(LIGHT.replace('rgb(', '').replace(')', '').split(','), dtype=float64) / 255)
    # bright_color: str = to_rgb(array(WARNING.replace('rgb(', '').replace(')', '').split(','), dtype=float64) / 255)
    plt.rcParams["axes.labelcolor"] = white_color
    plt.rcParams["xtick.color"] = white_color
    plt.rcParams["ytick.color"] = white_color

    plt.rc("figure")
    plt.rc("axes", edgecolor=white_color)
    plt.rcParams["figure.facecolor"] = background_color
