from __future__ import annotations

from configparser import ConfigParser
from pathlib import Path
from platform import system

import ScenarioGUI.global_settings as globs


def load(gui_file: str | Path):
    config = ConfigParser()
    config.read(gui_file)

    globs.FOLDER = globs.get_path_for_file(
        globs.get_path_for_file(Path(gui_file).parent.parent, config["DEFAULT"]["PATH_2_ICONS"]).joinpath(config["DEFAULT"]["PATH_2_ICONS"]), "icons"
    )

    globs.WHITE = config["COLORS"]["WHITE"]
    globs.LIGHT = config["COLORS"]["LIGHT"]
    globs.LIGHT_SELECT = config["COLORS"]["LIGHT_SELECT"]
    globs.DARK = config["COLORS"]["DARK"]
    globs.GREY = config["COLORS"]["GREY"]
    globs.WARNING = config["COLORS"]["WARNING"]
    globs.BLACK = config["COLORS"]["BLACK"]

    globs.FONT = config["DEFAULT"]["FONT_WINDOWS"] if system() == "Windows" else config["DEFAULT"]["FONT_MAC"]
    globs.FONT_SIZE = int(config["DEFAULT"]["FONT_SIZE_WINDOWS"] if system() == "Windows" else config["DEFAULT"]["FONT_SIZE_MAC"])

    globs.FILE_EXTENSION = config["DEFAULT"]["FILE_EXTENSION"]
    globs.GUI_NAME = config["DEFAULT"]["GUI_NAME"]
    globs.ICON_NAME = config["DEFAULT"]["ICON_NAME"]
    try:
        globs.VERSION = config["DEFAULT"]["VERSION"]
    except KeyError:
        globs.VERSION = globs.find_version(globs.get_path_for_file(Path(gui_file).parent.parent, "setup.cfg"))

