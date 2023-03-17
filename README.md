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

The GUI can be customized using the global setting. There the font and font size can be set. Furthermore, the gui name, icon, version, saving file extension  
can be set. Several 
colors like the DARK background and the LIGHT Foreground color can be set as well. A folder containing an icons folder can be given. This one needs to 
contain at least the icon contained under ScenarioGUI/icons. Besides a results creating class and a data 2 results function needs to be specified. They will 
be explained in more detail later.

```Python
import ScenarioGUI.global_settings as global_vars
from pathlib import Path
global_vars.FONT = "Arial"
global_vars.FONT_SIZE = 12
global_vars.GUI_NAME = "My GUI name"
global_vars.ICON_NAME = "icon"
global_vars.VERSION = "0.2.0"
global_vars.FILE_EXTENSION = "tool"
global_vars.DARK = "rgb(0,0,0)"
global_vars.LIGHT = "rgb(255,204,0)"
folder = Path("__file__").parent
global_vars.FOLDER = folder
global_vars.ResultsClass = ResultsClass
global_vars.DATA_2_RESULTS_FUNCTION = data_2_results 
```

To create your own GUI part you can inherit from the GuiStructure provided by this lib and add more pages, categories and input field as you like.

```Python
from ScenarioGUI.gui_classes.gui_structure import GuiStructure
from ScenarioGUI.gui_classes.gui_structure_classes import (
    Aim,
    ButtonBox,
    Category,
    FigureOption,
    FileNameBox,
    FloatBox,
    FunctionButton,
    Hint,
    IntBox,
    ListBox,
    Page,
    ResultFigure,
    ResultText,
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import PySide6.QtWidgets as QtW
    from examples.translation_class import Translations

class GUI(GuiStructure):
    """your own customized GUI"""
    def __init__(self, default_parent: QtW.QWidget, translations: Translations):
        # first init the parent clas
        super().__init__(default_parent, translations)
        # add a first page called "Inputs" and has a button name of "Input" and has an icon "Add.svg"
        self.page_inputs = Page(name="Inputs", button_name="Input", icon="Add.svg")
        # Then several aims can be added to the page with different names and icons
        self.aim_add = Aim(label="Adding", icon="Add", page=self.page_inputs)
        self.aim_sub = Aim(label="Substract", icon="Delete", page=self.page_inputs)
        self.aim_plot = Aim(label="Plot", icon="Parameters", page=self.page_inputs)
        # a category with the label "Inputs" can be added to the inputs page like:
        self.category_inputs = Category(label="Inputs", page=self.page_inputs)
        # an integer box can be added with different options like this (some of these options are optional):
        self.int_a = IntBox(label="a",default_value=2,minimal_value=0,maximal_value=200,step=2,category=self.category_inputs)
        # a float box can be added with different options like this (some of these options are optional):
        self.float_b = FloatBox(
            label="b",
            default_value=100,
            minimal_value=0,
            maximal_value=1000,
            decimal_number=2,
            step=0.5,
            category=self.category_inputs,
        )
        # a button box can be added with different options like this
        self.button_box = ButtonBox(label="a or b?", default_index=0, entries=["a", "b"], category=self.category_inputs)
        # the button box can also be a list box for many options
        self.list_box = ListBox(label="a or b?", default_index=0, entries=["a", "b"], category=self.category_inputs)
        # a filename box can be added with different options like this
        file = "./example_data.csv"
        self.filename = FileNameBox(label="Filename", default_value=file, dialog_text="Hello", error_text="no file found", category=self.category_inputs)
        # a function button can be implemented like this:
        self.function_button = FunctionButton(button_text="function", icon="Add", category=self.category_inputs)
        # the function ("func") which will be called every time the button is clicked can be defined as follows:
        self.page_inputs.add_function_called_if_button_clicked(func)

        self.category_grid = Category(page=self.page_inputs, label="Grid")
        self.category_grid.activate_grid_layout(3)
        self.hint_1 = Hint(category=self.category_grid, hint="Grid example")
        # int boxes and float boxes with no label are displayed small in a grid layout
        self.int_small_1 = IntBox(
            label="",
            default_value=2,
            minimal_value=0,
            maximal_value=200,
            category=self.category_grid,
        )
        # int boxes and float boxes with no label are displayed small in a grid layout
        self.float_small_1 = FloatBox(
            label="",
            default_value=2,
            minimal_value=0,
            maximal_value=200,
            decimal_number=2,
            category=self.category_grid,
        )
        self.hint_2 = Hint(category=self.category_grid, hint="Grid example")
        # int boxes and float boxes with no label are displayed small in a grid layout
        self.int_small_2 = IntBox(
            label="",
            default_value=2,
            minimal_value=0,
            maximal_value=200,
            category=self.category_grid,
        )
        # int boxes and float boxes with no label are displayed small in a grid layout
        self.float_small_2 = FloatBox(
            label="",
            default_value=2,
            minimal_value=0,
            maximal_value=200,
            decimal_number=2,
            category=self.category_grid,
        )
        self.category_grid.activate_graphic_left()
        self.category_grid.activate_graphic_right()

        self.create_results_page()
        self.numerical_results = Category(page=self.page_result, label="Numerical results")

        self.result_text_add = ResultText("Result", category=self.numerical_results, prefix="Result: ", suffix="m")
        self.result_text_add.text_to_be_shown("ResultsClass", "get_result")
        self.result_text_add.function_to_convert_to_text(lambda x: round(x, 2))
        self.result_text_sub = ResultText("Result", category=self.numerical_results, prefix="Result: ", suffix="m")
        self.result_text_sub.text_to_be_shown("ResultsClass", "result")
        self.result_text_sub.function_to_convert_to_text(lambda x: round(x, 2))

        self.figure_results = ResultFigure(label="Plot", page=self.page_result)
        self.legend_figure_results = FigureOption(
            category=self.figure_results, label="Legend on", param="legend", default=0, entries=["No", "Yes"], entries_values=[False, True]
        )

        self.figure_results.fig_to_be_shown(class_name="ResultsClass", function_name="create_plot")

        self.aim_add.add_link_2_show(self.result_text_add)
        self.aim_sub.add_link_2_show(self.result_text_sub)
        self.aim_plot.add_link_2_show(self.figure_results)

        self.create_settings_page()
        self.create_lists()
        self.page_inputs.set_next_page(self.page_result)
        self.page_result.set_previous_page(self.page_inputs)
        self.page_result.set_next_page(self.page_settings)
        self.page_result.set_previous_page(self.page_result)
```

A full list of functionalities is given below.

## Functionalities
ScenarioGUI offers functionalities of value to all different disciplines which would like to create a GUI for different scenarios. These scenario can thern 
be easily compared. 
For more information about the functionalities of ScenarioGUI, please visit the [ReadTheDocs](https://scenariogui.readthedocs.org).

## License

*ScenarioGUI* is licensed under the terms of the 3-clause BSD-license.
See [ScenarioGUI license](LICENSE).

## Contact ScenarioGUI
- Do you want to contribute to ScenarioGUI?
- Do you have a great idea for a new feature?
- Do you have a specific remark/problem?

Please do contact us at [blanke@fh-aachen.de](mailto:blanke@fh-aachen.de).