from cue import publisher, subscribe


@publisher
def event(arg, kwarg: bool = True):
    pass


class Subscriber:
    @subscribe.before(event)
    @staticmethod
    def on_event(arg, *, kwarg):
        pass

    @subscribe.before(event)
    @classmethod
    def on_event(cls, arg, *, kwarg):
        pass


subscriber = Subscriber()
subscriber_2 = Subscriber()
