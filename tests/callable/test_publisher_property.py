from types import SimpleNamespace

import pytest

from cue import publisher, subscribe


@pytest.fixture
def setup():
    class Klass:
        def __init__(self):
            self._number = 10

        @property
        def number(self):
            return self._number

        @publisher
        @number.setter
        def number(self, value):
            self._number = value

    subscribers = SimpleNamespace(
        on_number=[],
    )

    @subscribe(Klass.number)
    def on_number(instance, value):
        subscribers.on_number.append((instance, value))

    return Klass, subscribers


def test(setup):
    Klass, subscribers = setup

    instance = Klass()
    instance_2 = Klass()

    instance.number = 20
    instance_2.number = 30

    assert instance.number == 20
    assert instance_2.number == 30
    assert subscribers.on_number == [
        (instance, 20),
        (instance_2, 30),
    ]
