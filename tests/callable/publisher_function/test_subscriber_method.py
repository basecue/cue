from types import SimpleNamespace

import pytest

from cue import publisher, subscribe


@pytest.fixture
def setup():
    @publisher
    def event(text: str, flag: bool = True):
        pass

    @publisher
    def event_2(text: str, number: int, flag: bool = True):
        pass

    publishers = SimpleNamespace(event=event, event_2=event_2)

    class Subscriber:
        subscribers = SimpleNamespace(
            on_event_before=[],
            on_event_after=[],
            on_event_2_before=[],
            on_event_2_after=[],
            on_both_events=[],
        )

        @subscribe.before(event)
        def on_event_before(self, text: str, flag: bool = True):
            self.subscribers.on_event_before.append((self, text, flag))

        @subscribe.after(event)
        def on_event_after(self, text: str, flag: bool = True):
            self.subscribers.on_event_after.append((self, text, flag))

        @subscribe.before(event_2)
        def on_event_2_before(self, text: str, number: int, flag: bool = True):
            self.subscribers.on_event_2_before.append((self, text, number, flag))

        @subscribe.after(event_2)
        def on_event_2_after(self, text: str, number: int, flag: bool = True):
            self.subscribers.on_event_2_after.append((self, text, number, flag))

        @subscribe.before(event)
        @subscribe.before(event_2)
        def on_both_events(self, *args, **kwargs):
            self.subscribers.on_both_events.append((self, args, kwargs))

    return publishers, Subscriber


def test_event(setup):
    publishers, Subscriber = setup
    subscriber = Subscriber()
    subscriber_2 = Subscriber()

    publishers.event('text', flag=False)

    assert Subscriber.subscribers.on_event_before == [
        (subscriber, 'text', False),
        (subscriber_2, 'text', False),
    ]
    assert Subscriber.subscribers.on_event_after == [
        (subscriber, 'text', False),
        (subscriber_2, 'text', False),
    ]
    assert Subscriber.subscribers.on_event_2_before == []
    assert Subscriber.subscribers.on_event_2_after == []
    assert Subscriber.subscribers.on_both_events == [
        (subscriber, ('text',), {"flag": False}),
        (subscriber_2, ('text',), {"flag": False}),
    ]


def test_event_2(setup):
    publishers, Subscriber = setup
    subscriber = Subscriber()
    subscriber_2 = Subscriber()

    publishers.event_2('text', 42, flag=False)

    assert Subscriber.subscribers.on_event_before == []
    assert Subscriber.subscribers.on_event_after == []
    assert Subscriber.subscribers.on_event_2_before == [
        (subscriber, 'text', 42, False),
        (subscriber_2, 'text', 42, False),
    ]
    assert Subscriber.subscribers.on_event_2_after == [
        (subscriber, 'text', 42, False),
        (subscriber_2, 'text', 42, False),
    ]
    assert Subscriber.subscribers.on_both_events == [
        (subscriber, ('text', 42), {"flag": False}),
        (subscriber_2, ('text', 42), {"flag": False}),
    ]
