from types import SimpleNamespace

import pytest

from cue import publisher, subscribe


@pytest.fixture
def setup():
    class Klass:
        @publisher
        def event(self, text: str, flag: bool = True):
            return self, text, flag

    class Subscriber:
        subscribers = SimpleNamespace(
            on_event_classmethod=[],
        )

        @subscribe(Klass.event)
        @classmethod
        def on_event_classmethod(cls, instance: Klass, text: str, flag: bool = True):
            cls.subscribers.on_event_classmethod.append((cls, instance, text, flag))

    return Klass, Subscriber


def test(setup):
    Klass, Subscriber = setup
    instance = Klass()
    instance_2 = Klass()

    return_value_instance = instance.event('text', flag=False)
    return_value_instance_2 = instance_2.event('text_2', flag=True)

    assert return_value_instance == (instance, "text", False)
    assert return_value_instance_2 == (instance_2, "text_2", True)

    assert Subscriber.subscribers.on_event_classmethod == [
        (Subscriber, instance, 'text', False),
        (Subscriber, instance_2, 'text_2', True)
    ]


def test_class_call(setup):
    Klass, Subscriber = setup
    instance = Klass()
    instance_2 = Klass()

    return_value_instance = Klass.event(instance, 'text', flag=False)
    return_value_instance_2 = Klass.event(instance_2, 'text_2', flag=True)

    assert return_value_instance == (instance, "text", False)
    assert return_value_instance_2 == (instance_2, "text_2", True)

    assert Subscriber.subscribers.on_event_classmethod == [
        (Subscriber, instance, 'text', False),
        (Subscriber, instance_2, 'text_2', True)
    ]


def test_subscriber_instance(setup):
    Klass, Subscriber = setup
    instance = Klass()
    instance_2 = Klass()

    subscriber = Subscriber()
    subscriber_2 = Subscriber()

    return_value_instance = instance.event('text', flag=False)
    return_value_instance_2 = instance_2.event('text_2', flag=True)

    assert return_value_instance == (instance, "text", False)
    assert return_value_instance_2 == (instance_2, "text_2", True)

    assert Subscriber.subscribers.on_event_classmethod == [
        (Subscriber, instance, 'text', False),
        (Subscriber, instance_2, 'text_2', True)
    ]
