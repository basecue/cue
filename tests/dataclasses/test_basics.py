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

    subscribers = SimpleNamespace(
        on_change_before_text=[],
        on_change_after_text=[],
        on_change_before_flag=[],
        on_change_after_flag=[],
        on_change_before=[],
        on_change_after=[]
    )

    @subscribe.before(Klass.text)
    def on_change_before_text(instance: Klass, number: int):
        subscribers.on_change_before_text.append((instance, number))

    @subscribe(Klass.text)
    def on_change_after_text(instance: Klass, number: int):
        subscribers.on_change_after_text.append((instance, number))

    @subscribe.before(Klass.number)
    def on_change_before_flag(instance: Klass, number: int):
        subscribers.on_change_before_flag.append((instance, number))

    @subscribe(Klass.number)
    def on_change_after_flag(instance: Klass, number: int):
        subscribers.on_change_after_flag.append((instance, number))

    @subscribe.before(Klass.text)
    @subscribe.before(Klass.number)
    def on_change_before(instance: Klass, value: Union[str, int]):
        subscribers.on_change_before.append((instance, value))

    @subscribe(Klass.text)
    @subscribe(Klass.number)
    def on_change_after(instance: Klass, value: Union[str, int]):
        subscribers.on_change_after.append((instance, value))

    return Klass, subscribers


def test(setup):
    Klass, subscribers = setup
    instance = Klass(text="init", number=10)
    instance_2 = Klass(text="init_2", number=20)

    instance.text = "text"
    instance_2.text = "text_2"
    instance.number = 30
    instance_2.number = 40

    assert instance.text == "text"
    assert instance_2.text == "text_2"
    assert instance.number == 30
    assert instance_2.number == 40

    assert subscribers.on_change_before_text == [
        (instance, 'text'),
        (instance_2, 'text_2'),
    ]
    assert subscribers.on_change_after_text == [
        (instance, 'text'),
        (instance_2, 'text_2'),
    ]
    assert subscribers.on_change_before_flag == [
        (instance, 30),
        (instance_2, 40),
    ]
    assert subscribers.on_change_after_flag == [
        (instance, 30),
        (instance_2, 40),
    ]
    assert subscribers.on_change_before == [
        (instance, 'text'),
        (instance_2, 'text_2'),
        (instance, 30),
        (instance_2, 40),
    ]
    assert subscribers.on_change_after == [
        (instance, 'text'),
        (instance_2, 'text_2'),
        (instance, 30),
        (instance_2, 40),
    ]
