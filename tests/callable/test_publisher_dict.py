from types import SimpleNamespace

import pytest

from cue import publisher, subscribe


@pytest.fixture
def setup():
    class Klass(dict):
        __setitem__ = publisher(dict.__setitem__)

    subscribers = SimpleNamespace(
        on_setitem=[],
    )

    @subscribe(Klass.__setitem__)
    def on_setitem(instance, key, value):
        subscribers.on_setitem.append((instance, key, value))

    return Klass, subscribers


def test(setup):
    Klass, subscribers = setup

    instance = Klass()
    instance_2 = Klass()

    instance['test'] = 10
    instance_2['test_2'] = 20

    assert instance['test'] == 10
    assert instance_2['test_2'] == 20
    assert subscribers.on_setitem == [
        (instance, 'test', 10),
        (instance_2, 'test_2', 20),
    ]
