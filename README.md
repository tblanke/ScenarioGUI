# ScenarioGUI: An open-source tool for an easy way to create graphical user interfaces

[![PyPI version](https://badge.fury.io/py/ScenarioGUI.svg)](https://badge.fury.io/py/ScenarioGUI)
[![Tests](https://github.com/tblanke/ScenarioGUI/actions/workflows/test.yml/badge.svg)](https://github.com/tblanke/ScenarioGUI/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/tblanke/ScenarioGUI/branch/main/graph/badge.svg?token=P7WX73BTVH)](https://codecov.io/gh/tblanke/ScenarioGUI)
[![Downloads](https://static.pepy.tech/personalized-badge/scenariogui?period=total&units=international_system&left_color=black&right_color=blue&left_text=Downloads)](https://pepy.tech/project/scenariogui)
[![Downloads](https://static.pepy.tech/personalized-badge/scenariogui?period=week&units=international_system&left_color=black&right_color=orange&left_text=Downloads%20last%20week)](https://pepy.tech/project/scenariogui)
[![Documentation Status](https://readthedocs.org/projects/scenariogui/badge/?version=latest)](https://scenariogui.readthedocs.io/en/latest/?badge=latest)

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

The GUI can be customized using a gui_config.ini file. There the font and font size can be set. Furthermore, the gui name, icon, version, saving file 
extension can be set. Several colors like the DARK background and the LIGHT Foreground color can be set as well. A folder containing an icons folder can be given. This one needs to 
contain at least the icon contained under ScenarioGUI/icons. 

```file
[COLORS]
WHITE: rgb(255, 255, 255)
LIGHT: rgb(84, 188, 235)
LIGHT_SELECT: rgb(42, 126, 179)
DARK: rgb(0, 64, 122)
GREY: rgb(100, 100, 100)
WARNING: rgb(255, 200, 87)
BLACK: rgb(0, 0, 0)

[DEFAULT]
FILE_EXTENSION: scenario
GUI_NAME: Scenario GUI
ICON_NAME: icon.svg
PATH_2_ICONS: ./ScenarioGUI/
FONT_WINDOWS: Arial
FONT_MAC: Helvetica
FONT_SIZE_WINDOWS: 12
FONT_SIZE_MAC: 14
```

To create your own GUI part you can inherit from the GuiStructure provided by this lib and add more pages, categories and input field as you like.

```Python
from ScenarioGUI import GuiStructure
from ScenarioGUI import elements as els
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
        self.page_inputs = els.Page(name="Inputs", button_name="Input", icon="Add.svg")
        # Then several aims can be added to the page with different names and icons
        self.aim_add = els.Aim(label="Adding", icon="Add", page=self.page_inputs)
        self.aim_sub = els.Aim(label="Substract", icon="Delete", page=self.page_inputs)
        self.aim_plot = els.Aim(label="Plot", icon="Parameters", page=self.page_inputs)
        # this three aims can appear in one row by setting:
        self.page_inputs.aims_in_row = 3
        # a category with the label "Inputs" can be added to the inputs page like:
        self.category_inputs = els.Category(label="Inputs", page=self.page_inputs)
        # an integer box can be added with different options like this (some of these options are optional):
        self.int_a = els.IntBox(label="a",default_value=2,minimal_value=0,maximal_value=200,step=2,category=self.category_inputs)
        # a float box can be added with different options like this (some of these options are optional):
        self.float_b = els.FloatBox(
            label="b",
            default_value=100,
            minimal_value=0,
            maximal_value=1000,
            decimal_number=2,
            step=0.5,
            category=self.category_inputs,
        )
        # a button box can be added with different options like this
        self.button_box = els.ButtonBox(label="a or b?", default_index=0, entries=["a", "b"], category=self.category_inputs)
        # the button box can also be a list box for many options
        self.list_box = els.ListBox(label="a or b?", default_index=0, entries=["a", "b"], category=self.category_inputs)
        # a filename box can be added with different options like this
        file = "./example_data.csv"
        self.filename = els.FileNameBox(label="Filename", default_value=file, dialog_text="Hello", error_text="no file found", category=self.category_inputs)
        # a function button can be implemented like this:
        self.function_button = els.FunctionButton(button_text="function", icon="Add", category=self.category_inputs)
        # the function ("func") which will be called every time the button is clicked can be defined as follows:
        self.page_inputs.add_function_called_if_button_clicked(func)
        # A Hint can be implemented (if warning is True the option is displayed in WARNING color) like:
        self.hint = els.Hint(hint="Very important hint", category=self.category_inputs, warning=False)
        # The results page must be created like this:
        self.create_results_page()
        # then a category for numerical results can be added
        self.numerical_results = els.Category(page=self.page_result, label="Numerical results")
        # A text result calling the get_results function from the ResultsClass and rounding it to 2 decimals can be set like this: 
        self.result_text_add = els.ResultText("Result", category=self.numerical_results, prefix="Result: ", suffix="m")
        self.result_text_add.text_to_be_shown("ResultsClass", "get_result")
        self.result_text_add.function_to_convert_to_text(lambda x: round(x, 2))
        # a results figure calling the create_plot function from ResultsClass which is returning a tuple of a plt.Figure and plt.Axes can be implemented 
        # like this:
        self.figure_results = els.ResultFigure(label="Plot", page=self.page_result)
        self.figure_results.fig_to_be_shown(class_name="ResultsClass", function_name="create_plot")
        # this figure can then be linked to an option to display the legend like this:
        self.legend_figure_results = els.FigureOption(
            category=self.figure_results, label="Legend on", param="legend", default=0, entries=["No", "Yes"], entries_values=[False, True]
        )        
        # with this function the results options will be displayed if one of the aims is selected
        self.aim_add.add_link_2_show(self.result_text_add)
        self.aim_plot.add_link_2_show(self.figure_results)
        # The settings page must be created like this:
        self.create_settings_page()
        # This function needs to be called to update the page, category and option lists
        self.create_lists()
        # links to next or previous pages can be set like this:
        self.page_inputs.set_next_page(self.page_result)
        self.page_result.set_previous_page(self.page_inputs)
        self.page_result.set_next_page(self.page_settings)
        self.page_result.set_previous_page(self.page_result)
```

The ResultsClass needs to have a "_to_dict", "_from_dict" and all function defined in the ResulText and ResultFigure options. Furthermore, it needs to be 
creatable without any inputs.

```Python
from collections.abc import Callable
import matplotlib.pyplot as plt

class ResultsClass:
    """Example results class"""
    def __init__(self, a: int = 1, b: int = 2):
        self.a = a
        self.b = b
        self.result = None

    def adding(self):
        """adding a and b"""
        self.result = self.a + self.b

    def get_result(self) -> float:
        """returns the result"""
        return self.result

    def create_plot(self, legend: bool = False) -> tuple[plt.Figure, plt.Axes]:
        """Creates a plot"""
        fig = plt.figure()
        ax = fig.add_subplot(111)
        # set axes labels
        ax.set_xlabel(r"Time (year)")
        ax.set_ylabel(r"Temperature ($^\circ C$)")
        ax.hlines(self.a, 0, self.b, colors="r", linestyles="dashed", label="line", lw=1)
        if legend:
            ax.legend()
        return fig, ax

    def _to_dict(self) -> dict:
        """creates a dictionary from the class variables"""
        return {"a": self.a, "b": self.b, "result": self.result}

    def _from_dict(self, dictionary: dict):
        """creates the class from a dictionary"""
        self.a = dictionary["a"]
        self.b = dictionary["b"]
        self.result = dictionary["result"]

def data_2_results(data) -> tuple[ResultsClass, Callable[[], None]]:
    """casts the data in the Datastorage to the results class and the function which should be called"""
    result = ResultsClass(data.int_a, data.float_b)
    return result, result.adding
```

The gui can then be start like this:

```Python
from sys import argv, exit as sys_exit

def run(path_list=None):  # pragma: no cover
    import PySide6.QtWidgets as QtW

    from ScenarioGUI.global_settings import FILE_EXTENSION
    from ScenarioGUI import MainWindow
    # import your own Translation class a script to create one from a csv file is given as well
    from ScenarioGUI.gui_classes.translation_class import Translations

    # init application
    app = QtW.QApplication()
    # init window
    window = QtW.QMainWindow()
    # init gui window
    main_window = MainWindow(window, app, GUI, Translations, result_creating_class=ResultsClass, data_2_results_function=data_2_results)
    # load file if it is in path list
    if path_list is not None:
        main_window.filename = (
            [path for path in path_list if path.endswith(f".{FILE_EXTENSION}")][0],
            0,
        )
        main_window.fun_load_known_filename()

    # show window
    window.showMaximized()
    # close app
    sys_exit(app.exec())


if __name__ == "__main__":  # pragma: no cover
    # pass system args like a file to read
    run(argv if len(argv) > 1 else None)
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