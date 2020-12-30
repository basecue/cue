from types import SimpleNamespace

import pytest

from cue import publisher, subscribe


@pytest.fixture
def setup():
    @publisher
    def event(text: str, flag: bool = True):
        return text, flag

    @publisher
    def event_2(text: str, number: int, flag: bool = True):
        return text, number, flag

    publishers = SimpleNamespace(event=event, event_2=event_2)

    subscribers = SimpleNamespace(
        on_event_before=[],
        on_event_after=[],
        on_event_2_before=[],
        on_event_2_after=[],
        on_both_events=[],
    )

    @subscribe.before(event)
    def on_event_before(text, flag: bool = True):
        subscribers.on_event_before.append((text, flag))

    @subscribe(event)
    def on_event_after(text, flag: bool = True):
        subscribers.on_event_after.append((text, flag))

    @subscribe.before(event_2)
    def on_event_2_before(text, number, flag: bool = True):
        subscribers.on_event_2_before.append((text, number, flag))

    @subscribe(event_2)
    def on_event_2_after(text, number, flag: bool = True):
        subscribers.on_event_2_after.append((text, number, flag))

    @subscribe.before(event)
    @subscribe.before(event_2)
    def on_both_events(*args, **kwargs):
        subscribers.on_both_events.append((args, kwargs))

    return publishers, subscribers


def test_event(setup):
    publishers, subscribers = setup
    return_value = publishers.event('text', flag=False)

    assert return_value == ("text", False)

    assert subscribers.on_event_before == [('text', False)]
    assert subscribers.on_event_after == [('text', False)]
    assert subscribers.on_event_2_before == []
    assert subscribers.on_event_2_after == []
    assert subscribers.on_both_events == [(('text',), {"flag": False})]


def test_event_2(setup):
    publishers, subscribers = setup
    return_value = publishers.event_2('text', 42, flag=False)

    assert return_value == ("text", 42, False)

    assert subscribers.on_event_before == []
    assert subscribers.on_event_after == []
    assert subscribers.on_event_2_before == [('text', 42, False)]
    assert subscribers.on_event_2_after == [('text', 42, False)]
    assert subscribers.on_both_events == [(('text', 42), {"flag": False})]
