from types import SimpleNamespace

import pytest

from cue import publisher, subscribe


@pytest.fixture
def setup():
    class Klass:
        @publisher
        def event(self, text: str, flag: bool = True):
            pass

    class _Subscriber:
        subscribers = SimpleNamespace(
            on_event_staticmethod=[],
            on_event_classmethod=[],
        )

        @subscribe.before(Klass.event)
        @staticmethod
        def on_event_staticmethod(instance: Klass, text: str, flag: bool = True):
            Subscriber.subscribers.on_event_staticmethod.append((instance, text, flag))

        @subscribe.before(Klass.event)
        @classmethod
        def on_event_classmethod(cls, instance: Klass, text: str, flag: bool = True):
            cls.subscribers.on_event_staticmethod.append((cls, instance, text, flag))

    class Subscriber(_Subscriber):
        pass

    return Klass, Subscriber

@pytest.mark.xfail
def test(setup):
    Klass, Subscriber = setup
    instance = Klass()
    instance_2 = Klass()

    instance.event('text', flag=False)
    instance_2.event('text_2', flag=True)

    assert Subscriber.subscribers.on_event_staticmethod == [
        (instance, 'text', False),
        (instance_2, 'text_2', True)
    ]
    assert Subscriber.subscribers.on_event_classmethod == [
        (Subscriber, instance, 'text', False),
        (Subscriber, instance_2, 'text_2', True)
    ]


@pytest.mark.xfail
def test_class_call(setup):
    Klass, Subscriber = setup
    instance = Klass()
    instance_2 = Klass()

    Klass.event(instance, 'text', flag=False)
    Klass.event(instance_2, 'text_2', flag=True)

    assert Subscriber.subscribers.on_event_staticmethod == [
        (instance, 'text', False),
        (instance_2, 'text_2', True)
    ]
    assert Subscriber.subscribers.on_event_classmethod == [
        (Subscriber, instance, 'text', False),
        (Subscriber, instance_2, 'text_2', True)
    ]


@pytest.mark.xfail
def test_subscriber_instance(setup):
    Klass, Subscriber = setup
    instance = Klass()
    instance_2 = Klass()

    subscriber = Subscriber()
    subscriber_2 = Subscriber()

    instance.event('text', flag=False)
    instance_2.event('text_2', flag=True)

    assert Subscriber.subscribers.on_event_staticmethod == [
        (instance, 'text', False),
        (instance_2, 'text_2', True)
    ]
    assert Subscriber.subscribers.on_event_classmethod == [
        (Subscriber, instance, 'text', False),
        (Subscriber, instance_2, 'text_2', True)
    ]
