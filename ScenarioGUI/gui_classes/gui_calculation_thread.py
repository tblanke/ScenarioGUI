"""
This document contains all the code related to calculating the solution to the different
aims in the GUI.
"""
from __future__ import annotations

import multiprocessing as mp
from typing import TYPE_CHECKING

import PySide6.QtCore as QtC

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Callable
    from functools import partial

    import PySide6.QtWidgets as QtW

    from .gui_data_storage import DataStorage


class CalcProblem(QtC.QThread):
    """
    class to calculate the problem in an external thread
    """

    any_signal = QtC.Signal(tuple)
    role: int = 1

    def __init__(
        self,
        d_s: DataStorage,
        item: QtW.QListWidgetItem,
        parent=None,
        *,
        data_2_results_function: Callable[
            [DataStorage],
            tuple[object, partial[[], None]] | tuple[object, Callable[[], None]],
        ],
    ) -> None:
        """
        This function initialises the calculation class.

        Parameters
        ----------
        d_s : DataStorage
            DataStorage object with all the date to perform the calculation for
        idx : int
            Index of the current calculation thread
        parent :
            Parent class of the calculation problem
        data_2_results_function : Callable
            function to create the results class and a function to be called in the thread
        """
        super().__init__(parent)  # init parent class
        # set datastorage and index
        self.d_s = d_s
        self.item = item
        self.data_2_results_function = data_2_results_function
        self.calculated = False

    def run(self) -> None:
        """
        This function contains the actual code to run the different calculations.
        For each aim in the GUI, a new if statement is used. Here, one can put all the code
        needed to run the simulation/calculation with the all the functionalities of GHEtool.
        This function should return the DataStorage as a signal.

        Returns
        -------
        None
        """
        queue = mp.Queue()
        stop_event: mp.Event = mp.Event()
        process: mp.Process = mp.Process(target=calculate, args=(self.data_2_results_function, self.d_s, queue, stop_event))
        process.start()

        if not stop_event.wait(self.d_s.time_out):
            debug_message, results = f"{RuntimeError(f'RuntimeError: run time > {self.d_s.time_out}s')}", None
        else:
            debug_message, results = queue.get()
        process.terminate()
        self.d_s.debug_message = debug_message
        # save bore field in Datastorage
        self.d_s.results = results
        self.calculated = True
        self.item.setData(CalcProblem.role, self.d_s)
        # return Datastorage as signal
        self.any_signal.emit(self)


def calculate(data_2_results_function: Callable[[DataStorage], tuple[object, Callable]], d_s: DataStorage, queue: mp.Queue, stop_event: mp.Event) -> None:
    """
    This function contains the actual code to run the different calculations.
    For each aim in the GUI, a new if statement is used. Here, one can put all the code
    needed to run the simulation/calculation with the all the functionalities.
    This function should return the DataStorage as a signal.

    Returns
    -------
    None
    """

    try:
        results, func = data_2_results_function(d_s)
        func()
    except Exception as err:
        queue.put((err, None))
        return

    # set debug message to "" and save borefield in Datastorage
    queue.put(("", results))
    stop_event.set()
    return
