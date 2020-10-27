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

        _number: int = dataclasses.field(init=False, repr=False)

        @property
        def number(self) -> int:
            return self._number

        @number.setter  # FIXME is it publisher neccesary?
        def number(self, value) -> None:
            self._number = value

    subscribers = SimpleNamespace(
        on_change_number_before=[],
        on_change_number_after=[],
        on_change_both_before=[],
        on_change_both_after=[],
    )

    @subscribe.before(Klass.number)
    def on_change_number_before(instance: Klass, number: int) -> None:
        subscribers.on_change_number_before.append((instance, number))

    @subscribe.after(Klass.number)
    def on_change_number_after(instance: Klass, number: int) -> None:
        subscribers.on_change_number_after.append((instance, number))

    @subscribe.before(Klass.text)
    @subscribe.before(Klass.number)
    def on_change_both_before(instance: Klass, value: Union[str, int]) -> None:
        subscribers.on_change_both_before.append((instance, value))

    @subscribe.before(Klass.text)
    @subscribe.before(Klass.number)
    def on_change_both_after(instance: Klass, value: Union[str, int]) -> None:
        subscribers.on_change_both_after.append((instance, value))

    return Klass, subscribers


def test(setup):
    Klass, subscribers = setup

    instance = Klass(text="init", number=10)
    instance_2 = Klass(text="init_2", number=20)

    instance.text = "text"
    instance_2.text = "text_2"
    instance.number = 30
    instance_2.number = 40

    assert subscribers.on_change_number_before == [
        (instance, 10),
        (instance_2, 20),
        (instance, 30),
        (instance_2, 40),
    ]
    assert subscribers.on_change_number_after == [
        (instance, 10),
        (instance_2, 20),
        (instance, 30),
        (instance_2, 40),
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

    assert subscribers.on_change_both_after == [
        (instance, 'init'),
        (instance, 10),
        (instance_2, 'init_2'),
        (instance_2, 20),
        (instance, 'text'),
        (instance_2, 'text_2'),
        (instance, 30),
        (instance_2, 40),
    ]
