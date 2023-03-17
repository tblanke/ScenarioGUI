# ScenarioGUI: An open-source tool for an easy way to create graphical user interfaces

[![PyPI version](https://badge.fury.io/py/ScenarioGUI.svg)](https://badge.fury.io/py/ScenarioGUI)
[![Tests](https://github.com/tblanke/ScenarioGUI/actions/workflows/test.yml/badge.svg)](https://github.com/tblanke/ScenarioGUI/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/tblanke/ScenarioGUI/branch/main/graph/badge.svg?token=P7WX73BTVH)](https://codecov.io/gh/tblanke/ScenarioGUI)
[![Downloads](https://static.pepy.tech/personalized-badge/scenariogui?period=total&units=international_system&left_color=black&right_color=blue&left_text=Downloads)](https://pepy.tech/project/scenariogui)
[![Downloads](https://static.pepy.tech/personalized-badge/scenariogui?period=week&units=international_system&left_color=black&right_color=orange&left_text=Downloads%20last%20week)](https://pepy.tech/project/scenariogui)
[![Read the Docs](https://readthedocs.org/projects/scenariogui/badge/?version=stable)](https://scenariogui.readthedocs.io/en/stable/)

## What is *ScenarioGUI*?

<img src="https://raw.githubusercontent.com/tblanke/ScenarioGUI/main/ScenarioGUI/icons/icon.svg?token=GHSAT0AAAAAAB35NE3HTGDVH5ORMOVJSVC4ZAUOABA" width="110" align="left">

ScenarioGUI is a Python package that contains many functionalities to design your own Graphical User Interfaces (GUI). It should help to create and maintain 
scenario based GUIs.

#### Read The Docs
ScenarioGUI has an elaborate documentation were all the functionalities of the tool are explained, with examples.
This can be found on [ScenarioGUI.readthedocs.io](https://scenariogui.readthedocs.io).


## Requirements
This code is tested with Python 3.10 and 3.11 and requires the following libraries (the versions mentioned are the ones with which the code is tested)

* PySide6>=6.4.1
* matplotlib>=3.5.2
* numpy>=1.23.1
* pandas>=1.4.3
* black>=23.1.0

For the tests

* pytest>=7.1.2
* pytest-cov>=3.0.0
* pytest-timeout>=2.1.0
* pytest-qt>=4.1.0
* keyboard>=0.13.5

## Quick start
### Installation

One can install ScenarioGUI by running Pip and running the command

```
pip install ScenarioGUI
```

Developers can clone this repository.

It is a good practise to use virtual environments (venv) when working on a (new) Python project so different Python and package versions don't conflict with 
eachother. For ScenarioGUI, Python 3.10 or higher is recommended. General information about Python virtual environments can be found [here](https://docs.
Python.org/3.9/library/venv.html) and in [this article](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/).


### Get started with ScenarioGUI

To get started with ScenarioGUI, one needs to create a Borefield object. This is done in the following steps.

```Python
from ScenarioGUI import Borefield, GroundData
```

After importing the necessary classes, one sets all the relevant ground data and borehole equivalent resistance.

```Python
data = GroundData(3,   # ground thermal conductivity (W/mK)
                  10,  # initial/undisturbed ground temperature (deg C)
                  0.2, # borehole equivalent resistance (mK/W)
                  2.4*10**6) # volumetric heat capacity of the ground (J/m3K) 
```

Furthermore, one needs to set the peak and monthly baseload for both heating and cooling.

```Python
peak_cooling = [0., 0, 34., 69., 133., 187., 213., 240., 160., 37., 0., 0.]   # Peak cooling in kW
peak_heating = [160., 142, 102., 55., 0., 0., 0., 0., 40.4, 85., 119., 136.]  # Peak heating in kW

monthly_load_heating = [46500.0, 44400.0, 37500.0, 29700.0, 19200.0, 0.0, 0.0, 0.0, 18300.0, 26100.0, 35100.0, 43200.0]        # in kWh
monthly_load_cooling = [4000.0, 8000.0, 8000.0, 8000.0, 12000.0, 16000.0, 32000.0, 32000.0, 16000.0, 12000.0, 8000.0, 4000.0]  # in kWh
```

Next, one creates the borefield object in ScenarioGUI and sets the temperature constraints and the ground data.

```Python
# create the borefield object
borefield = Borefield(simulation_period=20,
                      peak_heating=peak_heating,
                      peak_cooling=peak_cooling,
                      baseload_heating=monthly_load_heating,
                      baseload_cooling=monthly_load_cooling)

borefield.set_ground_parameters(data)

# set temperature boundaries
borefield.set_max_ground_temperature(16)  # maximum temperature
borefield.set_min_ground_temperature(0)  # minimum temperature
```

```Python
# set a rectangular borefield
borefield.create_rectangular_borefield(10, 12, 6, 6, 110, 4, 0.075)
```

Note that the borefield can also be set using the pygfunction package.

```Python
import pygfunction as gt

# set a rectangular borefield
borefield_gt = gt.boreholes.rectangle_field(10, 12, 6, 6, 110, 1, 0.075) 
borefield.set_borefield(borefield_gt)
```

Once a Borefield object is created, one can make use of all the functionalities of ScenarioGUI. One can for example size the borefield using:

```Python
depth = borefield.size(100)
print("The borehole depth is: ", depth, "m")
```

Or one can plot the temperature profile by using

```Python
borefield.print_temperature_profile(legend=True)
```

A full list of functionalities is given below.

## Functionalities
ScenarioGUI offers functionalities of value to all different disciplines working with borefields. The features are available both in the code environment and in the GUI.
For more information about the functionalities of ScenarioGUI, please visit the [ReadTheDocs](https://scenariogui.readthedocs.org).

## License

*ScenarioGUI* is licensed under the terms of the 3-clause BSD-license.
See [ScenarioGUI license](LICENSE).

## Contact ScenarioGUI
- Do you want to contribute to ScenarioGUI?
- Do you have a great idea for a new feature?
- Do you have a specific remark/problem?

Please do contact us at [blanke@fh-aachen.de](mailto:blanke@fh-aachen.de).