from cue import publisher, subscribe


@publisher
def event(arg, kwarg: bool = True):
    pass


@publisher
def event_2(arg, arg_2, kwarg: bool = True):
    pass


@subscribe.before(event)
def on_event(arg, *, kwarg):
    pass


@subscribe.after(event)
def on_event(arg, *, kwarg):
    pass


@subscribe.before(event_2)
def on_event_2(arg, arg_2, *, kwarg):
    pass


@subscribe.after(event_2)
def on_event_2(arg, arg_2, *, kwarg):
    pass


@subscribe.before(event)
@subscribe.before(event_2)
def on_both_events(*args, **kwargs):
    pass
