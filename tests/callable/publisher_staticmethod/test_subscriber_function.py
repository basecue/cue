from types import SimpleNamespace
from typing import Type

import pytest

from cue import publisher, subscribe


@pytest.fixture
def setup():
    class _Klass:
        @publisher
        @staticmethod
        def event_staticmethod(text: str, flag: bool = True):
            return text, flag

    class Klass(_Klass):
        pass

    subscribers = SimpleNamespace(
        on_event_staticmethod_before=[],
        on_event_staticmethod_after_=[],
    )

    @subscribe.before(Klass.event_staticmethod)
    def on_event_staticmethod_before(
        instance_cls: Type[Klass],
        text: str,
        flag: bool = True
    ):
        subscribers.on_event_staticmethod_before.append((instance_cls, text, flag))

    @subscribe(Klass.event_staticmethod)
    def on_event_staticmethod_after_(instance_cls: Type[Klass], text: str,
        flag: bool = True):
        subscribers.on_event_staticmethod_after_.append((instance_cls, text, flag))

    # FIXME
    # @subscribe.before(Klass.event_staticmethod)
    # @subscribe.before(Klass.event_classmethod)
    # def on_both_events(instance_cls: Type[Klass], *args, **kwargs):
    #     subscribers.on_both_events.append((instance_cls, args, kwargs))

    return Klass, subscribers


def test_instance_event_staticmethod(setup):
    Klass, subscribers = setup

    instance = Klass()
    instance_2 = Klass()

    return_value_instance = instance.event_staticmethod('text', flag=False)
    return_value_instance_2 = instance_2.event_staticmethod('text_2', flag=True)

    assert return_value_instance == ("text", False)
    assert return_value_instance_2 == ("text_2", True)

    assert subscribers.on_event_staticmethod_before == [
        (Klass, 'text', False),
        (Klass, 'text_2', True),
    ]
    assert subscribers.on_event_staticmethod_after_ == [
        (Klass, 'text', False),
        (Klass, 'text_2', True),
    ]


def test_class_event_staticmethod(setup):
    Klass, subscribers = setup

    instance = Klass()
    instance_2 = Klass()

    return_value_instance = Klass.event_staticmethod('text', flag=False)
    return_value_instance_2 = Klass.event_staticmethod('text_2', flag=True)

    assert return_value_instance == ("text", False)
    assert return_value_instance_2 == ("text_2", True)

    assert subscribers.on_event_staticmethod_before == [
        (Klass, 'text', False),
        (Klass, 'text_2', True),
    ]
    assert subscribers.on_event_staticmethod_after_ == [
        (Klass, 'text', False),
        (Klass, 'text_2', True),
    ]
