import PySide6.QtCore as QtC
import PySide6.QtGui as QtG

from ..starting_closing_tests import close_tests, start_tests


def test_resize_event_button_sizes(qtbot):
    """
    test if the resize event is changing the button size

    Parameters
    ----------
    qtbot: qtbot
        bot for the GUI
    """
    # init gui window
    main_window = start_tests(qtbot)
    main_window.dia.setFixedSize(QtC.QSize(150, 150))
    main_window.resizeEvent(QtG.QResizeEvent(QtC.QSize(150, 150), QtC.QSize(1500, 1500)))
    assert main_window.size_b.height() < 48
    main_window.dia.setFixedSize(QtC.QSize(1500, 1500))
    main_window.resizeEvent(QtG.QResizeEvent(QtC.QSize(1500, 1500), QtC.QSize(150, 150)))
    assert main_window.size_push_s.height() == 75
    assert main_window.size_push_b.height() == 75
    assert main_window.size_b.height() == 48
    close_tests(main_window, qtbot)
