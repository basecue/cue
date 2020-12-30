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

    class Subscriber:
        subscribers = SimpleNamespace(
            on_event_staticmethod=[],
        )

        @subscribe.before(Klass.event_staticmethod)
        @staticmethod
        def on_event_staticmethod(instance_cls: Type[Klass], text: str,
            flag: bool = True):
            Subscriber.subscribers.on_event_staticmethod.append(
                (instance_cls, text, flag))

    return Klass, Subscriber


def test_instance_event_staticmethod(setup):
    Klass, Subscriber = setup
    instance = Klass()
    instance_2 = Klass()

    return_value_instance = instance.event_staticmethod('text', flag=False)
    return_value_instance_2 = instance_2.event_staticmethod('text_2', flag=True)

    assert return_value_instance == ("text", False)
    assert return_value_instance_2 == ("text_2", True)

    assert Subscriber.subscribers.on_event_staticmethod == [
        (Klass, 'text', False),
        (Klass, 'text_2', True)
    ]


def test_class_event_staticmethod(setup):
    Klass, Subscriber = setup
    instance = Klass()
    instance_2 = Klass()

    return_value_instance = Klass.event_staticmethod('text', flag=False)
    return_value_instance_2 = Klass.event_staticmethod('text_2', flag=True)

    assert return_value_instance == ("text", False)
    assert return_value_instance_2 == ("text_2", True)

    assert Subscriber.subscribers.on_event_staticmethod == [
        (Klass, 'text', False),
        (Klass, 'text_2', True)
    ]


def test_instance_event_staticmethod_subscriber_instance(setup):
    Klass, Subscriber = setup
    instance = Klass()
    instance_2 = Klass()

    subscriber = Subscriber()
    subscriber_2 = Subscriber()

    return_value_instance = instance.event_staticmethod('text', flag=False)
    return_value_instance_2 = instance_2.event_staticmethod('text_2', flag=True)

    assert return_value_instance == ("text", False)
    assert return_value_instance_2 == ("text_2", True)

    assert Subscriber.subscribers.on_event_staticmethod == [
        (Klass, 'text', False),
        (Klass, 'text_2', True)
    ]


def test_class_event_staticmethod_subscriber_instance(setup):
    Klass, Subscriber = setup
    instance = Klass()
    instance_2 = Klass()

    subscriber = Subscriber()
    subscriber_2 = Subscriber()

    return_value_instance = Klass.event_staticmethod('text', flag=False)
    return_value_instance_2 = Klass.event_staticmethod('text_2', flag=True)

    assert return_value_instance == ("text", False)
    assert return_value_instance_2 == ("text_2", True)

    assert Subscriber.subscribers.on_event_staticmethod == [
        (Klass, 'text', False),
        (Klass, 'text_2', True)
    ]
