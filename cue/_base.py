from __future__ import annotations

import dataclasses
import functools
from types import BuiltinFunctionType, MethodWrapperType
from typing import Any, Callable, Generic, List, NamedTuple, Optional, Type, \
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
        func: Callable[[PublisherReturnValue], Any],
    ):
        self.__call__ = func
        self.specific_publisher_subscribers_set = set()

    def subscribe(self, specific_publisher_subscribers):
        specific_publisher_subscribers.append(self.__call__)
        self.specific_publisher_subscribers_set.add(specific_publisher_subscribers)

    # def __call__(self, *args, **kwargs):
    #     """
    #     To support also cls.__call__(instance, ...)
    #     """
    #     return self.__call__(*args, **kwargs)

    def __get__(
        self,
        instance: Optional[object], owner: Type[object]
    ) -> _Subscriber[PublisherReturnValue]:
        if instance is not None:
            self.__call__ = self.__call__.__get__(instance, owner)
        return self

    def __set_name__(self, owner: Type[object], name: str) -> None:
        # for method decorator it should be bind to instance
        for specific_publisher_subscribers in self.specific_publisher_subscribers_set:
            specific_publisher_subscribers.remove(self.__call__)

        if hasattr(owner, '__init__'):
            def init_wrapper(init_func):
                @functools.wraps(init_func)
                def _wrapper(instance, *args, **kwargs):
                    for specific_publisher_subscribers in self.specific_publisher_subscribers_set:
                        specific_publisher_subscribers.append(
                            self.__call__.__get__(instance, instance.__class__)
                        )
                    init_func(instance, *args, **kwargs)

                return _wrapper

            owner.__init__ = init_wrapper(owner.__init__)
        else:
            def _init(instance, *args, **kwargs):
                for specific_publisher_subscribers in self.specific_publisher_subscribers_set:
                    _subscribe(specific_publisher_subscribers)(
                        self.__call__.__get__(instance, instance.__class__)
                    )
                super().__init__(*args, **kwargs)

            owner.__init__ = _init


class SubscriberList(list):
    def __hash__(self):
        return id(self)


class Subscribers(NamedTuple):
    before: List[SubscriberFunc[PublisherReturnValue]]
    after: List[SubscriberFunc[PublisherReturnValue]]


class _Publisher(Generic[PublisherReturnValue]):
    def __init__(self, func: PublisherFunc[PublisherReturnValue]) -> None:
        self._subscribers = Subscribers(SubscriberList(), SubscriberList())
        self._func = func
        self._instance: Any = None

    def __call__(self, *args: Any, **kwargs: Any) -> PublisherReturnValue:
        if self._instance is None:
            subscriber_args = args
        else:
            subscriber_args = (self._instance,) + args

        for subscriber in self._subscribers.before:
            subscriber(*subscriber_args, **kwargs)

        ret = self._func(*args, **kwargs)

        for subscriber in self._subscribers.after:
            subscriber(*subscriber_args, **kwargs)
        return ret

    def __set__(self, instance, value):
        for subscriber in self._subscribers.before:
            subscriber(instance, value)
        self._func.__set__(instance, value)
        for subscriber in self._subscribers.after:
            subscriber(instance, value)

    def __get__(
        self,
        instance: Optional[object],
        owner: Type[object]
    ) -> publisher[PublisherReturnValue]:
        if instance and isinstance(self._func, property):
            return self._func.__get__(instance)
        self._instance = instance
        if not isinstance(self._func, (BuiltinFunctionType, MethodWrapperType)):
            self._func = self._func.__get__(instance, owner)
        return self

    def __repr__(self):
        return repr(self._func)


def _getter(p_field_name):
    def getter(self):
        return getattr(self, p_field_name)

    return getter


def _setter(p_field_name):
    def setter(self, value):
        setattr(self, p_field_name, value)

    return setter


def publisher(obj):
    if isinstance(obj, type):
        if dataclasses.is_dataclass(obj):
            for field in dataclasses.fields(obj):
                p_field_name = f"_{field.name}"
                p_property = property(_getter(p_field_name))
                p_property = p_property.setter(_setter(p_field_name))
                setattr(obj, field.name, _Publisher(p_property))

            return obj
    else:
        return _Publisher(obj)


# @overload
# def subscribe(
#     publisher: PublisherFunc[PublisherReturnValue]
# ) -> Callable[
#     [Callable[[PublisherReturnValue], SubscriberReturnValue]],
#     Callable[[PublisherReturnValue], SubscriberReturnValue]
# ]:
#     ...


def _subscribe(
    specific_publisher_subscribers: List
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
    def __subscribe(
        func: Callable[[PublisherClass], SubscriberReturnValue]
    ) -> Callable[[PublisherClass, PublisherReturnValue], SubscriberReturnValue]:
        ...

    @overload
    def __subscribe(
        func: Callable[[PublisherReturnValue], SubscriberReturnValue]
    ) -> Callable[[PublisherReturnValue], SubscriberReturnValue]:
        ...

    def __subscribe(
        func: Union[
            Callable[[PublisherClass], SubscriberReturnValue],
            Callable[[PublisherReturnValue], SubscriberReturnValue]
        ]
    ) -> Union[
        Callable[[Any, PublisherReturnValue], SubscriberReturnValue],
        Callable[[PublisherReturnValue], SubscriberReturnValue]
    ]:
        if isinstance(func, _Subscriber):
            subscriber = func
        else:
            subscriber = _Subscriber(func)

        subscriber.subscribe(specific_publisher_subscribers)
        return subscriber

    return __subscribe


class subscribe:
    @staticmethod
    def after(publisher: Union[
        Cue[PublisherClass, PublisherReturnValue],
        PublisherFunc[PublisherReturnValue]
    ]):
        return _subscribe(publisher._subscribers.after)

    @staticmethod
    def before(publisher: Union[
        Cue[PublisherClass, PublisherReturnValue],
        PublisherFunc[PublisherReturnValue]
    ]):
        return _subscribe(publisher._subscribers.before)
