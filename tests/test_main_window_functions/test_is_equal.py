from ScenarioGUI.gui_classes.gui_data_storage import is_equal


def test_is_equal():
    assert is_equal(1, 1)
    assert not is_equal(1, 2)
    assert is_equal(1.2, 1.2)
    assert not is_equal(1.2, 1.3)
    assert is_equal("Hello", "Hello")
    assert not is_equal("Hello", "World")
    assert is_equal([1, 2, 3, 4], [1, 2, 3, 4])
    assert not is_equal([1, 2, 3, 4], [1, 2, 3])
    assert not is_equal([1, 2, 3, 4], [1, 2, 3, 5])
