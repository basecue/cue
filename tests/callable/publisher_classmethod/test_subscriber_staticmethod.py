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
            return text, flag

    class Klass(_Klass):
        pass

    class Subscriber:
        subscribers = SimpleNamespace(
            on_event_classmethod=[],
        )

        @subscribe.before(Klass.event_classmethod)
        @staticmethod
        def on_event_classmethod(
            cls,
            instance_cls: Type[Klass],
            text: str,
            flag: bool = True
        ):
            Subscriber.subscribers.on_event_classmethod.append(
                (cls, instance_cls, text, flag)
            )

    return Klass, Subscriber


def test_instance_event_classmethod(setup):
    Klass, Subscriber = setup
    instance = Klass()
    instance_2 = Klass()

    return_value_instance = instance.event_classmethod('text', flag=False)
    return_value_instance_2 = instance_2.event_classmethod('text_2', flag=True)

    assert return_value_instance == ("text", False)
    assert return_value_instance_2 == ("text_2", True)

    assert Subscriber.subscribers.on_event_classmethod == [
        (Subscriber, Klass, 'text', False),
        (Subscriber, Klass, 'text_2', True)
    ]


def test_class_event_classmethod(setup):
    Klass, Subscriber = setup
    instance = Klass()
    instance_2 = Klass()

    return_value_instance = Klass.event_classmethod('text', flag=False)
    return_value_instance_2 = Klass.event_classmethod('text_2', flag=True)

    assert return_value_instance == ("text", False)
    assert return_value_instance_2 == ("text_2", True)

    assert Subscriber.subscribers.on_event_classmethod == [
        (Subscriber, Klass, 'text', False),
        (Subscriber, Klass, 'text_2', True)
    ]


def test_instance_event_classmethod_subscriber_instance(setup):
    Klass, Subscriber = setup
    instance = Klass()
    instance_2 = Klass()

    subscriber = Subscriber()
    subscriber_2 = Subscriber()

    return_value_instance = instance.event_classmethod('text', flag=False)
    return_value_instance_2 = instance_2.event_classmethod('text_2', flag=True)

    assert return_value_instance == ("text", False)
    assert return_value_instance_2 == ("text_2", True)

    assert Subscriber.subscribers.on_event_classmethod == [
        (Subscriber, Klass, 'text', False),
        (Subscriber, Klass, 'text_2', True)
    ]


def test_class_event_classmethod_subscriber_instance(setup):
    Klass, Subscriber = setup
    instance = Klass()
    instance_2 = Klass()

    subscriber = Subscriber()
    subscriber_2 = Subscriber()

    return_value_instance = instance.event_classmethod('text', flag=False)
    return_value_instance_2 = instance_2.event_classmethod('text_2', flag=True)

    assert return_value_instance == ("text", False)
    assert return_value_instance_2 == ("text_2", True)

    assert Subscriber.subscribers.on_event_classmethod == [
        (Subscriber, Klass, 'text', False),
        (Subscriber, Klass, 'text_2', True)
    ]
