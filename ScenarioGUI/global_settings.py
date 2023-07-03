"""
global settings of scenario gui
"""
from __future__ import annotations

import logging
from configparser import ConfigParser
from pathlib import Path

path = Path(__file__).parent.absolute()
config = ConfigParser()


def get_path_for_file(start_path: Path, filename: str) -> Path:
    path_i = start_path.absolute()
    for _ in range(6):
        items = [item.parent for item in path_i.glob(f"**/{filename}")]
        if items:
            return items[0]
        path_i = path_i.parent
    raise FileNotFoundError


FOLDER: Path = Path("./icons")

WHITE: str = "rgb(0,0,0)"
LIGHT: str = "rgb(0,0,0)"
LIGHT_SELECT: str = "rgb(0,0,0)"
DARK: str = "rgb(0,0,0)"
GREY: str = "rgb(0,0,0)"
WARNING: str = "rgb(0,0,0)"
BLACK: str = "rgb(0,0,0)"

FONT = "Arial"
FONT_SIZE = 10

FILE_EXTENSION: str = "yourGUI"
GUI_NAME: str = "Your GUI Name"
ICON_NAME: str = "icon"

# get current version
try:
    config.read(config.read(get_path_for_file(path, "setup.cfg").joinpath("setup.cfg")))
    VERSION = config.get("metadata", "version")
except FileNotFoundError:  # pragma: no cover
    VERSION = "0.0.0"


LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
LOGGER.addHandler(console_handler)

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


def set_print_layout(ax) -> None:
    """
    This function sets the graph layout to the correct format when it is saved.

    Returns
    -------
    None
    """

    ax.spines['bottom'].set_color('black')
    ax.spines['top'].set_color('black')
    ax.spines['right'].set_color('black')
    ax.spines['left'].set_color('black')

    ax.tick_params(axis='x', colors='black')
    ax.tick_params(axis='y', colors='black')

    ax.xaxis.label.set_color('black')
    ax.yaxis.label.set_color('black')
