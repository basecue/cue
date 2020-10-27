import dataclasses
from types import SimpleNamespace
from typing import Union

import pytest

from cue import publisher, subscribe


@pytest.fixture
def setup():
    @publisher
    @dataclasses.dataclass
    class Klass:
        text: str
        number: int

        def __post_init__(self):
            @subscribe.after(Klass.text)
            @subscribe.after(Klass.number)
            def _change(instance, *_args):
                instance.on_change()

        @publisher
        def on_change(self):
            pass

    subscribers = SimpleNamespace(
        on_change_text_after=[],
        on_change_text_before=[],
        on_change_both_before=[],
        on_change_before=[],
        on_change_after=[],
    )

    @subscribe.before(Klass.number)
    def on_change_text_before(instance: Klass, number):
        subscribers.on_change_text_before.append((instance, number))

    @subscribe.after(Klass.text)
    def on_change_text_after(instance: Klass, text):
        subscribers.on_change_text_after.append((instance, text))

    @subscribe.before(Klass.text)
    @subscribe.before(Klass.number)
    def on_change_both_before(instance: Klass, value: Union[str, int]):
        subscribers.on_change_both_before.append((instance, value))

    @subscribe.before(Klass.on_change)
    def on_change_before(instance):
        subscribers.on_change_both_before.append(instance)

    @subscribe.after(Klass.on_change)
    def on_change_after(instance):
        subscribers.on_change_after.append(instance)

    return Klass, subscribers


def test_event(setup):
    Klass, subscribers = setup

    instance = Klass(text="init", number=10)
    instance_2 = Klass(text="init_2", number=20)

    instance.text = "text"
    instance_2.text = "text_2"
    instance.number = 30
    instance_2.number = 40

    assert subscribers.on_change_text_before == [
        (instance, 'init'),
        (instance_2, 'init_2'),
        (instance, 'text'),
        (instance_2, 'text_2'),
    ]
    assert subscribers.on_change_text_after == [
        (instance, 'init'),
        (instance_2, 'init_2'),
        (instance, 'text'),
        (instance_2, 'text_2'),
    ]
    assert subscribers.on_change_both_before == [
        (instance, 'init'),
        (instance, 10),
        (instance_2, 'init_2'),
        (instance_2, 20),
        (instance, 'text'),
        (instance_2, 'text_2'),
        (instance, 30),
        (instance_2, 40),
    ]
    assert subscribers.on_change_before == [
        instance,
        instance,
        instance_2,
        instance_2,
        instance,
        instance_2,
        instance,
        instance_2,
    ]
    assert subscribers.on_change_after == [
        instance,
        instance,
        instance_2,
        instance_2,
        instance,
        instance_2,
        instance,
        instance_2,
    ]
