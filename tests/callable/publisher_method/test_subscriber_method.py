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

    class Subscriber:
        subscribers = SimpleNamespace(
            on_event_before=[],
            on_event_after=[],
            on_event_2_before=[],
            on_event_2_after=[],
            on_both_events=[],
        )

        @subscribe.before(Klass.event)
        def on_event_before(self, instance: Klass, text: str, flag: bool = True):
            self.subscribers.on_event_before.append((self, instance, text, flag))

        @subscribe(Klass.event)
        def on_event_after(self, instance: Klass, text: str, flag: bool = True):
            self.subscribers.on_event_after.append((self, instance, text, flag))

        @subscribe.before(Klass.event_2)
        def on_event_2_before(self, instance: Klass, text: str, number: int, flag: bool = True):
            self.subscribers.on_event_2_before.append((self, instance, text, number, flag))

        @subscribe(Klass.event_2)
        def on_event_2_after(self, instance: Klass, text: str, number: int, flag: bool = True):
            self.subscribers.on_event_2_after.append((self, instance, text, number, flag))

        @subscribe.before(Klass.event)
        @subscribe.before(Klass.event_2)
        def on_both_events(self, instance: Klass, *args, **kwargs):
            self.subscribers.on_both_events.append((self, instance, args, kwargs))

    return Klass, Subscriber


def test_event(setup):
    Klass, Subscriber = setup

    instance = Klass()
    instance_2 = Klass()

    subscriber = Subscriber()
    subscriber_2 = Subscriber()

    return_value_instance = instance.event('text', flag=False)
    return_value_instance_2 =instance_2.event('text_2', flag=True)

    assert return_value_instance == (instance, "text", False)
    assert return_value_instance_2 == (instance_2, "text_2", True)

    assert Subscriber.subscribers.on_event_before == [
        (subscriber, instance, 'text', False),
        (subscriber_2, instance, 'text', False),
        (subscriber, instance_2, 'text_2', True),
        (subscriber_2, instance_2, 'text_2', True),
    ]
    assert Subscriber.subscribers.on_event_after == [
        (subscriber, instance, 'text', False),
        (subscriber_2, instance, 'text', False),
        (subscriber, instance_2, 'text_2', True),
        (subscriber_2, instance_2, 'text_2', True),
    ]
    assert Subscriber.subscribers.on_event_2_before == []
    assert Subscriber.subscribers.on_event_2_after == []
    assert Subscriber.subscribers.on_both_events == [
        (subscriber, instance, ('text',), {"flag": False}),
        (subscriber_2, instance, ('text',), {"flag": False}),
        (subscriber, instance_2, ('text_2',), {"flag": True}),
        (subscriber_2, instance_2, ('text_2',), {"flag": True}),
    ]


def test_event_class_call(setup):
    Klass, Subscriber = setup

    instance = Klass()
    instance_2 = Klass()

    subscriber = Subscriber()
    subscriber_2 = Subscriber()

    return_value_instance = Klass.event(instance, 'text', flag=False)
    return_value_instance_2 = Klass.event(instance_2, 'text_2', flag=True)

    assert return_value_instance == (instance, "text", False)
    assert return_value_instance_2 == (instance_2, "text_2", True)

    assert Subscriber.subscribers.on_event_before == [
        (subscriber, instance, 'text', False),
        (subscriber_2, instance, 'text', False),
        (subscriber, instance_2, 'text_2', True),
        (subscriber_2, instance_2, 'text_2', True),
    ]
    assert Subscriber.subscribers.on_event_after == [
        (subscriber, instance, 'text', False),
        (subscriber_2, instance, 'text', False),
        (subscriber, instance_2, 'text_2', True),
        (subscriber_2, instance_2, 'text_2', True),
    ]
    assert Subscriber.subscribers.on_event_2_before == []
    assert Subscriber.subscribers.on_event_2_after == []
    assert Subscriber.subscribers.on_both_events == [
        (subscriber, instance, ('text',), {"flag": False}),
        (subscriber_2, instance, ('text',), {"flag": False}),
        (subscriber, instance_2, ('text_2',), {"flag": True}),
        (subscriber_2, instance_2, ('text_2',), {"flag": True}),
    ]

def test_event_2(setup):
    Klass, Subscriber = setup

    instance = Klass()
    instance_2 = Klass()

    subscriber = Subscriber()
    subscriber_2 = Subscriber()

    return_value_instance = instance.event_2('text', 10, flag=False)
    return_value_instance_2 = instance_2.event_2('text_2', 20, flag=True)

    assert return_value_instance == (instance, "text", 10, False)
    assert return_value_instance_2 == (instance_2, "text_2", 20, True)

    assert Subscriber.subscribers.on_event_before == []
    assert Subscriber.subscribers.on_event_after == []
    assert Subscriber.subscribers.on_event_2_before == [
        (subscriber, instance, 'text', 10, False),
        (subscriber_2, instance, 'text', 10, False),
        (subscriber, instance_2, 'text_2', 20, True),
        (subscriber_2, instance_2, 'text_2', 20, True),
    ]
    assert Subscriber.subscribers.on_event_2_after == [
        (subscriber, instance, 'text', 10, False),
        (subscriber_2, instance, 'text', 10, False),
        (subscriber, instance_2, 'text_2', 20, True),
        (subscriber_2, instance_2, 'text_2', 20, True),
    ]
    assert Subscriber.subscribers.on_both_events == [
        (subscriber, instance, ('text', 10), {"flag": False}),
        (subscriber_2, instance, ('text', 10), {"flag": False}),
        (subscriber, instance_2, ('text_2', 20), {"flag": True}),
        (subscriber_2, instance_2, ('text_2', 20), {"flag": True}),
    ]