from cue import publisher, subscribe


class Klass:
    @publisher
    def event(self, arg, kwarg: bool = True):
        pass

    @publisher
    def event_2(self, arg, arg_2, kwarg: bool = True):
        pass


@subscribe.before(Klass.event)
def on_event(arg, *, kwarg):
    pass


@subscribe.after(Klass.event)
def on_event(arg, *, kwarg):
    pass


@subscribe.before(Klass.event_2)
def on_event_2(arg, arg_2, *, kwarg):
    pass


@subscribe.after(Klass.event_2)
def on_event_2(arg, arg_2, *, kwarg):
    pass


@subscribe.before(Klass.event)
@subscribe.before(Klass.event_2)
def on_both_events(*args, **kwargs):
    pass


instance = Klass()
instance_2 = Klass()
