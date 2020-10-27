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
            pass

        @publisher
        @classmethod
        def event_classmethod(cls, text: str, number: int, flag: bool = True):
            pass

    class Klass(_Klass):
        pass

    subscribers = SimpleNamespace(
        on_event_staticmethod_before=[],
        on_event_staticmethod_after_=[],
        on_event_classmethod_before=[],
        on_event_classmethod_after=[],
        on_both_events=[],
    )

    @subscribe.before(Klass.event_staticmethod)
    def on_event_staticmethod_before(instance_cls: Type[Klass], text: str, flag: bool = True):
        subscribers.on_event_staticmethod_before.append((instance_cls, text, flag))

    @subscribe.after(Klass.event_staticmethod)
    def on_event_staticmethod_after_(instance_cls: Type[Klass], text: str, flag: bool = True):
        subscribers.on_event_staticmethod_after_.append((instance_cls, text, flag))

    @subscribe.before(Klass.event_classmethod)
    def on_event_classmethod_before(instance_cls: Type[Klass], text: str,
        number: int,
        flag: bool = True):
        subscribers.on_event_classmethod_before.append(
            (instance_cls, text, number, flag)
        )

    @subscribe.after(Klass.event_classmethod)
    def on_event_classmethod_after(instance_cls: Type[Klass], text: str,
        number: int,
        flag: bool = True):
        subscribers.on_event_classmethod_after.append(
            (instance_cls, text, number, flag)
        )

    @subscribe.before(Klass.event_staticmethod)
    @subscribe.before(Klass.event_classmethod)
    def on_both_events(instance_cls: Type[Klass], *args, **kwargs):
        subscribers.on_both_events.append((instance_cls, args, kwargs))

    return Klass, subscribers

@pytest.mark.xfail
def test_event_staticmethod(setup):
    Klass, subscribers = setup

    instance = Klass()
    instance_2 = Klass()


    instance.event_staticmethod('text', flag=False)
    instance_2.event_staticmethod('text_2', flag=True)

    assert subscribers.on_event_staticmethod_before == [
        (Klass, 'text', False),
        (Klass, 'text', False),
        (Klass, 'text_2', True),
        (Klass, 'text_2', True),
    ]
    assert subscribers.on_event_staticmethod_after_ == [
        (Klass, 'text', False),
        (Klass, 'text', False),
        (Klass, 'text_2', True),
        (Klass, 'text_2', True),
    ]
    assert subscribers.on_event_classmethod_before == []
    assert subscribers.on_event_classmethod_after == []
    assert subscribers.on_both_events == [
        ((Klass, 'text',), {"flag": False}),
        ((Klass, 'text',), {"flag": False}),
        ((Klass, 'text_2',), {"flag": True}),
        ((Klass, 'text_2',), {"flag": True}),
    ]

@pytest.mark.xfail
def test_event_classmethod(setup):
    Klass, subscribers = setup

    instance = Klass()
    instance_2 = Klass()

    instance.event_classmethod('text', 10, flag=False)
    instance_2.event_classmethod('text_2', 20, flag=True)

    assert subscribers.on_event_staticmethod_before == []
    assert subscribers.on_event_staticmethod_after_ == []
    assert subscribers.on_event_classmethod_before == [
        (Klass, 'text', 10, False),
        (Klass, 'text', 10, False),
        (Klass, 'text_2', 20, True),
        (Klass, 'text_2', 20, True),
    ]
    assert subscribers.on_event_classmethod_after == [
        (Klass, 'text', 10, False),
        (Klass, 'text', 10, False),
        (Klass, 'text_2', 20, True),
        (Klass, 'text_2', 20, True),
    ]
    assert subscribers.on_both_events == [
        (Klass, ('text', 10), {"flag": False}),
        (Klass, ('text', 10), {"flag": False}),
        (Klass, ('text_2', 20), {"flag": True}),
        (Klass, ('text_2', 20), {"flag": True}),
    ]
