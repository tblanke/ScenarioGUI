from __future__ import annotations

from typing import TYPE_CHECKING

from .results_creation_class import ResultsClass

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Callable


def data_2_results(data) -> tuple[ResultsClass, Callable[[], None]]:  # pragma: no cover
    result = ResultsClass(data.int_a, data.float_b)
    return result, result.adding if data.aim_add else result.subtract
