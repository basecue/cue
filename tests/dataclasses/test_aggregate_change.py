import dataclasses
from typing import Union

from cue import publisher, subscribe


@publisher
@dataclasses.dataclass
class Klass:
    text: str
    flag: bool

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        @subscribe.after(Klass.text)
        @subscribe.after(Klass.flag)
        def _change(instance, *_args):
            instance.on_change()

    @publisher
    def on_change(self):
        pass


@subscribe.after(Klass.text)
def on_change_is_available(instance: Klass, text):
    pass


@subscribe.before(Klass.flag)
def on_change_is_available(instance: Klass, flag):
    pass


@subscribe.before(Klass.text)
@subscribe.before(Klass.flag)
def on_change_is_available(instance: Klass, value: Union[str, bool]):
    pass


@subscribe.before(Klass.change)
def on_change_is_available(instance):
    pass


@subscribe.after(Klass.change)
def on_change_is_available(instance):
    pass