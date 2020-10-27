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

    class Subscriber:
        subscribers = SimpleNamespace(
            on_event_staticmethod_before=[],
            on_event_staticmethod_after_=[],
            on_event_classmethod_before=[],
            on_event_classmethod_after=[],
            on_both_events=[],
        )

        @subscribe.before(Klass.event_staticmethod)
        def on_event_staticmethod_before(self, instance_cls: Type[Klass], text: str, flag: bool = True):
            self.subscribers.on_event_staticmethod_before.append((self, instance_cls, text, flag))

        @subscribe.after(Klass.event_staticmethod)
        def on_event_staticmethod_after_(self, instance_cls: Type[Klass], text: str, flag: bool = True):
            self.subscribers.on_event_staticmethod_after_.append((self, instance_cls, text, flag))

        @subscribe.before(Klass.event_classmethod)
        def on_event_classmethod_before(self, instance_cls: Type[Klass], text: str,
            number: int,
            flag: bool = True):
            self.subscribers.on_event_classmethod_before.append(
                (self, instance_cls, text, number, flag)
            )

        @subscribe.after(Klass.event_classmethod)
        def on_event_classmethod_after(self, instance_cls: Type[Klass], text: str,
            number: int,
            flag: bool = True):
            self.subscribers.on_event_classmethod_after.append(
                (self, instance_cls, text, number, flag)
            )

        @subscribe.before(Klass.event_staticmethod)
        @subscribe.before(Klass.event_classmethod)
        def on_both_events(self, instance_cls: Type[Klass], *args, **kwargs):
            self.subscribers.on_both_events.append((self, instance_cls, args, kwargs))

    return Klass, Subscriber


def test_event_staticmethod(setup):
    Klass, Subscriber = setup

    instance = Klass()
    instance_2 = Klass()

    subscriber = Subscriber()
    subscriber_2 = Subscriber()

    instance.event_staticmethod('text', flag=False)
    instance_2.event_staticmethod('text_2', flag=True)

    assert Subscriber.subscribers.on_event_staticmethod_before == [
        (subscriber, Klass, 'text', False),
        (subscriber_2, Klass, 'text', False),
        (subscriber, Klass, 'text_2', True),
        (subscriber_2, Klass, 'text_2', True),
    ]
    assert Subscriber.subscribers.on_event_staticmethod_after_ == [
        (subscriber, Klass, 'text', False),
        (subscriber_2, Klass, 'text', False),
        (subscriber, Klass, 'text_2', True),
        (subscriber_2, Klass, 'text_2', True),
    ]
    assert Subscriber.subscribers.on_event_classmethod_before == []
    assert Subscriber.subscribers.on_event_classmethod_after == []
    assert Subscriber.subscribers.on_both_events == [
        (subscriber, Klass, ('text',), {"flag": False}),
        (subscriber_2, Klass, ('text',), {"flag": False}),
        (subscriber, Klass, ('text_2',), {"flag": True}),
        (subscriber_2, Klass, ('text_2',), {"flag": True}),
    ]


def test_event_classmethod(setup):
    Klass, Subscriber = setup

    instance = Klass()
    instance_2 = Klass()

    subscriber = Subscriber()
    subscriber_2 = Subscriber()

    instance.event_classmethod('text', 10, flag=False)
    instance_2.event_classmethod('text_2', 20, flag=True)

    assert Subscriber.subscribers.on_event_staticmethod_before == []
    assert Subscriber.subscribers.on_event_staticmethod_after_ == []
    assert Subscriber.subscribers.on_event_classmethod_before == [
        (subscriber, Klass, 'text', 10, False),
        (subscriber_2, Klass, 'text', 10, False),
        (subscriber, Klass, 'text_2', 20, True),
        (subscriber_2, Klass, 'text_2', 20, True),
    ]
    assert Subscriber.subscribers.on_event_classmethod_after == [
        (subscriber, Klass, 'text', 10, False),
        (subscriber_2, Klass, 'text', 10, False),
        (subscriber, Klass, 'text_2', 20, True),
        (subscriber_2, Klass, 'text_2', 20, True),
    ]
    assert Subscriber.subscribers.on_both_events == [
        (subscriber, (Klass, 'text', 10), {"flag": False}),
        (subscriber_2, (Klass, 'text', 10), {"flag": False}),
        (subscriber, (Klass, 'text_2', 20), {"flag": True}),
        (subscriber_2, (Klass, 'text_2', 20), {"flag": True}),
    ]
