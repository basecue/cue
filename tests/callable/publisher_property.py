from cue import subscribe


class Klass:
    def __init__(self):
        self._flag = True

    @property
    def flag(self):
        return self._flag

    @flag.setter
    def flag(self, value):
        self._flag = value


@subscribe.after(Klass.flag)
def on_event_2(instance, value):
    pass


klass = Klass()

