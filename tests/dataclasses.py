@dataclasses.dataclass
@cue.publisher
class Device:
    uid: bytes
    ip: str
    is_available: bool
    is_known: bool


@cue.subscribe.after(Device.is_available)
def on_change_is_available(device, is_available):
    pass


@cue.subscribe.before(Device.is_available)
def on_change_is_available(device, is_available):
    pass


@cue.subscribe.before(Device.is_known)
@cue.subscribe.before(Device.is_available)
def on_change_is_available(device, value):
    pass
