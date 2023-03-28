"""
global settings of scenario gui
"""
from __future__ import annotations

import logging
from configparser import ConfigParser
from pathlib import Path
from platform import system

path = Path(".").absolute()
config = ConfigParser()


def get_path_for_file(start_path: Path, filename: str)-> Path:
    path_i = start_path
    for i in range(10):
        if path_i.joinpath(filename).exists():
            return path_i
        path_i = path_i.parent
    raise ValueError


config.read(get_path_for_file(path, "gui_config.ini").joinpath("gui_config.ini"))

FOLDER: Path = get_path_for_file(path.joinpath(config['DEFAULT']["PATH_2_ICONS"]), "icons")

WHITE: str = config['COLORS']["WHITE"]
LIGHT: str = config['COLORS']["LIGHT"]
LIGHT_SELECT: str = config['COLORS']["LIGHT_SELECT"]
DARK: str = config['COLORS']["DARK"]
GREY: str = config['COLORS']["GREY"]
WARNING: str = config['COLORS']["WARNING"]
BLACK: str = config['COLORS']["BLACK"]

FONT = config['DEFAULT']["FONT_WINDOWS"] if system() == "Windows" else config['DEFAULT']["FONT_MAC"]
FONT_SIZE = int(config['DEFAULT']["FONT_SIZE_WINDOWS"] if system() == "Windows" else config['DEFAULT']["FONT_SIZE_MAC"])

FILE_EXTENSION: str = config['DEFAULT']["FILE_EXTENSION"]
GUI_NAME: str = config['DEFAULT']["GUI_NAME"]
ICON_NAME: str = config['DEFAULT']["ICON_NAME"]

# get current version
config.read(config.read(get_path_for_file(path, "setup.cfg").joinpath("setup.cfg")))
VERSION = config.get("metadata", "version")

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
