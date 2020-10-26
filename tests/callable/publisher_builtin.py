from cue import publisher, subscribe


class Klass(list):
    append = publisher(list.append)


@subscribe.after(Klass.append)
def on_event_2(instance, item):
    pass


klass = Klass()
