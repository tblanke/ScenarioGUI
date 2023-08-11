from typing import Callable


class Signal:
    def __init__(self):
        self.functions: list[Callable[[], None]] = []

    def emit(self, *args) -> None:
        """
        calls the stored functions

        Parameters
        ----------
        args: any
            ignored arguments

        Returns
        -------
            None
        """
        _ = [func() for func in self.functions]

    def connect(self, func: Callable[[], None]) -> None:
        """
        connects the function with the signal so every time a signal is emitted the function gets called

        Parameters
        ----------
        func: Callable[[], None]
            function to be called with no input or output

        Returns
        -------
            None
        """
        self.functions.append(func)
