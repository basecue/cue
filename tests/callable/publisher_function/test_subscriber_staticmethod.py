from types import SimpleNamespace

import pytest

from cue import publisher, subscribe


@pytest.fixture
def setup():
    @publisher
    def event(text: str, flag: bool = True):
        return text, flag

    class Subscriber:
        subscribers = SimpleNamespace(
            on_event_staticmethod=[],
        )

        @subscribe(event)
        @staticmethod
        def on_event_staticmethod(text: str, flag: bool = True):
            Subscriber.subscribers.on_event_staticmethod.append((text, flag))

    return event, Subscriber


def test(setup):
    event, Subscriber = setup
    return_value = event('text', flag=False)

    assert return_value == ("text", False)

    assert Subscriber.subscribers.on_event_staticmethod == [
        ('text', False)
    ]


def test_subscriber_instance(setup):
    event, Subscriber = setup

    subscriber = Subscriber()
    subscriber_2 = Subscriber()

    return_value = event('text', flag=False)

    assert return_value == ("text", False)

    assert Subscriber.subscribers.on_event_staticmethod == [
        ('text', False)
    ]
