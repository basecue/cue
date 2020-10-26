from cue import publisher, subscribe


class Klass:
    @publisher
    def event(self, arg, kwarg: bool = True):
        pass


class Subscriber:
    @subscribe.before(Klass.event)
    @staticmethod
    def on_event(arg, *, kwarg):
        pass

    @subscribe.before(Klass.event)
    @classmethod
    def on_event(cls, arg, *, kwarg):
        pass


instance = Klass()
instance_2 = Klass()

subscriber = Subscriber()
subscriber_2 = Subscriber()
