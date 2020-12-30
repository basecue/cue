from types import SimpleNamespace

import pytest

from cue import publisher, subscribe


@pytest.fixture
def setup():
    class Klass:
        @publisher
        def __init__(self, text: str, flag: bool = True):
            self.text = text
            self.flag = flag

    subscribers = SimpleNamespace(
        on_init=[],
    )

    @subscribe(Klass.__init__)
    def on_init(instance, text, flag: bool = True):
        subscribers.on_init.append((instance, text, flag))

    return Klass, subscribers


def test(setup):
    Klass, subscribers = setup

    instance = Klass('test', False)
    instance_2 = Klass('test_2', True)

    assert instance.text == 'test'
    assert instance.flag is False

    assert instance_2.text == 'test_2'
    assert instance_2.flag is True
    assert subscribers.on_init == [
        (instance, 'test', False),
        (instance_2, 'test_2', True),
    ]
