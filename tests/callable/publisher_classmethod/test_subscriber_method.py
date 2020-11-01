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

    class Subscriber:
        subscribers = SimpleNamespace(
            on_event_classmethod_before=[],
            on_event_classmethod_after=[],
        )

        @subscribe.before(Klass.event_classmethod)
        def on_event_classmethod_before(self, instance_cls: Type[Klass], text: str,
            flag: bool = True):
            self.subscribers.on_event_classmethod_before.append(
                (self, instance_cls, text, flag)
            )

        @subscribe(Klass.event_classmethod)
        def on_event_classmethod_after(self, instance_cls: Type[Klass], text: str,
            flag: bool = True):
            self.subscribers.on_event_classmethod_after.append(
                (self, instance_cls, text, flag)
            )
        # FIXME
        # @subscribe.before(Klass.event_staticmethod)
        # @subscribe.before(Klass.event_classmethod)
        # def on_both_events(self, instance_cls: Type[Klass], *args, **kwargs):
        #     self.subscribers.on_both_events.append((self, instance_cls, args, kwargs))

    return Klass, Subscriber


def test_instance_event_classmethod(setup):
    Klass, Subscriber = setup

    instance = Klass()
    instance_2 = Klass()

    subscriber = Subscriber()
    subscriber_2 = Subscriber()

    return_value_instance = instance.event_classmethod('text', flag=False)
    return_value_instance_2 = instance_2.event_classmethod('text_2', flag=True)

    assert return_value_instance == (Klass, "text", False)
    assert return_value_instance_2 == (Klass, "text_2", True)

    assert Subscriber.subscribers.on_event_classmethod_before == [
        (subscriber, Klass, 'text', False),
        (subscriber_2, Klass, 'text', False),
        (subscriber, Klass, 'text_2', True),
        (subscriber_2, Klass, 'text_2', True),
    ]
    assert Subscriber.subscribers.on_event_classmethod_after == [
        (subscriber, Klass, 'text', False),
        (subscriber_2, Klass, 'text', False),
        (subscriber, Klass, 'text_2', True),
        (subscriber_2, Klass, 'text_2', True),
    ]
    # assert Subscriber.subscribers.on_both_events == [
    #     (subscriber, (Klass, 'text'), {"flag": False}),
    #     (subscriber_2, (Klass, 'text'), {"flag": False}),
    #     (subscriber, (Klass, 'text_2'), {"flag": True}),
    #     (subscriber_2, (Klass, 'text_2'), {"flag": True}),
    # ]


def test_class_event_classmethod(setup):
    Klass, Subscriber = setup

    instance = Klass()
    instance_2 = Klass()

    subscriber = Subscriber()
    subscriber_2 = Subscriber()

    return_value_instance = Klass.event_classmethod('text', flag=False)
    return_value_instance_2 = Klass.event_classmethod('text_2', flag=True)

    assert return_value_instance == (Klass, "text", False)
    assert return_value_instance_2 == (Klass, "text_2", True)

    assert Subscriber.subscribers.on_event_classmethod_before == [
        (subscriber, Klass, 'text', False),
        (subscriber_2, Klass, 'text', False),
        (subscriber, Klass, 'text_2', True),
        (subscriber_2, Klass, 'text_2', True),
    ]
    assert Subscriber.subscribers.on_event_classmethod_after == [
        (subscriber, Klass, 'text', False),
        (subscriber_2, Klass, 'text', False),
        (subscriber, Klass, 'text_2', True),
        (subscriber_2, Klass, 'text_2', True),
    ]
    # assert Subscriber.subscribers.on_both_events == [
    #     (subscriber, (Klass, 'text'), {"flag": False}),
    #     (subscriber_2, (Klass, 'text'), {"flag": False}),
    #     (subscriber, (Klass, 'text_2'), {"flag": True}),
    #     (subscriber_2, (Klass, 'text_2'), {"flag": True}),
    # ]
