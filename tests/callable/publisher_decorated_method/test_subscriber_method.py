from cue import publisher, subscribe


class Klass:
    @publisher
    @staticmethod
    def event(arg, kwarg: bool = True):
        pass

    @publisher
    @classmethod
    def event_static(cls, arg, kwarg: bool = True):
        pass


class Subscriber:
    @subscribe.before(Klass.event)
    def on_event(self, arg, *, kwarg):
        pass

    @subscribe.after(Klass.event)
    def on_event(self, arg, *, kwarg):
        pass

    @subscribe.before(Klass.event_static)
    def on_event_2(self, arg, arg_2, *, kwarg):
        pass

    @subscribe.after(Klass.event_static)
    def on_event_2(self, arg, arg_2, *, kwarg):
        pass

    @subscribe.before(Klass.event)
    @subscribe.before(Klass.event_static)
    def on_both_events(self, *args, **kwargs):
        pass


instance = Klass()
instance_2 = Klass()

subscriber = Subscriber()
subscriber_2 = Subscriber()
