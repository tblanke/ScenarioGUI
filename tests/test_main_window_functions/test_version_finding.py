import os
import shutil
from pathlib import Path
from time import sleep

import ScenarioGUI.global_settings as globs
from configparser import ConfigParser

path = Path(__file__).parent.parent


def test_find_version():
    config = ConfigParser()
    shutil.copy(path.parent.joinpath("setup.cfg"), path.parent.joinpath("setup_new.cfg"))
    config.read(path.parent.joinpath("setup.cfg"))
    config.set("metadata", "version", "0.2.0")
    with open(path.parent.joinpath("setup.cfg"), "w") as file:
        config.write(file)
        file.close()

    sleep(1)
    assert "0.2.0" == globs.find_version(path)

    # 1. Create a new section with the desired name
    config["meta"] = {}

    # 2. Copy the key-value pairs from the old section to the new section
    for key, value in config["metadata"].items():
        config["meta"][key] = value

    # 3. Optionally, delete the old section if it's no longer needed
    config.remove_section("metadata")
    with open(path.parent.joinpath("setup.cfg"), "w") as file:
        config.write(file)

    # os.remove(path.parent.joinpath("setup.cfg"))
    sleep(1)
    assert "0.0.0" == globs.find_version(path)

    shutil.copy(path.parent.joinpath("setup_new.cfg"), path.parent.joinpath("setup.cfg"))

    os.remove(path.parent.joinpath("setup_new.cfg"))
