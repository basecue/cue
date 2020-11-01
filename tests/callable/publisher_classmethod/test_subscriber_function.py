from types import SimpleNamespace
from typing import Type

import pytest

from cue import publisher, subscribe


@pytest.fixture
def setup():
    class _Klass:
        @publisher
        @classmethod
        def event_classmethod(cls, text: str, flag: bool = True):
            return cls, text, flag

    class Klass(_Klass):
        pass

    subscribers = SimpleNamespace(
        on_event_classmethod_before=[],
        on_event_classmethod_after=[],
    )

    @subscribe.before(Klass.event_classmethod)
    def on_event_classmethod_before(instance_cls: Type[Klass], text: str,
        flag: bool = True):
        subscribers.on_event_classmethod_before.append(
            (instance_cls, text, flag)
        )

    @subscribe(Klass.event_classmethod)
    def on_event_classmethod_after(instance_cls: Type[Klass], text: str,
        flag: bool = True):
        subscribers.on_event_classmethod_after.append(
            (instance_cls, text, flag)
        )

    # FIXME
    # @subscribe.before(Klass.event_staticmethod)
    # @subscribe.before(Klass.event_classmethod)
    # def on_both_events(instance_cls: Type[Klass], *args, **kwargs):
    #     subscribers.on_both_events.append((instance_cls, args, kwargs))

    return Klass, subscribers


def test_instance_event_classmethod(setup):
    Klass, subscribers = setup

    instance = Klass()
    instance_2 = Klass()

    return_value_instance = instance.event_classmethod('text', flag=False)
    return_value_instance_2 = instance_2.event_classmethod('text_2', flag=True)

    assert return_value_instance == (Klass, "text", False)
    assert return_value_instance_2 == (Klass, "text_2", True)

    assert subscribers.on_event_classmethod_before == [
        (Klass, 'text', False),
        (Klass, 'text_2', True),
    ]
    assert subscribers.on_event_classmethod_after == [
        (Klass, 'text', False),
        (Klass, 'text_2', True),
    ]
    # assert subscribers.on_both_events == [
    #     (Klass, ('text'), {"flag": False}),
    #     (Klass, ('text'), {"flag": False}),
    #     (Klass, ('text_2'), {"flag": True}),
    #     (Klass, ('text_2'), {"flag": True}),
    # ]


def test_class_event_classmethod(setup):
    Klass, subscribers = setup

    instance = Klass()
    instance_2 = Klass()

    return_value_instance = Klass.event_classmethod('text', flag=False)
    return_value_instance_2 = Klass.event_classmethod('text_2', flag=True)

    assert return_value_instance == (Klass, "text", False)
    assert return_value_instance_2 == (Klass, "text_2", True)

    assert subscribers.on_event_classmethod_before == [
        (Klass, 'text', False),
        (Klass, 'text_2', True),
    ]
    assert subscribers.on_event_classmethod_after == [
        (Klass, 'text', False),
        (Klass, 'text_2', True),
    ]
    # assert subscribers.on_both_events == [
    #     (Klass, ('text'), {"flag": False}),
    #     (Klass, ('text'), {"flag": False}),
    #     (Klass, ('text_2'), {"flag": True}),
    #     (Klass, ('text_2'), {"flag": True}),
    # ]
