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
            on_event_classmethod=[],
        )

        @subscribe(event)
        @classmethod
        def on_event_classmethod(cls, text: str, flag: bool = True):
            cls.subscribers.on_event_classmethod.append((cls, text, flag))

    return event, Subscriber


def test(setup):
    event, Subscriber = setup
    return_value = event('text', flag=False)

    assert return_value == ("text", False)

    assert Subscriber.subscribers.on_event_classmethod == [
        (Subscriber, 'text', False)
    ]


def test_subscriber_instance(setup):
    event, Subscriber = setup

    subscriber = Subscriber()
    subscriber_2 = Subscriber()

    return_value = event('text', flag=False)

    assert return_value == ("text", False)

    assert Subscriber.subscribers.on_event_classmethod == [
        (Subscriber, 'text', False)
    ]
