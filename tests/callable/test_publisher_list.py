from types import SimpleNamespace

import pytest

from cue import publisher, subscribe


@pytest.fixture
def setup():
    class Klass(list):
        append = publisher(list.append)

    subscribers = SimpleNamespace(
        on_append=[],
    )

    @subscribe(Klass.append)
    def on_append(instance, item):
        subscribers.on_append.append((instance, item))

    return Klass, subscribers


def test(setup):
    Klass, subscribers = setup

    instance = Klass()
    instance_2 = Klass()

    instance.append('test')
    instance_2.append('test_2')

    assert instance[0] == 'test'
    assert instance_2[0] == 'test_2'
    assert subscribers.on_append == [
        (instance, 'test'),
        (instance_2, 'test_2'),
    ]
