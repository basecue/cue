from cue import publisher, subscribe


@publisher
def event(arg, kwarg: bool = True):
    pass


@publisher
def event_2(arg, arg_2, kwarg: bool = True):
    pass


class Subscriber:
    @subscribe.before(event)
    def on_event(self, arg, *, kwarg):
        pass

    @subscribe.after(event)
    def on_event(self, arg, *, kwarg):
        pass

    @subscribe.before(event_2)
    def on_event_2(self, arg, arg_2, *, kwarg):
        pass

    @subscribe.after(event_2)
    def on_event_2(self, arg, arg_2, *, kwarg):
        pass

    @subscribe.before(event)
    @subscribe.before(event_2)
    def on_both_events(self, *args, **kwargs):
        pass


subscriber = Subscriber()
subscriber_2 = Subscriber()
