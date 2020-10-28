from types import SimpleNamespace

import pytest

from cue import publisher, subscribe


@pytest.fixture
def setup():
    @publisher
    def event(text: str, flag: bool = True):
        return text, flag

    class _Subscriber:
        subscribers = SimpleNamespace(
            on_event_staticmethod=[],
            on_event_classmethod=[],
        )

        @subscribe.before(event)
        @staticmethod
        def on_event_staticmethod(text: str, flag: bool = True):
            Subscriber.subscribers.on_event_staticmethod.append((text, flag))

        @subscribe.before(event)
        @classmethod
        def on_event_classmethod(cls, text: str, flag: bool = True):
            cls.subscribers.on_event_staticmethod.append((cls, text, flag))

    class Subscriber(_Subscriber):
        pass

    return event, Subscriber

@pytest.mark.xfail
def test(setup):
    event, Subscriber = setup
    return_value = event('text', flag=False)

    assert return_value == ("text", False)

    assert Subscriber.subscribers.on_event_staticmethod == [
        ('text', False)
    ]
    assert Subscriber.subscribers.on_event_classmethod == [
        (Subscriber, 'text', False)
    ]

@pytest.mark.xfail
def test_subscriber_instance(setup):
    event, Subscriber = setup

    subscriber = Subscriber()
    subscriber_2 = Subscriber()

    return_value = event('text', flag=False)

    assert return_value == ("text", False)

    assert Subscriber.subscribers.on_event_staticmethod == [
        ('text', False)
    ]
    assert Subscriber.subscribers.on_event_classmethod == [
        (Subscriber, 'text', False)
    ]
