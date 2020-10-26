import dataclasses
from typing import Union

from cue import publisher, subscribe


@publisher
@dataclasses.dataclass
class Klass:
    text: str
    flag: bool


@subscribe.before(Klass.text)
def on_change_before_text(instance: Klass, flag: bool):
    pass


@subscribe.after(Klass.text)
def on_change_after_text(instance: Klass, flag: bool):
    pass


@subscribe.before(Klass.flag)
def on_change_before_flag(instance: Klass, flag: bool):
    pass


@subscribe.after(Klass.flag)
def on_change_after_flag(instance: Klass, flag: bool):
    pass


@subscribe.before(Klass.text)
@subscribe.before(Klass.flag)
def on_change_before(instance: Klass, value: Union[str, bool]):
    pass


@subscribe.after(Klass.text)
@subscribe.after(Klass.flag)
def on_change_after(instance: Klass, value: Union[str, bool]):
    pass
