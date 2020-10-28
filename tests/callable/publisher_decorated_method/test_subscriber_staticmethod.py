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

        @publisher
        @classmethod
        def event_classmethod(cls, text: str, number: int, flag: bool = True):
            return text, number, flag

    class Klass(_Klass):
        pass

    class _Subscriber:
        subscribers = SimpleNamespace(
            on_event_staticmethod=[],
            on_event_classmethod=[],
        )

        @subscribe.before(Klass.event_staticmethod)
        @staticmethod
        def on_event_staticmethod(instance_cls: Type[Klass], text: str, flag: bool = True):
            Subscriber.subscribers.on_event_staticmethod.append((instance_cls, text, flag))

        @subscribe.before(Klass.event_classmethod)
        @staticmethod
        def on_event_classmethod(cls, instance_cls: Type[Klass], text: str, flag: bool = True):
            Subscriber.subscribers.on_event_classmethod.append((instance_cls, text, flag))

    class Subscriber(_Subscriber):
        pass

    return Klass, Subscriber


@pytest.mark.xfail
def test_event_staticmethod(setup):
    Klass, Subscriber = setup
    instance = Klass()
    instance_2 = Klass()

    return_value_instance = instance.event_staticmethod('text', flag=False)
    return_value_instance_2 = instance_2.event_staticmethod('text_2', flag=True)

    assert return_value_instance == ("text", False)
    assert return_value_instance_2 == ("text_2", True)

    assert Subscriber.subscribers.on_event_staticmethod == [
        (Klass, 'text', False),
        ( Klass, 'text_2', True)
    ]
    assert Subscriber.subscribers.on_event_classmethod == [
    ]

@pytest.mark.xfail
def test_event_staticmethod_subscriber_instance(setup):
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
    assert Subscriber.subscribers.on_event_classmethod == [
    ]


@pytest.mark.xfail
def test_event_classmethod(setup):
    Klass, Subscriber = setup
    instance = Klass()
    instance_2 = Klass()

    return_value_instance = instance.event_classmethod('text', flag=False)
    return_value_instance_2 = instance_2.event_classmethod('text_2', flag=True)

    assert return_value_instance == ("text", False)
    assert return_value_instance_2 == ("text_2", True)

    assert Subscriber.subscribers.on_event_staticmethod == [
    ]
    assert Subscriber.subscribers.on_event_classmethod == [
        (Klass, 'text', False),
        (Klass, 'text_2', True)
    ]


@pytest.mark.xfail
def test_event_classmethod_subscriber_instance(setup):
    Klass, Subscriber = setup
    instance = Klass()
    instance_2 = Klass()

    subscriber = Subscriber()
    subscriber_2 = Subscriber()

    return_value_instance = instance.event_classmethod('text', flag=False)
    return_value_instance_2 = instance_2.event_classmethod('text_2', flag=True)

    assert return_value_instance == ("text", False)
    assert return_value_instance_2 == ("text_2", True)

    assert Subscriber.subscribers.on_event_staticmethod == [
    ]
    assert Subscriber.subscribers.on_event_classmethod == [
        (Klass, 'text', False),
        (Klass, 'text_2', True)
    ]
