from types import SimpleNamespace

import pytest

from cue import publisher, subscribe


@pytest.fixture
def setup():
    class Klass:
        @publisher
        def event(self, text: str, flag: bool = True):
            return self, text, flag

        @publisher
        def event_2(self, text: str, number: int, flag: bool = True):
            return self, text, number, flag

    subscribers = SimpleNamespace(
        on_event_before=[],
        on_event_after=[],
        on_event_2_before=[],
        on_event_2_after=[],
        on_both_events=[],
    )

    @subscribe.before(Klass.event)
    def on_event_before(instance: Klass, text, flag: bool = True):
        subscribers.on_event_before.append((instance, text, flag))

    @subscribe(Klass.event)
    def on_event_after(instance: Klass, text, flag: bool = True):
        subscribers.on_event_after.append((instance, text, flag))

    @subscribe.before(Klass.event_2)
    def on_event_2_before(instance: Klass, text, number, flag: bool = True):
        subscribers.on_event_2_before.append((instance, text, number, flag))

    @subscribe(Klass.event_2)
    def on_event_2_after(instance: Klass, text, number, flag: bool = True):
        subscribers.on_event_2_after.append((instance, text, number, flag))

    @subscribe.before(Klass.event)
    @subscribe.before(Klass.event_2)
    def on_both_events(instance: Klass, *args, **kwargs):
        subscribers.on_both_events.append((instance, args, kwargs))

    return Klass, subscribers


def test_event(setup):
    Klass, subscribers = setup

    instance = Klass()
    instance_2 = Klass()

    return_value_instance = instance.event('text', flag=False)
    return_value_instance_2 = instance_2.event('text_2', flag=True)

    assert return_value_instance == (instance, "text", False)
    assert return_value_instance_2 == (instance_2, "text_2", True)

    assert subscribers.on_event_before == [
        (instance, 'text', False),
        (instance_2, 'text_2', True),
    ]
    assert subscribers.on_event_after == [
        (instance, 'text', False),
        (instance_2, 'text_2', True),
    ]
    assert subscribers.on_event_2_before == []
    assert subscribers.on_event_2_after == []
    assert subscribers.on_both_events == [
        (instance, ('text',), {"flag": False}),
        (instance_2, ('text_2',), {"flag": True}),
    ]


def test_event_class(setup):
    Klass, subscribers = setup

    instance = Klass()
    instance_2 = Klass()

    return_value_instance = Klass.event(instance, 'text', flag=False)
    return_value_instance_2 = Klass.event(instance_2, 'text_2', flag=True)
    
    assert return_value_instance == (instance, "text", False)
    assert return_value_instance_2 == (instance_2, "text_2", True)
    
    assert subscribers.on_event_before == [
        (instance, 'text', False),
        (instance_2, 'text_2', True),
    ]
    assert subscribers.on_event_after == [
        (instance, 'text', False),
        (instance_2, 'text_2', True),
    ]
    assert subscribers.on_event_2_before == []
    assert subscribers.on_event_2_after == []
    assert subscribers.on_both_events == [
        (instance, ('text',), {"flag": False}),
        (instance_2, ('text_2',), {"flag": True}),
    ]


def test_event_2(setup):
    Klass, subscribers = setup

    instance = Klass()
    instance_2 = Klass()

    return_value_instance = instance.event_2('text', 10, flag=False)
    return_value_instance_2 = instance_2.event_2('text_2', 20, flag=True)

    assert return_value_instance == (instance, "text", 10, False)
    assert return_value_instance_2 == (instance_2, "text_2", 20, True)

    assert subscribers.on_event_before == []
    assert subscribers.on_event_after == []
    assert subscribers.on_event_2_before == [
        (instance, 'text', 10, False),
        (instance_2, 'text_2', 20, True),
    ]
    assert subscribers.on_event_2_after == [
        (instance, 'text', 10, False),
        (instance_2, 'text_2', 20, True),
    ]
    assert subscribers.on_both_events == [
        (instance, ('text', 10), {"flag": False}),
        (instance_2, ('text_2', 20), {"flag": True}),
    ]
