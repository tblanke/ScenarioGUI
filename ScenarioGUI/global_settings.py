"""
global settings of scenario gui
"""
from __future__ import annotations

import logging
from configparser import ConfigParser
from pathlib import Path
from platform import system

path = Path(__file__).parent.absolute()
config = ConfigParser()


def get_path_for_file(start_path: Path, filename: str) -> Path:
    path_i = start_path
    for i in range(6):
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

FONT = "None"
FONT_SIZE = 6

FILE_EXTENSION: str = "nothing"
GUI_NAME: str = "None"
ICON_NAME: str = "icon"

# get current version
config.read(config.read(get_path_for_file(path, "setup.cfg").joinpath("setup.cfg")))
VERSION = config.get("metadata", "version")


def load(gui_file: str | Path):
    config.read(gui_file)

    global FOLDER
    global WHITE
    global LIGHT
    global LIGHT_SELECT
    global DARK
    global GREY
    global WARNING
    global BLACK
    global FONT
    global FONT_SIZE
    global FILE_EXTENSION
    global GUI_NAME
    global ICON_NAME
    global VERSION

    FOLDER = get_path_for_file(get_path_for_file(Path(gui_file).parent.parent, config['DEFAULT']["PATH_2_ICONS"]).joinpath(config['DEFAULT']["PATH_2_ICONS"]), "icons")

    config.read(config.read(get_path_for_file(Path(gui_file).parent.parent, "setup.cfg").joinpath("setup.cfg")))
    VERSION = config.get("metadata", "version")

    WHITE = config['COLORS']["WHITE"]
    LIGHT = config['COLORS']["LIGHT"]
    LIGHT_SELECT = config['COLORS']["LIGHT_SELECT"]
    DARK = config['COLORS']["DARK"]
    GREY = config['COLORS']["GREY"]
    WARNING = config['COLORS']["WARNING"]
    BLACK = config['COLORS']["BLACK"]

    FONT = config['DEFAULT']["FONT_WINDOWS"] if system() == "Windows" else config['DEFAULT']["FONT_MAC"]
    FONT_SIZE = int(config['DEFAULT']["FONT_SIZE_WINDOWS"] if system() == "Windows" else config['DEFAULT']["FONT_SIZE_MAC"])

    FILE_EXTENSION = config['DEFAULT']["FILE_EXTENSION"]
    GUI_NAME = config['DEFAULT']["GUI_NAME"]
    ICON_NAME = config['DEFAULT']["ICON_NAME"]


LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


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
