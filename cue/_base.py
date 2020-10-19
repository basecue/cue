from __future__ import annotations

import functools
from types import BuiltinFunctionType, MethodWrapperType
from typing import Any, Callable, Generic, List, Optional, Type, \
    TypeVar, \
    Union, \
    overload

T = TypeVar('T')

PublisherReturnValue = TypeVar('PublisherReturnValue')
SubscriberReturnValue = TypeVar('SubscriberReturnValue')

# class PublisherFunc(Protocol[PublisherReturnValue]):
#     _subscribers: List[Callable[[PublisherReturnValue], SubscriberReturnValue]]
#     __call__: Callable[..., PublisherReturnValue]

PublisherFunc = Callable[..., PublisherReturnValue]

PublisherClass = TypeVar('PublisherClass')

FuncT = Callable[..., Any]


class _Subscriber(Generic[PublisherReturnValue]):
    def __init__(
        self,
        publisher: BasePublisher[PublisherReturnValue],
        func: Callable[[PublisherReturnValue], Any],
    ):
        self.publisher = publisher
        self.__call__ = func

    def __call__(self, *args, **kwargs):
        """
        To support also cls.__call__(instance, ...)
        """
        return self.__call__(*args, **kwargs)

    def __get__(
        self,
        instance: Optional[object], owner: Type[object]
    ) -> _Subscriber[PublisherReturnValue]:
        if instance is not None:
            self.__call__ = self.__call__.__get__(instance, owner)
        return self

    def __set_name__(self, owner: Type[object], name: str) -> None:
        # for method decorator it should be bind to instance
        self.publisher._subscribers.remove(self.__call__)
        if not hasattr(owner, '_subscribers'):
            owner._subscribers = []
        owner._subscribers.append(self)

        if getattr(owner, '_subscribed', False):
            return

        if hasattr(owner, '__init__'):
            def init_wrapper(init_func):
                @functools.wraps(init_func)
                def _wrapper(self, *args, **kwargs):
                    for subscriber in self._subscribers:
                        subscribe(subscriber.publisher)(
                            subscriber.__call__.__get__(self, self.__class__)
                        )
                    init_func(self, *args, **kwargs)

                return _wrapper

            owner.__init__ = init_wrapper(owner.__init__)
        else:
            def _init(self, *args, **kwargs):
                for subscriber in self._subscribers:
                    subscribe(subscriber.publisher)(
                        subscriber.__call__.__get__(self, self.__class__)
                    )
                super().__init__(*args, **kwargs)

            owner.__init__ = _init
        owner._subscribed = True


class BasePublisher(Generic[PublisherReturnValue]):
    def __init__(self) -> None:
        self._subscribers: List[SubscriberFunc[PublisherReturnValue]] = []

    def unsubscribe(self, subscriber: _Subscriber[PublisherReturnValue]) -> None:
        self._subscribers.remove(subscriber.__call__)


class publisher(BasePublisher[PublisherReturnValue]):
    def __init__(self, func: PublisherFunc[PublisherReturnValue]) -> None:
        super().__init__()
        self._func = func
        self._instance: Any = None

    def __call__(self, *args: Any, **kwargs: Any) -> PublisherReturnValue:
        ret = self._func(*args, **kwargs)
        if self._instance is not None:
            args = (self._instance,) + args
        for subscriber in self._subscribers:
            subscriber(*args, **kwargs)
        return ret

    def __get__(self, instance: Optional[object], owner: Type[object]) -> publisher[
        PublisherReturnValue]:
        self._instance = instance
        if not isinstance(self._func, (BuiltinFunctionType, MethodWrapperType)):
            self._func = self._func.__get__(instance, owner)
        return self

    def __repr__(self):
        return repr(self._func)


class Cue(
    Generic[PublisherClass, PublisherReturnValue],
    BasePublisher[PublisherReturnValue]
):
    _value: PublisherReturnValue

    @overload
    def __get__(
        self,
        instance: None,
        owner: Type[PublisherClass]
    ) -> Cue[PublisherClass, PublisherReturnValue]:
        ...

    @overload
    def __get__(
        self,
        instance: PublisherClass,
        owner: Type[PublisherClass]
    ) -> Optional[PublisherReturnValue]:
        ...

    def __get__(self,
        instance: Optional[PublisherClass],
        owner: Type[PublisherClass]
    ) -> Union[
        Cue[PublisherClass, PublisherReturnValue],
        Optional[PublisherReturnValue]
    ]:
        if instance is None:
            return self
        return self._value

    def __set__(self, instance: PublisherClass, value: PublisherReturnValue) -> None:
        self._value = value
        for subscriber in self._subscribers:
            subscriber(instance)


@overload
def subscribe(
    publisher: Cue[PublisherClass, PublisherReturnValue]
) -> Callable[
    [Callable[[PublisherClass, PublisherReturnValue], SubscriberReturnValue]],
    Callable[[PublisherClass, PublisherReturnValue], SubscriberReturnValue]
]:
    ...


@overload
def subscribe(
    publisher: PublisherFunc[PublisherReturnValue]
) -> Callable[
    [Callable[[PublisherReturnValue], SubscriberReturnValue]],
    Callable[[PublisherReturnValue], SubscriberReturnValue]
]:
    ...


def subscribe(
    publisher: Union[
        Cue[PublisherClass, PublisherReturnValue],
        PublisherFunc[PublisherReturnValue]
    ]
) -> Union[
    Callable[
        [Callable[[PublisherClass, PublisherReturnValue], SubscriberReturnValue]],
        Callable[[PublisherClass, PublisherReturnValue], SubscriberReturnValue]
    ],
    Callable[
        [Callable[[PublisherReturnValue], SubscriberReturnValue]],
        Callable[[PublisherReturnValue], SubscriberReturnValue]
    ]
]:
    @overload
    def _subscribe(
        func: Callable[[PublisherClass], SubscriberReturnValue]
    ) -> Callable[[PublisherClass, PublisherReturnValue], SubscriberReturnValue]:
        ...

    @overload
    def _subscribe(
        func: Callable[[PublisherReturnValue], SubscriberReturnValue]
    ) -> Callable[[PublisherReturnValue], SubscriberReturnValue]:
        ...

    def _subscribe(
        func: Union[
            Callable[[PublisherClass], SubscriberReturnValue],
            Callable[[PublisherReturnValue], SubscriberReturnValue]
        ]
    ) -> Union[
        Callable[[Any, PublisherReturnValue], SubscriberReturnValue],
        Callable[[PublisherReturnValue], SubscriberReturnValue]
    ]:
        publisher._subscribers.append(func)
        return _Subscriber(publisher, func)

    return _subscribe
