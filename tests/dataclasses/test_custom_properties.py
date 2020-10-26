import dataclasses
from typing import Union

from cue import publisher, subscribe


@publisher
@dataclasses.dataclass
class Klass:
    text: str
    flag: bool

    _flag: bool

    @property
    def flag(self) -> bool:
        return self._flag

    @flag.setter  # FIXME is it publisher neccesary?
    def flag(self, value) -> None:
        self._flag = value


@subscribe.after(Klass.flag)
def on_change_flag(instance: Klass, flag: bool) -> None:
    pass


@subscribe.before(Klass.flag)
def on_change_flag(instance: Klass, flag: bool) -> None:
    pass


@subscribe.before(Klass.text)
@subscribe.before(Klass.flag)
def on_change(instance: Klass, value: Union[str, bool]) -> None:
    pass


@subscribe.before(Klass.flag)
@subscribe.before(Klass.text)
def on_change(instance: Klass, value: Union[str, bool]) -> None:
    pass
