from .fixture import get_function_name as get_fixture_name, get_zopelayer_state
import inspect
import pytest
import unittest


def pytest_pycollect_makeitem(collector, name, obj):
    # this works because of two things:
    # * this plugin is called before the pytest unittest collector (if it
    #   wasn't, it wouldn't be called at all after the pytest collector has
    #   detected a unittest test case)
    # * usefixtures works in-place
    # * as long as we return None the original unittest collector is called
    try:
        isunit = issubclass(obj, unittest.TestCase)
    except TypeError:
        isunit = False
    if isunit and hasattr(obj, 'layer'):
        pytest.mark.usefixtures(get_fixture_name(obj.layer))(obj)


def pytest_runtest_teardown(item, nextitem):
    state = get_zopelayer_state(item.session)

    if hasattr(nextitem, 'cls') and hasattr(nextitem.cls, 'layer'):
        state.keep = state.current & set(inspect.getmro(nextitem.cls.layer))
    else:
        state.keep.clear()
